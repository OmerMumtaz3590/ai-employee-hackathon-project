# AI Employee – Bronze, Silver & Gold Tiers

## Bronze Tier – Foundation
Local-first foundation: file drops → watcher → Claude processes → updates dashboard

### Folders
- `Inbox/`          → drop files here to test
- `Needs_Action/`   → watcher moves items here
- `Done/`           → completed items go here
- `Skills/`         → reusable agent behaviors

### How to use (Bronze)
1. Run watcher: `python inbox_watcher.py`
2. Drop any text file into `Inbox/`
3. Wait ~5s → check `Needs_Action/`
4. Process manually:
   ```bash
   claude "Read Company_Handbook.md and Skills/SKILL_Process_Needs_Action.md. Then process everything in /Needs_Action using the skill. Update Dashboard.md and move files to /Done/."
   ```

---

## Silver Tier – Advanced Features

### New Watchers (Gmail/WhatsApp)
Monitor external communication channels for actionable items.

```bash
# Gmail Watcher (requires credentials.json from Google Cloud Console)
python gmail_watcher.py

# WhatsApp Watcher (requires whatsapp-web.js setup)
python whatsapp_watcher.py
```

### LinkedIn Posting
Automated sales/content posting to LinkedIn.

```bash
# Manual trigger
claude "Run linkedin-sales-post skill"

# Scheduled via scheduler.py (daily at 8 AM)
```

### Reasoning Loop
Multi-step reasoning for complex decisions and audits.

```bash
# Run reasoning loop
claude "Run reasoning-loop skill for [task]"

# Weekly audit (scheduled Sundays)
claude "Run reasoning-loop audit"
```

### MCP Email Integration
Draft and send emails via MCP server.

```bash
# Draft email (uses human-approval for send)
claude "Use MCP email to draft [subject]"
```

### HITL (Human-in-the-Loop) Workflow
Sensitive actions require human approval before execution.

**Folders:**
- `Pending_Approval/` → approval requests await here
- `Approved/` → move files here to approve
- `Rejected/` → move files here to reject

```bash
# Create approval request
claude "Use human-approval for [action]"

# Check approval status
claude "Check Pending_Approval folder for status"
```

### Scheduling
Automated task scheduling with `schedule` library.

```bash
# Install dependencies
pip install schedule

# Run scheduler (runs forever)
python scheduler.py
```

**Scheduled Tasks:**
| Frequency | Time | Task |
|-----------|------|------|
| Every 10 min | - | Check `Needs_Action/` |
| Daily | 8:00 AM | LinkedIn sales post |
| Weekly | Sunday 9:00 AM | Audit reasoning loop |

---

## Gold Tier – Enterprise Features

### Odoo Integration
Self-hosted ERP integration for accounting operations.

```bash
# Draft invoice in Odoo (requires approval to post)
claude "Use odoo-accounting skill to draft invoice for client X"

# Post approved invoice
claude "Use odoo-accounting skill to post invoice #123"

# Get account balance summary
claude "Use odoo-accounting skill to get current balance"

# List recent transactions
claude "Use odoo-accounting skill to list recent transactions"
```

**Configuration:**
- Set environment variables: `ODOO_URL`, `DB_NAME`, `USER`, `PASSWORD`
- Requires Odoo MCP server running
- Draft operations auto-perform, posting requires approval

**Security Notes:**
- All financial operations require approval for posting
- Credentials stored in environment variables only
- Audit trail maintained for all financial operations

---

### Multi-Social Posting
Cross-platform social media management with platform-specific optimization.

```bash
# Create and schedule posts across platforms
claude "Use social-multi-post skill for [content idea from Business_Goals.md]"

# Post to specific platform
claude "Use social-multi-post skill to create Twitter post about [topic]"
```

**Supported Platforms:**
- Twitter/X: Short-form content with trending hashtags
- Instagram: Visual-focused content with stories support
- Facebook: Community-focused content with detailed information

**Configuration:**
- MCP servers for each platform: `mcp_servers/twitter`, `mcp_servers/instagram`, `mcp_servers/facebook`
- Platform-specific credentials required
- Auto-post for low-risk content, approval for sensitive content

**Security Notes:**
- All content undergoes safety-check before posting
- Approval required for potentially sensitive content
- Engagement metrics tracked and reported

---

### Weekly CEO Briefing
Automated executive reporting with business intelligence.

```bash
# Generate weekly CEO briefing manually
claude "Run weekly-ceo-briefing skill"

# Automatic generation every Sunday night
# Scheduled in scheduler.py
```

**Briefing Contents:**
- Executive Summary with business health score
- Revenue analysis with week-over-week comparisons
- Completed tasks with goal alignment
- Bottleneck identification with impact assessment
- Proactive suggestions for cost savings and growth

**Configuration:**
- Runs automatically every Sunday at 22:00
- Uses templates from `Audit_Templates/`
- Outputs to `Briefings/[date]_Monday_Briefing.md`

**Security Notes:**
- Financial data access limited to authorized personnel
- Confidential business information protected
- Audit trail maintained for all briefing generations

---

### Ralph Wiggum Autonomy
Autonomous task execution with intelligent stopping conditions.

```bash
# Run complex multi-step task autonomously
python Skills/ralph-autonomous-loop/ralph_orchestrator.py 'Process full invoice flow from WhatsApp to Odoo post'

# With custom iteration limit
python Skills/ralph-autonomous-loop/ralph_orchestrator.py --max-iterations 15 'Process client onboarding workflow'
```

**Features:**
- Context preservation between Claude iterations
- Intelligent stopping with `<promise>TASK_COMPLETE</promise>` detection
- Maximum iteration limits to prevent infinite loops
- Progress monitoring via folder state
- Integration with all available skills

**Security Notes:**
- Maximum iteration limits prevent resource exhaustion
- Context isolation between different tasks
- All actions logged for audit purposes

---

### Error Handling & Logging
Enterprise-grade resilience with comprehensive audit trails.

```bash
# Error recovery in action (automatic)
# Triggered when any skill encounters an error

# Audit logging in action (automatic)
# Applied to all system operations
```

**Error Recovery Features:**
- Transient error retries with exponential backoff
- Authentication failure queuing
- Component offline alerts to Dashboard.md
- Graceful degradation during partial outages

**Audit Logging Features:**
- Structured JSON logging to `Logs/YYYY-MM-DD.json`
- Comprehensive action tracking with parameters and results
- Approval status tracking for all operations
- Privacy-compliant data sanitization

**Security Notes:**
- Immutable logs with UTC timestamps
- Sensitive data sanitization in logs
- Access controls for log files
- Regular log rotation and retention policies

---

## Quick Start (Full System)

```bash
# 1. Install dependencies
pip install schedule watchdog

# 2. Configure environment variables for MCP servers
# Set ODOO_URL, DB_NAME, USER, PASSWORD for Odoo
# Set TWITTER_API_KEY, TWITTER_API_SECRET, etc. for social platforms

# 3. Start MCP servers (in separate terminals or background)
# Odoo MCP server:
python mcp_servers/odoo_accounting/odoo_mcp.py
# Twitter MCP server:
node mcp_servers/twitter/index.js
# Email MCP server:
node mcp_servers/email/index.js
# (Other MCP servers as needed)

# 4. Start scheduler (background)
python scheduler.py &

# 5. Start inbox watcher
python inbox_watcher.py

# 6. Start other watchers as needed
python gmail_watcher.py
python whatsapp_watcher.py
```

## MCP Server Troubleshooting

### Starting MCP Servers
If MCP servers fail to start or are not responding:

1. **Check environment variables**:
   ```bash
   # For Odoo
   echo $ODOO_URL
   echo $DB_NAME
   echo $USER
   echo $PASSWORD
   
   # For Twitter
   echo $TWITTER_API_KEY
   echo $TWITTER_API_SECRET
   # ... etc
   ```

2. **Test individual MCP servers**:
   ```bash
   # Test Odoo server
   python -c "import sys; exec(open('mcp_servers/odoo_accounting/odoo_mcp.py').read())"
   
   # Test Twitter server
   node mcp_servers/twitter/index.js
   ```

3. **Verify server connectivity**:
   - Ensure Odoo instance is running and accessible
   - Verify API credentials are correct
   - Check firewall/network settings

4. **Common fixes**:
   - Restart MCP servers if they become unresponsive
   - Verify all required environment variables are set
   - Check logs in Logs/ for error details
   - Ensure sufficient system resources are available

### Server Readiness Checks
Before executing tasks that depend on MCP servers:
1. Verify servers are running with `ps aux | grep [server-name]`
2. Test connectivity with simple operations
3. Check Dashboard.md for any reported server issues

## Dashboard
Check `Dashboard.md` for approval logs and system status.
