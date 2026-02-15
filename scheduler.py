"""
AI Employee Scheduler
Runs scheduled tasks using the 'schedule' library.
"""

import schedule
import time
import subprocess
import os
from datetime import datetime

# Configuration
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
NEEDS_ACTION_DIR = os.path.join(WORKING_DIR, "Needs_Action")


def log(message: str):
    """Log message with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def run_claude_skill(skill_name: str, args: str = ""):
    """Invoke a Claude skill via CLI."""
    cmd = f'claude "{skill_name}{" " + args if args else ""}"'
    log(f"Running skill: {skill_name}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=WORKING_DIR,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        if result.returncode == 0:
            log(f"Skill {skill_name} completed successfully")
        else:
            log(f"Skill {skill_name} failed: {result.stderr}")
        return result
    except subprocess.TimeoutExpired:
        log(f"Skill {skill_name} timed out")
    except Exception as e:
        log(f"Error running skill {skill_name}: {e}")


def check_needs_action():
    """Check Needs_Action folder and process items."""
    log("Checking Needs_Action folder...")

    if not os.path.exists(NEEDS_ACTION_DIR):
        os.makedirs(NEEDS_ACTION_DIR)
        log("Created Needs_Action folder")
        return

    items = os.listdir(NEEDS_ACTION_DIR)
    if items:
        log(f"Found {len(items)} items in Needs_Action")
        run_claude_skill("process-needs-action")
    else:
        log("No items in Needs_Action")


def daily_linkedin_post():
    """Run LinkedIn sales post skill daily."""
    log("Running daily LinkedIn sales post...")
    run_claude_skill("linkedin-sales-post")


def weekly_audit():
    """Run reasoning loop for weekly audit."""
    log("Running weekly audit reasoning loop...")
    run_claude_skill("reasoning-loop", "audit")


def main():
    """Main scheduler loop."""
    log("=" * 50)
    log("AI Employee Scheduler Started")
    log("=" * 50)

    # Schedule tasks
    schedule.every(10).minutes.do(check_needs_action)
    schedule.every().day.at("08:00").do(daily_linkedin_post)
    schedule.every().sunday.at("09:00").do(weekly_audit)

    log("Scheduled tasks:")
    log("  - Every 10 min: Check Needs_Action")
    log("  - Daily at 8:00 AM: LinkedIn sales post")
    log("  - Weekly Sunday at 9:00 AM: Audit reasoning loop")
    log("-" * 50)

    # Run initial check
    check_needs_action()

    # Run forever
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    main()
