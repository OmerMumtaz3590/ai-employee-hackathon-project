---
name: update-dashboard
description: Safely append logs, status updates or summaries to Dashboard.md. Use when any action needs to be recorded, or when summarizing status. Always timestamp entries.
---

# Update Dashboard Skill

## Purpose
Keep Dashboard.md as single source of truth for activity and status.

## Rules
- Only append — never overwrite or delete existing content
- Use sections: Recent Activity, Quick Status, Needs Human Review
- Every entry starts with timestamp: '- YYYY-MM-DD HH:MM | '
- Keep entries concise (1-2 lines max)
- If updating status → find and replace only the Quick Status block if possible

## Steps
1. Read current Dashboard.md
2. Append new line(s) under appropriate section
3. If no section exists → create it
4. Write updated file back

## Example usage
Append: Processed test file → success
→ Adds line under Recent Activity
