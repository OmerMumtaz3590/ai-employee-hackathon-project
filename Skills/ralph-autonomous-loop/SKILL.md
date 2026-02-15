---
name: ralph-autonomous-loop
description: Runs Claude in autonomous loop mode with stop-hook logic for complex multi-step tasks. Continues until task completion or max iterations reached.
---

# Ralph Wiggum Autonomous Loop Skill

## Purpose
Execute complex, multi-step tasks autonomously using Claude in a continuous loop with intelligent stopping conditions. Designed for end-to-end task completion that requires multiple skills and iterations.

## When to Use This Skill
- When processing complex workflows that span multiple systems
- When a task requires multiple skills to complete (e.g., invoice processing from detection to Odoo posting)
- When human oversight is not required for routine complex operations
- When executing multi-step business processes

## Prerequisites
- Claude CLI must be installed and accessible
- Company_Handbook.md must be available
- Relevant skills must be available in Skills/ directory
- Appropriate MCP servers must be running if needed

## Components

### ralph_orchestrator.py
Main orchestrator script that:
- Creates a state/PROMPT.md file with the initial task
- Runs Claude in a loop with context from previous iterations
- Stops when `<promise>TASK_COMPLETE</promise>` is detected
- Limits execution to maximum 20 iterations
- Updates the prompt with context after each iteration

### state/PROMPT.md
Generated file containing the current task context and Claude's instructions

## Usage

### Command Line
```bash
python ralph_orchestrator.py 'Process full invoice flow from WhatsApp to Odoo post'
```

### With Custom Iteration Limit
```bash
python ralph_orchestrator.py --max-iterations 15 'Process client onboarding workflow'
```

## Operation Flow

1. **Initialization**: Creates state/PROMPT.md with the task description
2. **Iteration Loop**: Runs Claude repeatedly with updated context
3. **Context Preservation**: Each iteration includes output from the previous iteration
4. **Completion Detection**: Looks for `<promise>TASK_COMPLETE</promise>` in output
5. **Folder Monitoring**: Checks for activity in Done/ folder as progress indicator
6. **Iteration Limit**: Stops after maximum iterations to prevent infinite loops

## Stopping Conditions

- `<promise>TASK_COMPLETE</promise>` appears in Claude's output
- Maximum iteration count reached (default: 20)
- Error occurs during Claude execution
- Script is manually terminated

## Safety Measures

- Maximum iteration limit prevents infinite loops
- Timeout on each Claude call prevents hanging
- Context updates ensure Claude maintains task awareness
- Error handling for Claude execution failures

## Example Use Cases

- Process invoice from detection in Needs_Action to Odoo posting
- Handle complete customer onboarding workflow
- Execute multi-step marketing campaign
- Perform weekly audit and reporting cycle

## Expected Behavior

Claude will:
- Use available skills as needed
- Update Dashboard.md with progress
- Move files between folders appropriately
- Interact with MCP servers when required
- Continue until the task is fully completed