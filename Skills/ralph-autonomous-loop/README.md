# Ralph Wiggum Autonomous Loop

An autonomous task execution system that runs Claude in a continuous loop with intelligent stopping conditions.

## Overview

The Ralph Wiggum Orchestrator enables complex, multi-step tasks to be executed autonomously by running Claude in a loop with preserved context between iterations. The system continues until the task is complete or a maximum iteration count is reached.

## Features

- Autonomous task execution with Claude
- Context preservation between iterations
- Intelligent stopping conditions
- Configurable maximum iteration count
- Progress monitoring via folder state
- Integration with existing skills and MCP servers

## Requirements

- Python 3.7+
- Claude CLI installed and configured
- Access to the project directory with Company_Handbook.md
- Available skills in the Skills/ directory

## Installation

No special installation required - just ensure Claude CLI is available in your PATH.

## Usage

### Basic Usage
```bash
python ralph_orchestrator.py 'Process full invoice flow from WhatsApp to Odoo post'
```

### With Custom Iteration Limit
```bash
python ralph_orchestrator.py --max-iterations 15 'Process client onboarding workflow'
```

## How It Works

1. Creates a `state/PROMPT.md` file with the initial task description
2. Runs Claude repeatedly, feeding the output of each iteration back as context
3. Continues until `<promise>TASK_COMPLETE</promise>` is detected in the output
4. Stops after reaching the maximum iteration count (default: 20)
5. Updates the prompt with context after each iteration to maintain task awareness

## Stopping Conditions

The loop will stop when:
- `<promise>TASK_COMPLETE</promise>` is found in Claude's output
- The maximum iteration count is reached
- An error occurs during Claude execution
- The script is manually terminated

## Example Tasks

The orchestrator is ideal for complex workflows such as:
- End-to-end invoice processing from detection to payment
- Customer onboarding workflows spanning multiple systems
- Multi-step marketing campaign execution
- Weekly audit and reporting cycles

## Safety Features

- Maximum iteration limit prevents infinite loops
- Timeout on each Claude call prevents hanging
- Error handling for robust operation
- Context updates ensure task continuity