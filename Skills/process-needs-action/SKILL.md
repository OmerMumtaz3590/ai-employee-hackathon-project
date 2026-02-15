---
name: process-needs-action
description: Process files in the Needs_Action folder. Use when there are pending items to triage, summarize, act on or flag for review. Check against Company_Handbook.md rules. Move completed files to Done/ and log to Dashboard.md.
---

# Process Needs Action Skill

## When to use this skill
- Whenever /Needs_Action contains .md files
- When user asks to 'process pending', 'check inbox', 'handle new items' or similar
- Automatically consider using if context mentions new drops or watcher activity

## Core Instructions (follow exactly every time)
1. Read Company_Handbook.md from project root to load all rules.
2. List all .md files in /Needs_Action/ (use file system tools).
3. For each file:
   a. Read full content including frontmatter if present.
   b. Determine type (e.g. dropped_file, test_item, message).
   c. Apply handbook rules: check for money, urgent keywords, sensitivity.
   d. Decide action:
      - If simple and safe → summarize what it is, log short result.
      - If money > $100, new contact, sensitive → flag for human review.
      - If unsure → default to human review.
   e. Append log line to Dashboard.md under 'Recent Activity':
      Format: '- YYYY-MM-DD HH:MM | Processed [filename] → [result or Needs human review]'
   f. If action complete → move the file to /Done/
   g. If flagged → append to 'Needs Human Review' section in Dashboard.md
4. After processing all files, append a summary line to Dashboard.md:
   '- Needs_Action check complete. Processed X items, Y pending review.'
5. Never delete files. Never act on payments/emails without explicit approval.
6. Be verbose in logs for auditability.

## Examples
User says: process needs action
→ Skill activates → processes files → updates dashboard → moves to Done

## Troubleshooting
- Folder empty → log 'No pending items'
- Permission error → log error and stop
