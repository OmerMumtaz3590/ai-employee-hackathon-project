---
name: error-recovery
description: Handle system errors gracefully with retries, queuing, and alerts. Implements backoff strategies for transient errors and queues actions during authentication failures.
---

# Error Recovery Skill

## Purpose
Provide robust error handling for the AI Employee system by implementing retry mechanisms, queuing strategies, and alerting for various error conditions.

## When to Use This Skill
- When an MCP server returns an error
- When authentication fails for external services
- When network connectivity issues occur
- When external APIs are temporarily unavailable
- When any system component becomes unreachable

## Prerequisites
- Dashboard.md must be accessible for alerts
- Company_Handbook.md for understanding error handling policies
- Logs/ directory must exist for error logging

## Error Categories & Responses

### 1. Transient Errors (Network, Temporarily Unavailable)
For errors like:
- Network timeouts
- Service temporarily unavailable (HTTP 503)
- Rate limiting responses
- Temporary connection failures

**Response:**
1. **Detect transient error** in response from external service
2. **Implement exponential backoff** with random jitter:
   - First retry: 5-10 seconds
   - Second retry: 20-40 seconds
   - Third retry: 60-120 seconds
   - Maximum 3 retries before escalation
3. **Log retry attempts** to Dashboard.md with format:
   `- YYYY-MM-DD HH:MM | Retry attempt X for [component] | [error type]`
4. **Continue with original task** if recovery successful
5. **Escalate to queue** if retries exhausted

### 2. Authentication Failures
For errors like:
- Invalid credentials
- Token expiration
- Unauthorized access (HTTP 401/403)
- Session timeout

**Response:**
1. **Detect authentication error** in response
2. **Queue the action** in Queued_Actions/ folder with:
   - Original parameters
   - Timestamp
   - Error details
   - Component requiring authentication
3. **Alert via Dashboard.md** with format:
   `- YYYY-MM-DD HH:MM | [Component] offline - auth failure | Action queued for retry`
4. **Continue with other tasks** while monitoring for credential updates
5. **Retry queued actions** when authentication is restored

### 3. Permanent Errors
For errors like:
- Invalid parameters
- Resource not found (HTTP 404)
- Forbidden operations
- Data validation failures

**Response:**
1. **Log error permanently** to Dashboard.md with format:
   `- YYYY-MM-DD HH:MM | Permanent error in [component] | [error details] | Action failed`
2. **Stop current task** and mark as failed
3. **Continue with other tasks** if possible
4. **Notify human operator** if critical operation

## Retry Logic Implementation

### Backoff Algorithm
1. **Calculate delay** using exponential backoff with jitter:
   - Delay = BaseDelay × (2 ^ attempt_number) + random_jitter
   - BaseDelay = 5 seconds
   - Jitter = random value between -1 and 1 seconds
2. **Wait for calculated delay** before retry
3. **Update Dashboard.md** with retry status
4. **Proceed with retry** or escalate based on attempt count

### Queue Management
1. **Create queued action file** in Queued_Actions/ with format:
   ```
   ---
   type: queued_action
   original_action: [action_name]
   parameters: [original_params]
   queued_at: [timestamp]
   component: [affected_component]
   error_reason: [auth_failure, etc.]
   ---
   
   # Queued Action Details
   Original action: [action_name]
   Parameters: [parameters]
   Error: [error_details]
   ```
2. **Monitor for resolution** of authentication issues
3. **Process queued actions** when component becomes available
4. **Remove from queue** after successful processing

## Alerting System

### Dashboard Alerts
When components go offline:
1. **Log to Dashboard.md** with format:
   `- YYYY-MM-DD HH:MM | [Component] offline | [Reason] | [Action taken]`
2. **Include recovery strategy** used (retry, queue, etc.)
3. **Monitor for restoration** of component
4. **Update status** when component comes back online

### Component Offline Scenarios
- **MCP Servers**: Queue actions, alert in Dashboard
- **External APIs**: Retry with backoff, then queue if persistent
- **File System**: Alert and wait, do not retry indefinitely
- **Database Connections**: Retry with backoff, queue operations

## Integration with Other Skills
1. **Call error-recovery** whenever another skill encounters an error
2. **Pass error details** including component name and error type
3. **Receive recovery instruction** (retry, queue, escalate)
4. **Implement recommended action** based on error category

## Safety Measures
- Never retry indefinitely - always have maximum attempt limits
- Queue rather than fail when authentication issues occur
- Log all error recovery attempts for audit purposes
- Alert humans for persistent component failures
- Preserve original action parameters during queuing