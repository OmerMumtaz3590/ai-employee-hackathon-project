---
name: weekly-ceo-briefing
description: Every Sunday night: audit bank/transactions via Odoo MCP, review Tasks/Done, Business_Goals.md → generate Monday Morning CEO Briefing in Briefings/[date]_Monday_Briefing.md with sections: Executive Summary, Revenue, Completed Tasks, Bottlenecks, Proactive Suggestions. Use templates from Audit_Templates/.
---

# Weekly CEO Briefing Skill

## Purpose
Generate a comprehensive weekly CEO briefing every Sunday night that analyzes business performance, completed tasks, and provides strategic recommendations.

## When to Use This Skill
- Every Sunday night as part of the scheduled audit cycle
- When user requests a CEO briefing
- When business performance analysis is needed

## Prerequisites
- Company_Handbook.md must be available for reference
- Business_Goals.md must be available for goal tracking
- Odoo MCP server must be accessible for financial data
- Done/ folder must contain completed tasks
- Audit_Templates/ directory must contain briefing templates
- Briefings/ directory must exist for output

## Steps

### 1. Data Collection
1. **Read Business_Goals.md** to understand current objectives and targets
2. **Connect to Odoo MCP server** to retrieve:
   - Weekly revenue data
   - Outstanding invoices
   - Recent transactions
   - Account balances
3. **Scan Done/ folder** to identify completed tasks from the week
4. **Check Needs_Action/ and Pending_Approval/** for ongoing items
5. **Review Dashboard.md** for recent activity and issues

### 2. Revenue Analysis
1. **Calculate weekly revenue** using Odoo data:
   - Sum all posted invoices from the past week
   - Include recurring revenue from subscriptions
   - Factor in any one-time payments
2. **Compare to previous weeks** to identify trends
3. **Calculate growth percentage** from previous week/month
4. **Identify largest transactions** and their sources

### 3. Task Completion Review
1. **Count completed tasks** in Done/ folder from the past week
2. **Categorize completed tasks** by type (e.g., client work, internal ops, strategic initiatives)
3. **Match completed tasks** to Business_Goals.md objectives
4. **Highlight significant achievements** that advance business goals

### 4. Bottleneck Identification
1. **Scan pending items** in Needs_Action/ and Pending_Approval/
2. **Identify overdue items** or items pending for extended periods
3. **Note resource constraints** or process inefficiencies observed during the week
4. **Document any system issues** or technical problems encountered
5. **Format bottlenecks** in a table format:
   ```
   | Bottleneck | Impact | Duration | Recommended Action |
   |------------|---------|----------|-------------------|
   | Example    | High    | 3 days   | Resolve X         |
   ```

### 5. Proactive Suggestions
1. **Analyze spending patterns** from Odoo data to identify cost-saving opportunities:
   - Cancel unused subscriptions
   - Renegotiate vendor contracts
   - Consolidate services
2. **Review completed work** for automation opportunities
3. **Assess team capacity** based on completed vs. pending tasks
4. **Identify growth opportunities** based on successful initiatives
5. **Suggest process improvements** based on bottleneck analysis

### 6. Template Application
1. **Load template** from Audit_Templates/ (preferably CEO_briefing_template.md)
2. **Fill template** with collected data and analysis
3. **Apply formatting** consistently across sections

### 7. Briefing Generation
1. **Create file** in Briefings/ with filename: `[YYYY-MM-DD]_Monday_Briefing.md`
2. **Include frontmatter**:
   ```
   ---
   type: ceo_briefing
   date: YYYY-MM-DD
   week_ending: YYYY-MM-DD
   author: AI_Employee
   status: generated
   ---
   ```
3. **Structure briefing** with these sections:
   
   ### Executive Summary
   - Overall business health score (1-10)
   - Key highlights from the week
   - Critical issues requiring attention
   
   ### Revenue
   - Total revenue for the week
   - Comparison to previous week/month
   - Major transactions
   - Outstanding invoices requiring follow-up
   
   ### Completed Tasks
   - Number of tasks completed
   - Key accomplishments
   - Progress toward business goals
   
   ### Bottlenecks
   - Current operational challenges
   - Resource constraints
   - Process inefficiencies
   
   ### Proactive Suggestions
   - Cost-saving opportunities
   - Growth recommendations
   - Process improvements
   - Strategic initiatives to pursue

### 8. Quality Assurance
1. **Use reasoning-loop skill** if complex analysis is required
2. **Verify data accuracy** by cross-referencing multiple sources
3. **Ensure readability** with clear, concise language appropriate for CEO level
4. **Check for completeness** against all required sections

### 9. Logging
1. **Log briefing creation** to Dashboard.md with format:
   `- YYYY-MM-DD HH:MM | Generated CEO Weekly Briefing | [file name] | Success`
2. **Record key metrics** in Dashboard.md for trend tracking

### 10. Follow-up Actions
1. **Schedule reminder** for Monday morning to ensure briefing is reviewed
2. **Flag important items** from the briefing that require immediate attention
3. **Prepare follow-up tasks** based on proactive suggestions

## Error Handling
- If Odoo MCP unavailable: Generate briefing with "Revenue data unavailable" note
- If templates missing: Use default structure from memory
- If Done/ folder empty: Note "No completed tasks this week"
- If Business_Goals.md missing: Proceed with general analysis

## Safety Measures
- Ensure all financial data is accurate before inclusion
- Verify that proactive suggestions align with company values
- Maintain confidentiality of sensitive business information
- Follow Company_Handbook guidelines for reporting

## Schedule Trigger Note
This skill should be triggered every Sunday at 22:00 (10 PM) as part of the weekly audit cycle by the scheduler.py.