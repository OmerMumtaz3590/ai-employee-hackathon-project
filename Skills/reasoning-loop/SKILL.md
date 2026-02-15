---
name: reasoning-loop
description: Create Plan.md files via iterative reasoning. Loop until task complete or max 5 iterations.
---

# Reasoning Loop Skill

## Purpose
Implements an iterative reasoning process to break down tasks into actionable plans with progress tracking.

## Input
- Task description (required)

## Process

### Loop (max 5 iterations):

1. **Read Current State**
   - Check existing Plan_[task_id].md for current status
   - Identify items marked as `Needs_Action`

2. **Think Step-by-Step**
   - Analyze the task requirements
   - Break down into logical sub-steps
   - Consider dependencies between steps

3. **Create/Update Plan**
   - Create or update `Plan_[task_id].md` in `/Plans/` directory
   - Use checkbox format for tracking:
     ```
     - [ ] Step 1: Description
     - [ ] Step 2: Description
     - [x] Step 3: Completed step
     ```

4. **Check Completion**
   - Verify if all checkboxes are checked
   - If all complete → mark task as done
   - If incomplete → continue to next iteration

5. **Iterate**
   - If not done and iterations < 5, repeat from step 1
   - Execute pending steps where possible

6. **Log Progress**
   - Update `Dashboard.md` with iteration count and status
   - Record timestamps and progress notes

## Completion
- When all steps are checked: move related files to `/Done/` folder
- Update Dashboard.md with final status

## Constraints
- Maximum iterations: 5
- If max reached without completion, log warning and pause for user input

## Output
- Plan_[task_id].md with tracked progress
- Updated Dashboard.md
- Files moved to Done folder on completion
