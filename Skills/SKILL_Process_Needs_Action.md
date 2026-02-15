# SKILL: Process Needs Action Folder

## Description
Core skill for handling new items dropped into /Needs_Action

## Steps to follow (in order):
1. List all .md files in /Needs_Action
2. For each file:
   a. Read full content
   b. Determine type (from frontmatter: email, message, file_drop, etc.)
   c. Check against Company_Handbook.md rules
   d. Decide: simple action? complex? money-related? sensitive?
   e. If simple → execute logic, log result to Dashboard.md → move file to /Done/
   f. If complex/money/sensitive/new contact → append to 'Needs Human Review' in Dashboard.md → do NOT act → move file to /Done/ after logging
   g. Always append log line to Dashboard.md → format: '- YYYY-MM-DD HH:MM | Processed [filename] → [short result]'
3. If no files → append to Dashboard.md: '- Checked Needs_Action: empty'
4. Be conservative — default to human review when in doubt

## Usage
Invoke this skill whenever Needs_Action has new content.
