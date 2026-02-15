"""
Ralph Wiggum Orchestrator
Autonomous loop that runs Claude with stop-hook logic for complex task execution
Based on the concept from github.com/anthropics/claude-code/plugins/ralph-wiggum
"""

import os
import sys
import subprocess
import time
import argparse
from pathlib import Path


def ensure_state_directory():
    """Create state directory if it doesn't exist"""
    state_dir = Path("state")
    state_dir.mkdir(exist_ok=True)
    return state_dir


def create_prompt_file(task_description, state_dir):
    """Create the initial PROMPT.md file with the task description"""
    prompt_content = f"""# Autonomous Task Execution

## Task Description
{task_description}

## Instructions
You are an autonomous AI employee. Execute this task by:
1. Reading the Company_Handbook.md to understand rules and procedures
2. Identifying the current state of the task
3. Taking appropriate actions based on the situation
4. Updating your progress in Dashboard.md
5. Using available skills as needed
6. Continuing until the task is complete

## Available Skills
- process-needs-action
- human-approval
- update-dashboard
- safety-check
- reasoning-loop
- odoo-accounting
- social-multi-post
- weekly-ceo-briefing

## Current State
Begin execution of the assigned task. Monitor folders like Needs_Action/, Pending_Approval/, and others as appropriate for your task.

## Completion Condition
Mark the task as complete when all sub-tasks are finished and files are moved to the Done/ folder. Respond with <promise>TASK_COMPLETE</promise> when done.
"""
    
    prompt_file = state_dir / "PROMPT.md"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt_content)
    
    return prompt_file


def run_claude_iteration(prompt_file_path):
    """Run a single iteration of Claude with the current prompt"""
    try:
        # Run Claude with the prompt file
        cmd = f'claude "{prompt_file_path}"'
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout per iteration
        )
        
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Claude iteration timed out", 1
    except Exception as e:
        return "", f"Error running Claude: {str(e)}", 1


def check_completion(output):
    """Check if the task is complete based on the output"""
    return "<promise>TASK_COMPLETE</promise>" in output


def check_done_folder():
    """Check if the Done/ folder has new content indicating progress"""
    done_dir = Path("Done")
    if not done_dir.exists():
        return False
    
    # Check if there are files in Done/ that weren't there before
    files = list(done_dir.glob("*"))
    return len(files) > 0


def update_prompt_with_context(prompt_file, iteration, output):
    """Update the prompt file with context from the previous iteration"""
    with open(prompt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add the previous output as context for the next iteration
    updated_content = f"""# Autonomous Task Execution - Iteration {iteration}

## Previous Output
{output}

## Task Description
{content.split('## Task Description')[1].split('## Instructions')[0].strip()}

## Instructions
You are an autonomous AI employee. Continue executing this task by:
1. Reading the Company_Handbook.md to understand rules and procedures
2. Identifying the current state of the task
3. Taking appropriate actions based on the situation
4. Updating your progress in Dashboard.md
5. Using available skills as needed
6. Continuing until the task is complete

## Available Skills
- process-needs-action
- human-approval
- update-dashboard
- safety-check
- reasoning-loop
- odoo-accounting
- social-multi-post
- weekly-ceo-briefing

## Current State
Previous iteration produced the output above. Assess the current state and continue execution. Monitor folders like Needs_Action/, Pending_Approval/, and others as appropriate for your task.

## Completion Condition
Mark the task as complete when all sub-tasks are finished and files are moved to the Done/ folder. Respond with <promise>TASK_COMPLETE</promise> when done.
"""
    
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)


def main():
    parser = argparse.ArgumentParser(description='Ralph Wiggum Orchestrator - Autonomous Claude Loop')
    parser.add_argument('task', nargs='*', help='Task description to execute')
    parser.add_argument('--max-iterations', type=int, default=20, help='Maximum number of iterations (default: 20)')
    
    args = parser.parse_args()
    
    if not args.task:
        print("Usage: python ralph_orchestrator.py 'Task description'")
        sys.exit(1)
    
    task_description = ' '.join(args.task)
    
    print("=" * 60)
    print("RALPH WIGGUM ORCHESTRATOR")
    print(f"Task: {task_description}")
    print(f"Max iterations: {args.max_iterations}")
    print("=" * 60)
    
    # Create state directory and initial prompt
    state_dir = ensure_state_directory()
    prompt_file = create_prompt_file(task_description, state_dir)
    
    print(f"Created prompt file: {prompt_file}")
    
    # Main loop
    for iteration in range(1, args.max_iterations + 1):
        print(f"\n--- ITERATION {iteration} ---")
        
        # Run Claude iteration
        print("Running Claude iteration...")
        stdout, stderr, returncode = run_claude_iteration(prompt_file)
        
        if returncode != 0:
            print(f"Error in iteration {iteration}: {stderr}")
            continue
        
        print(f"Output received ({len(stdout)} chars)")
        
        # Check for completion
        if check_completion(stdout):
            print("\n✅ TASK COMPLETED - Completion promise detected!")
            print("Exiting loop as requested.")
            break
        
        # Check if Done/ folder has activity
        if check_done_folder():
            print("✅ ACTIVITY DETECTED IN DONE FOLDER")
            # Still continue the loop as the task might not be fully complete
        
        # Update prompt with context for next iteration
        update_prompt_with_context(prompt_file, iteration + 1, stdout)
        
        print(f"Iteration {iteration} completed. Preparing next iteration...")
        
        # Small delay between iterations
        time.sleep(2)
    else:
        # This runs if the loop completed without hitting the break
        print(f"\n⚠️  MAX ITERATIONS REACHED ({args.max_iterations})")
        print("Task may not be fully completed.")
    
    print("\n" + "=" * 60)
    print("RALPH WIGGUM ORCHESTRATOR COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()