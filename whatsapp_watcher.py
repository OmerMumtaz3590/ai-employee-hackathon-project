"""
WhatsApp Watcher - Monitors unread chats for urgent keywords using Playwright.
Part of AI Employee Bronze hackathon project.
"""

import os
import json
import logging
import time
import re
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Configuration
CHECK_INTERVAL = 30  # seconds
SESSION_PATH = '/path/to/session'  # USER: Replace with your session directory
PROCESSED_IDS_FILE = 'processed_whatsapp_ids.json'
NEEDS_ACTION_DIR = Path('Needs_Action')

# Keywords to monitor (case-insensitive)
KEYWORDS = ['urgent', 'asap', 'invoice', 'payment', 'help']

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('whatsapp_watcher.log')
    ]
)
logger = logging.getLogger(__name__)


def load_processed_ids():
    """Load set of already processed message IDs."""
    if os.path.exists(PROCESSED_IDS_FILE):
        with open(PROCESSED_IDS_FILE, 'r') as f:
            data = json.load(f)
            return set(data.get('processed_ids', []))
    return set()


def save_processed_ids(processed_ids):
    """Save processed message IDs to file."""
    with open(PROCESSED_IDS_FILE, 'w') as f:
        json.dump({'processed_ids': list(processed_ids)}, f, indent=2)


def sanitize_filename(text, max_length=50):
    """Create a safe filename from text."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        text = text.replace(char, '_')
    return text[:max_length].strip().strip('.')


def find_keywords(text):
    """Find matching keywords in text (case-insensitive)."""
    text_lower = text.lower()
    matched = []
    for keyword in KEYWORDS:
        if keyword.lower() in text_lower:
            matched.append(keyword)
    return matched


def generate_message_id(chat_name, message_text, timestamp):
    """Generate a unique ID for a message."""
    import hashlib
    content = f"{chat_name}:{message_text}:{timestamp}"
    return hashlib.md5(content.encode()).hexdigest()[:16]


def create_action_file(chat_name, message_text, matched_keywords):
    """Create a markdown file in Needs_Action directory."""
    NEEDS_ACTION_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    chat_safe = sanitize_filename(chat_name)
    filename = f"whatsapp_{timestamp}_{chat_safe}.md"
    filepath = NEEDS_ACTION_DIR / filename

    received_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    keywords_str = ', '.join(matched_keywords)

    # Escape quotes in message for frontmatter
    message_escaped = message_text.replace('"', '\\"')
    chat_escaped = chat_name.replace('"', '\\"')

    content = f"""---
type: message
platform: whatsapp
from: "{chat_escaped}"
received: "{received_str}"
keywords: [{keywords_str}]
priority: high
status: pending
---

# WhatsApp Message from {chat_name}

**From:** {chat_name}
**Received:** {received_str}
**Keywords Matched:** {keywords_str}

## Message Content

{message_text}

---
*Action required. Review and respond to this message.*
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    logger.info(f"Created action file: {filepath}")
    return filepath


def wait_for_whatsapp_load(page, timeout=60000):
    """Wait for WhatsApp Web to fully load."""
    try:
        # Wait for the main chat list to appear
        page.wait_for_selector('[data-testid="chat-list"]', timeout=timeout)
        logger.info("WhatsApp Web loaded successfully")
        return True
    except PlaywrightTimeout:
        logger.warning("WhatsApp Web took too long to load. You may need to scan QR code.")
        return False


def get_unread_chats(page):
    """Get list of unread chats with their preview messages."""
    unread_chats = []

    try:
        # Find chat items with unread indicators
        chat_items = page.query_selector_all('[data-testid="cell-frame-container"]')

        for chat in chat_items:
            try:
                # Check for unread badge
                unread_badge = chat.query_selector('[data-testid="icon-unread-count"]')
                if not unread_badge:
                    # Alternative: check for unread indicator span
                    unread_span = chat.query_selector('span[aria-label*="unread"]')
                    if not unread_span:
                        continue

                # Get chat name
                name_elem = chat.query_selector('[data-testid="cell-frame-title"]')
                chat_name = name_elem.inner_text() if name_elem else "Unknown"

                # Get last message preview
                msg_elem = chat.query_selector('[data-testid="last-msg-status"]')
                if not msg_elem:
                    msg_elem = chat.query_selector('span[dir="ltr"]')
                message_preview = msg_elem.inner_text() if msg_elem else ""

                if chat_name and message_preview:
                    unread_chats.append({
                        'name': chat_name.strip(),
                        'preview': message_preview.strip()
                    })

            except Exception as e:
                logger.debug(f"Error parsing chat item: {e}")
                continue

    except Exception as e:
        logger.error(f"Error getting unread chats: {e}")

    return unread_chats


def open_chat_and_get_messages(page, chat_name, num_messages=5):
    """Open a specific chat and get recent messages."""
    messages = []

    try:
        # Search for the chat
        search_box = page.query_selector('[data-testid="chat-list-search"]')
        if search_box:
            search_box.click()
            search_box.fill(chat_name)
            time.sleep(1)

            # Click on the chat result
            chat_result = page.query_selector(f'span[title="{chat_name}"]')
            if chat_result:
                chat_result.click()
                time.sleep(1)

                # Get recent messages
                msg_elements = page.query_selector_all('[data-testid="msg-container"]')
                for msg in msg_elements[-num_messages:]:
                    try:
                        text_elem = msg.query_selector('span.selectable-text')
                        if text_elem:
                            messages.append(text_elem.inner_text())
                    except:
                        continue

                # Clear search
                search_box.fill('')
                page.keyboard.press('Escape')

    except Exception as e:
        logger.error(f"Error opening chat {chat_name}: {e}")

    return messages


def process_unread_chats(page, processed_ids):
    """Process unread chats and create action files for keyword matches."""
    unread_chats = get_unread_chats(page)
    logger.info(f"Found {len(unread_chats)} unread chats")

    new_count = 0

    for chat in unread_chats:
        chat_name = chat['name']
        preview = chat['preview']

        # Generate ID from preview (to avoid reprocessing same message)
        msg_id = generate_message_id(chat_name, preview, datetime.now().strftime('%Y%m%d%H'))

        if msg_id in processed_ids:
            logger.debug(f"Skipping already processed: {chat_name}")
            continue

        # Check for keywords in preview
        matched_keywords = find_keywords(preview)

        if matched_keywords:
            logger.info(f"Keywords {matched_keywords} found in chat: {chat_name}")

            # Optionally get more messages from the chat
            # messages = open_chat_and_get_messages(page, chat_name)
            # full_text = '\n'.join(messages) if messages else preview

            create_action_file(chat_name, preview, matched_keywords)
            processed_ids.add(msg_id)
            new_count += 1

    if new_count > 0:
        save_processed_ids(processed_ids)
        logger.info(f"Created {new_count} new action files")

    return new_count


def main():
    """Main entry point."""
    logger.info("=" * 50)
    logger.info("WhatsApp Watcher Starting")
    logger.info(f"Monitoring keywords: {KEYWORDS}")
    logger.info("=" * 50)

    # Validate session path
    if SESSION_PATH == '/path/to/session':
        logger.warning("Please update SESSION_PATH in the script to your actual session directory!")
        logger.info("The session directory stores your WhatsApp Web login state.")

    processed_ids = load_processed_ids()
    logger.info(f"Loaded {len(processed_ids)} previously processed message IDs")

    with sync_playwright() as p:
        # Launch browser with persistent context (maintains login)
        logger.info(f"Launching browser with session: {SESSION_PATH}")

        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_PATH,
            headless=False,  # WhatsApp Web requires visible browser
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox'
            ]
        )

        page = browser_context.new_page()

        try:
            logger.info("Navigating to WhatsApp Web...")
            page.goto('https://web.whatsapp.com', wait_until='networkidle')

            # Wait for WhatsApp to load (may require QR scan on first run)
            if not wait_for_whatsapp_load(page, timeout=120000):
                logger.info("Waiting for manual QR code scan...")
                wait_for_whatsapp_load(page, timeout=300000)

            logger.info("WhatsApp Web ready. Starting monitoring loop...")

            while True:
                try:
                    logger.info("Checking for unread messages with keywords...")
                    process_unread_chats(page, processed_ids)

                except Exception as e:
                    logger.error(f"Error in processing loop: {e}")

                    # Check if page is still valid
                    try:
                        page.title()
                    except:
                        logger.warning("Page disconnected, attempting to reconnect...")
                        page = browser_context.new_page()
                        page.goto('https://web.whatsapp.com', wait_until='networkidle')
                        wait_for_whatsapp_load(page)

                logger.info(f"Sleeping for {CHECK_INTERVAL} seconds...")
                time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            logger.info("Shutting down gracefully...")

        finally:
            browser_context.close()
            logger.info("Browser closed. Goodbye!")


if __name__ == '__main__':
    main()
