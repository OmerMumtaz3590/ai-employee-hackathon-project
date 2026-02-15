"""
Gmail Watcher - Monitors unread important emails and creates action items.
Part of AI Employee Bronze hackathon project.
"""

import os
import json
import logging
import time
from datetime import datetime
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CHECK_INTERVAL = 120  # seconds
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'
PROCESSED_IDS_FILE = 'processed_email_ids.json'
NEEDS_ACTION_DIR = Path('Needs_Action')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('gmail_watcher.log')
    ]
)
logger = logging.getLogger(__name__)


def get_gmail_service():
    """Authenticate and return Gmail API service."""
    creds = None

    # Load existing token if available
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # Refresh or obtain new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                logger.error(f"Missing {CREDENTIALS_FILE}. Please download from Google Cloud Console.")
                raise FileNotFoundError(f"{CREDENTIALS_FILE} not found")

            logger.info("Initiating OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            logger.info(f"Credentials saved to {TOKEN_FILE}")

    return build('gmail', 'v1', credentials=creds)


def load_processed_ids():
    """Load set of already processed email IDs."""
    if os.path.exists(PROCESSED_IDS_FILE):
        with open(PROCESSED_IDS_FILE, 'r') as f:
            data = json.load(f)
            return set(data.get('processed_ids', []))
    return set()


def save_processed_ids(processed_ids):
    """Save processed email IDs to file."""
    with open(PROCESSED_IDS_FILE, 'w') as f:
        json.dump({'processed_ids': list(processed_ids)}, f, indent=2)


def sanitize_filename(text, max_length=50):
    """Create a safe filename from text."""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        text = text.replace(char, '_')
    # Truncate and strip
    return text[:max_length].strip().strip('.')


def get_header_value(headers, name):
    """Extract header value by name."""
    for header in headers:
        if header['name'].lower() == name.lower():
            return header['value']
    return ''


def create_action_file(email_data):
    """Create a markdown file in Needs_Action directory."""
    NEEDS_ACTION_DIR.mkdir(exist_ok=True)

    # Generate unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    subject_safe = sanitize_filename(email_data['subject'])
    filename = f"email_{timestamp}_{subject_safe}.md"
    filepath = NEEDS_ACTION_DIR / filename

    # Format received date
    received_dt = datetime.fromtimestamp(int(email_data['internal_date']) / 1000)
    received_str = received_dt.strftime('%Y-%m-%d %H:%M:%S')

    # Build markdown content with frontmatter
    content = f"""---
type: email
from: "{email_data['from']}"
subject: "{email_data['subject']}"
received: "{received_str}"
priority: high
status: pending
message_id: "{email_data['id']}"
---

# Email: {email_data['subject']}

**From:** {email_data['from']}
**Received:** {received_str}

## Snippet

{email_data['snippet']}

---
*Action required. Review and process this email.*
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    logger.info(f"Created action file: {filepath}")
    return filepath


def fetch_unread_important_emails(service):
    """Fetch unread important emails from Gmail."""
    try:
        # Query for unread important emails
        query = 'is:unread is:important'
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=20
        ).execute()

        messages = results.get('messages', [])
        logger.info(f"Found {len(messages)} unread important emails")
        return messages

    except HttpError as error:
        logger.error(f"Error fetching emails: {error}")
        return []


def get_email_details(service, message_id):
    """Get full email details by ID."""
    try:
        message = service.users().messages().get(
            userId='me',
            id=message_id,
            format='metadata',
            metadataHeaders=['From', 'Subject', 'Date']
        ).execute()

        headers = message.get('payload', {}).get('headers', [])

        return {
            'id': message_id,
            'from': get_header_value(headers, 'From'),
            'subject': get_header_value(headers, 'Subject') or '(No Subject)',
            'snippet': message.get('snippet', ''),
            'internal_date': message.get('internalDate', '0')
        }

    except HttpError as error:
        logger.error(f"Error getting email details for {message_id}: {error}")
        return None


def process_emails(service, processed_ids):
    """Main processing loop for emails."""
    messages = fetch_unread_important_emails(service)
    new_count = 0

    for msg in messages:
        msg_id = msg['id']

        if msg_id in processed_ids:
            logger.debug(f"Skipping already processed email: {msg_id}")
            continue

        email_data = get_email_details(service, msg_id)
        if email_data:
            create_action_file(email_data)
            processed_ids.add(msg_id)
            new_count += 1
            logger.info(f"Processed new email: {email_data['subject'][:50]}")

    if new_count > 0:
        save_processed_ids(processed_ids)
        logger.info(f"Processed {new_count} new emails")

    return new_count


def main():
    """Main entry point."""
    logger.info("=" * 50)
    logger.info("Gmail Watcher Starting")
    logger.info("=" * 50)

    try:
        service = get_gmail_service()
        logger.info("Gmail API service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Gmail service: {e}")
        return

    processed_ids = load_processed_ids()
    logger.info(f"Loaded {len(processed_ids)} previously processed email IDs")

    while True:
        try:
            logger.info("Checking for new unread important emails...")
            process_emails(service, processed_ids)

        except HttpError as error:
            if error.resp.status == 401:
                logger.warning("Token expired, re-authenticating...")
                service = get_gmail_service()
            else:
                logger.error(f"API error: {error}")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")

        logger.info(f"Sleeping for {CHECK_INTERVAL} seconds...")
        time.sleep(CHECK_INTERVAL)


if __name__ == '__main__':
    main()
