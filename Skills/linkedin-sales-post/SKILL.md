---
name: linkedin-sales-post
description: Generate sales-oriented LinkedIn post drafts about business (e.g., promote products/services). Draft to Plans/LinkedIn_Post_[date].md for approval.
---

# LinkedIn Sales Post Skill

Generate engaging, sales-oriented LinkedIn posts to promote products, services, or business updates.

## Steps

1. **Read Company Handbook**
   - Read `Company_Handbook.md` for brand tone, voice guidelines, and content rules
   - Ensure post aligns with company messaging and values

2. **Generate Engaging Post**
   - Write post between 200-300 characters
   - Include a clear call to action (CTA)
   - Make it conversational and engaging
   - Highlight value proposition or benefit

3. **Add Hashtags & Emojis**
   - Include 3-5 relevant hashtags
   - Add appropriate emojis to increase engagement
   - Keep professional but approachable

4. **Write to Plans Directory**
   - Save draft to `Plans/LinkedIn_Post_[YYYY-MM-DD].md`
   - Include frontmatter:
     ```yaml
     ---
     type: post_draft
     platform: linkedin
     status: pending_approval
     created: [timestamp]
     ---
     ```

5. **Log to Dashboard**
   - Update `Dashboard.md` with new draft entry
   - Include status and file location

## Example Output

```markdown
---
type: post_draft
platform: linkedin
status: pending_approval
created: 2024-01-15 10:30:00
---

# LinkedIn Post Draft

🚀 Excited about our new AI Employee! Automate your biz for $500/mo. Stop drowning in admin tasks and focus on what matters. DM for a free demo! 💼

#AI #Automation #SmallBusiness #Productivity #TechSolutions
```

## Post Guidelines

- **Length:** 200-300 characters (excluding hashtags)
- **Tone:** Professional yet friendly, enthusiastic but not pushy
- **CTA Examples:** "DM for demo", "Link in comments", "Book a call", "Try free today"
- **Hashtag Count:** 3-5 relevant tags
- **Emoji Usage:** 2-4 emojis, placed strategically

## Trigger Phrases

- "Create a LinkedIn post"
- "Write a sales post for LinkedIn"
- "Draft LinkedIn content"
- "Promote [product/service] on LinkedIn"
