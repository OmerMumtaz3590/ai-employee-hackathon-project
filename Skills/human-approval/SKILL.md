---
name: human-approval
description: For sensitive actions, create approval .md in /Pending_Approval/. Wait for move to /Approved/ before acting.
---

# Human Approval Workflow

## Steps

1. **On sensitive action** (money, send, post):
   - Create file in `/Pending_Approval/` e.g. `APPROVAL_[action]_[date].md`
   - Include frontmatter:
     ```yaml
     ---
     type: approval_request
     action: [e.g. send_email]
     details: [description of the action]
     created: [timestamp]
     status: pending
     ---
     ```

2. **Add instructions** in file body:
   - "To approve: move this file to `/Approved/`"
   - "To reject: move this file to `/Rejected/` or delete it"

3. **Log to Dashboard.md**:
   - Add entry: "Approval pending for [action]"

4. **Later check**:
   - If file found in `/Approved/` → proceed with action (e.g. call MCP)
   - If file found in `/Rejected/` → log rejection and stop
   - If file still in `/Pending_Approval/` → wait

## Sensitive Actions (require approval)
- Sending emails
- Posting to social media
- Financial transactions
- External API calls with side effects
- Publishing content
- Deleting data
