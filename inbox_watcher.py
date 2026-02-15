"""
Inbox Watcher - Bronze Tier AI Employee
Monitors Inbox/ folder and moves new files to Needs_Action/ for processing.
"""

import os
import shutil
import logging
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
BASE_DIR = Path(__file__).parent.resolve()
INBOX_DIR = BASE_DIR / "Inbox"
NEEDS_ACTION_DIR = BASE_DIR / "Needs_Action"
LOG_FILE = BASE_DIR / "watcher.log"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class InboxHandler(FileSystemEventHandler):
    """Handles new files dropped into Inbox/ folder."""

    def on_created(self, event):
        """Triggered when a new file is created in Inbox/."""
        if event.is_directory:
            return

        source_path = Path(event.src_path)

        # Skip temporary files and hidden files
        if source_path.name.startswith(".") or source_path.name.startswith("~"):
            logger.debug(f"Skipping temporary file: {source_path.name}")
            return

        # Wait briefly to ensure file is fully written
        import time
        time.sleep(0.5)

        # Check if file still exists (wasn't a temp file that got deleted)
        if not source_path.exists():
            logger.debug(f"File no longer exists: {source_path.name}")
            return

        self.process_new_file(source_path)

    def process_new_file(self, source_path: Path):
        """Copy file to Needs_Action/ with ITEM_ prefix and create metadata."""
        try:
            timestamp = datetime.now()
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            timestamp_prefix = timestamp.strftime("%Y%m%d_%H%M%S")

            # Generate new filename with ITEM_ prefix
            original_name = source_path.name
            new_name = f"ITEM_{timestamp_prefix}_{original_name}"
            dest_path = NEEDS_ACTION_DIR / new_name

            # Copy file to Needs_Action/
            shutil.copy2(source_path, dest_path)
            logger.info(f"Copied: {original_name} → {new_name}")

            # Create metadata file
            metadata_name = f"ITEM_{timestamp_prefix}_{source_path.stem}.md"
            metadata_path = NEEDS_ACTION_DIR / metadata_name

            # Don't create duplicate metadata if the original was already .md
            if source_path.suffix.lower() == ".md":
                metadata_path = dest_path  # Metadata will be the file itself
                self.prepend_metadata(metadata_path, original_name, timestamp_str)
            else:
                self.create_metadata_file(metadata_path, original_name, dest_path.name, timestamp_str)

            # Remove original from Inbox/ after successful copy
            source_path.unlink()
            logger.info(f"Removed original from Inbox: {original_name}")

        except Exception as e:
            logger.error(f"Error processing {source_path.name}: {e}")

    def create_metadata_file(self, metadata_path: Path, original_name: str,
                             copied_name: str, timestamp: str):
        """Create a metadata .md file for non-markdown files."""
        # Detect file type
        extension = Path(original_name).suffix.lower()
        file_type = self.detect_file_type(extension)

        content = f"""---
type: file_drop
original_name: {original_name}
copied_as: {copied_name}
received: {timestamp}
status: pending
file_type: {file_type}
---

# New Item: {original_name}

## Source
- Dropped into Inbox/ at {timestamp}
- File type: {file_type}

## Action Required
Review this item and determine next steps.

## Notes
(none yet)
"""
        metadata_path.write_text(content, encoding="utf-8")
        logger.info(f"Created metadata: {metadata_path.name}")

    def prepend_metadata(self, file_path: Path, original_name: str, timestamp: str):
        """Prepend YAML frontmatter to existing .md file."""
        try:
            existing_content = file_path.read_text(encoding="utf-8")

            # Check if frontmatter already exists
            if existing_content.strip().startswith("---"):
                logger.debug(f"Frontmatter already exists in {file_path.name}")
                return

            frontmatter = f"""---
type: file_drop
original_name: {original_name}
received: {timestamp}
status: pending
---

"""
            new_content = frontmatter + existing_content
            file_path.write_text(new_content, encoding="utf-8")
            logger.info(f"Added frontmatter to: {file_path.name}")

        except Exception as e:
            logger.error(f"Error adding frontmatter to {file_path.name}: {e}")

    def detect_file_type(self, extension: str) -> str:
        """Map file extension to a human-readable type."""
        type_map = {
            ".txt": "text",
            ".md": "markdown",
            ".pdf": "pdf_document",
            ".doc": "word_document",
            ".docx": "word_document",
            ".xls": "spreadsheet",
            ".xlsx": "spreadsheet",
            ".csv": "spreadsheet",
            ".json": "json_data",
            ".xml": "xml_data",
            ".eml": "email",
            ".msg": "email",
            ".png": "image",
            ".jpg": "image",
            ".jpeg": "image",
            ".gif": "image",
        }
        return type_map.get(extension, "unknown")


def ensure_directories():
    """Ensure required directories exist."""
    INBOX_DIR.mkdir(exist_ok=True)
    NEEDS_ACTION_DIR.mkdir(exist_ok=True)
    logger.info(f"Watching: {INBOX_DIR}")
    logger.info(f"Output to: {NEEDS_ACTION_DIR}")


def main():
    """Main entry point."""
    print("=" * 50)
    print("  AI Employee Inbox Watcher - Bronze Tier")
    print("=" * 50)
    print()

    ensure_directories()

    event_handler = InboxHandler()
    observer = Observer()
    observer.schedule(event_handler, str(INBOX_DIR), recursive=False)
    observer.start()

    logger.info("Watcher started. Press Ctrl+C to stop.")
    print()
    print(f"Drop files into: {INBOX_DIR}")
    print(f"They will appear in: {NEEDS_ACTION_DIR}")
    print()

    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping watcher...")
        observer.stop()

    observer.join()
    logger.info("Watcher stopped.")


if __name__ == "__main__":
    main()
