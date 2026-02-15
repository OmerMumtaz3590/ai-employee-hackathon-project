---
name: audit-logger
description: Log all system actions to JSON files in dated logs directory for compliance and debugging. Captures timestamp, action type, parameters, results, and approval status.
---

# Audit Logger Skill

## Purpose
Maintain a comprehensive, tamper-evident log of all system actions for compliance, debugging, and accountability purposes. Records all significant operations in structured JSON format.

## When to Use This Skill
- Before executing any significant action
- When logging MCP server interactions
- When recording approval workflows
- When documenting system state changes
- When tracking user-initiated operations

## Prerequisites
- Logs/ directory must exist with YYYY-MM subdirectories
- Company_Handbook.md for understanding logging requirements
- Dashboard.md for critical alert logging

## Logging Process

### 1. Prepare Log Entry
Before executing any action, prepare a structured log entry with:
- `timestamp`: ISO 8601 formatted datetime
- `action_type`: Type of action being performed
- `actor`: Who initiated the action (typically "claude")
- `parameters`: Input parameters for the action
- `result`: Outcome of the action
- `approval_status`: Current approval status if applicable

### 2. Determine Log File
1. **Get current date** in YYYY-MM-DD format
2. **Create/open log file** in Logs/YYYY-MM/ with name YYYY-MM-DD.json
3. **If directory doesn't exist**, create it before proceeding

### 3. Format JSON Entry
Create a JSON object with the following structure:
```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SS.sssZ",
  "action_type": "action_name",
  "actor": "claude",
  "parameters": {...},
  "result": {...},
  "approval_status": "pending|approved|rejected|not_required",
  "session_id": "unique_session_identifier",
  "correlation_id": "links_related_actions"
}
```

### 4. Append to Log File
1. **Read existing log file** if it exists
2. **Parse existing JSON** (should be an array of log entries)
3. **Append new entry** to the array
4. **Write updated array** back to the file in JSON format
5. **Preserve existing entries** - never overwrite

### 5. Action Types to Log
Log all of the following action types:

#### MCP Server Interactions
- `mcp_call`: Calls to any MCP server (email, odoo, twitter, etc.)
- `mcp_initialize`: MCP server initialization
- `mcp_list_tools`: Tool listing requests

#### File System Operations
- `file_create`: Creating new files
- `file_move`: Moving files between directories
- `file_update`: Updating existing files
- `file_delete`: Deleting files

#### Approval Workflows
- `approval_requested`: When approval is requested
- `approval_granted`: When approval is granted
- `approval_denied`: When approval is denied
- `action_approved`: When approved action is executed

#### Skill Executions
- `skill_start`: Beginning of skill execution
- `skill_complete`: Successful skill completion
- `skill_error`: Skill execution errors

#### System Events
- `system_start`: System startup events
- `system_shutdown`: System shutdown events
- `error_occurred`: Error events (logged with error-recovery skill)
- `dashboard_update`: Updates to Dashboard.md

## Special Handling

### Approval Status Tracking
For each action, determine and log the approval status:
- `not_required`: For safe, automated operations
- `pending`: For operations awaiting approval
- `approved`: For operations that received approval
- `rejected`: For operations that were rejected

### Parameter Sanitization
Before logging, sanitize parameters to remove sensitive information:
- Remove passwords, tokens, or other secrets
- Mask financial amounts if required by privacy policy
- Preserve enough detail for debugging while protecting privacy

### Result Sanitization
Similarly, sanitize results to remove sensitive data:
- Remove API responses containing personal data
- Mask error messages that might reveal system details
- Preserve error codes for debugging purposes

## Error Handling for Logger
If the audit logger itself fails:
1. **Attempt to log to Dashboard.md** as backup
2. **Continue with original action** - don't fail due to logging issues
3. **Queue log entry** for retry if file system issues occur
4. **Alert system administrator** about logging failure

## Integration with Other Skills
1. **Call audit-logger** at the beginning of significant operations
2. **Pass action details** including type, parameters, and initial state
3. **Update log entry** with results after operation completes
4. **Handle logging errors** gracefully without affecting main operation

## Log File Rotation
- **Daily rotation**: New file for each day
- **Monthly directories**: Organized by YYYY-MM
- **Retention policy**: Follow Company_Handbook guidelines for log retention
- **Backup considerations**: Ensure logs are included in system backups

## Compliance Considerations
- **Immutable logs**: Once written, logs should not be modified
- **Complete records**: Capture all significant system actions
- **Accurate timestamps**: Use UTC for consistency
- **Correlation IDs**: Link related actions for easier analysis
- **Privacy compliance**: Sanitize personal information per policy