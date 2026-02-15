---
name: odoo-accounting
description: Interact with self-hosted Odoo via MCP for accounting (draft invoices, post with approval, get balance/transactions).
---

# Odoo Accounting Skill

## Purpose
Integrate with self-hosted Odoo ERP for accounting operations including invoice creation, posting, and financial reporting.

## When to Use This Skill
- When processing items in Needs_Action that involve invoicing or accounting
- When performing financial audits or balance checks
- When user requests Odoo accounting operations

## Prerequisites
- Odoo MCP server must be running and accessible
- Required environment variables must be configured
- Company_Handbook.md must be available for reference

## Steps

### 1. Invoice Processing
When handling invoice requests from Needs_Action (e.g. 'send invoice $1500'):

1. **Read Company_Handbook.md** to check amount thresholds and approval requirements
2. **Parse invoice request** to extract:
   - Partner/customer information
   - Amount to invoice
   - Description/service details
3. **Validate amount** against Company_Handbook thresholds
4. **Use MCP 'odoo'** to call `draft_invoice(partner_id, amount, description)`
5. **Check response** for success/error:
   - On success: note the draft invoice ID
   - On failure: log error and queue for retry
6. **Write draft ID** to Plan.md file in Plans/ directory
7. **Create approval request** in Pending_Approval/ODOO_INVOICE_[id].md with:
   ```
   ---
   type: approval_request
   action: post_invoice
   details: Post invoice #[id] for $[amount] to [customer]
   created: [timestamp]
   status: pending
   invoice_id: [id]
   ---
   ```
8. **Wait for approval** by checking if file is moved to Approved/ folder
9. **After approval**, use MCP 'odoo' to call `post_invoice(invoice_id)`
10. **Log the outcome** to Dashboard.md and move original file to Done/

### 2. Financial Audits
For periodic audits or user requests for financial data:

1. **Use MCP 'odoo'** to call `get_balance()` 
2. **Use MCP 'odoo'** to call `list_recent_transactions(limit=10)`
3. **Format data** into readable summary
4. **Save summary** to Briefings/Odoo_Balance_Summary_[date].md
5. **Include in summary**:
   - Total receivables
   - Total payables
   - Net position
   - Recent transaction list
   - Date of report

### 3. Logging
For every Odoo operation:

1. **Create log entry** in Logs/YYYY-MM/odoo_operations_[date].log
2. **Include timestamp**, operation type, parameters, and result
3. **Format as**: `[TIMESTAMP] [OPERATION] [PARAMS] -> [RESULT]`

### 4. Error Handling
If Odoo operations fail:

1. **Log error** with full details to Logs/
2. **Queue action** for retry if it's a connectivity issue
3. **Set status** to 'Odoo offline - retry later' in Plan.md
4. **Continue with other tasks** while periodically retrying
5. **Notify user** if critical operations cannot be completed

### 5. Compliance Checks
Always verify against Company_Handbook:

1. **Check amount thresholds** before processing any financial transaction
2. **Follow approval workflows** for amounts exceeding limits
3. **Apply sensitivity rules** to financial data
4. **Maintain audit trail** as per handbook requirements

## Example Usage

### Invoice Request Processing:
Input: "Invoice client $1500 for consulting work"
1. Parse request → amount=$1500, service="consulting work"
2. Check Company_Handbook → $1500 exceeds $100 threshold → requires approval
3. Call draft_invoice(partner_id, 1500, "Consulting work")
4. Get draft ID → create approval request in Pending_Approval/
5. Wait for approval → post invoice when approved

### Audit Request:
Input: "Get current account balance"
1. Call get_balance() → receive balance data
2. Call list_recent_transactions(limit=10) → receive transaction list
3. Format and save to Briefings/ as summary

## Safety Measures
- All invoice postings require explicit approval
- Amounts are validated against Company_Handbook thresholds
- Operations are logged for audit trail
- Graceful degradation when Odoo is unavailable