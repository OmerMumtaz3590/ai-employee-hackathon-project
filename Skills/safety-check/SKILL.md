---
name: safety-check
description: Apply Company_Handbook.md rules before any action. Use always before processing, deciding or acting. Flag sensitive items. Prevents unsafe behavior.
---

# Safety Check Skill

## Mandatory checks (run first)
1. Read full Company_Handbook.md
2. Scan content for: money, payment, $ amount >100, urgent, asap, invoice, legal, personal info, new recipient
3. If any match → MUST flag for human review and stop
4. Log decision in Dashboard.md via update-dashboard skill if loaded
5. Output format: SAFE or FLAGGED: [reason]

## When to invoke
- Before any file move, log, or decision in other skills
- When user asks to act autonomously
