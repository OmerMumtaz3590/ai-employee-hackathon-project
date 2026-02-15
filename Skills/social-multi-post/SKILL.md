---
name: social-multi-post
description: Draft and schedule posts to Facebook, Instagram, Twitter/X via respective MCP servers (assume mcp_servers/facebook, instagram, twitter exist or use browser-mcp). Generate summary after posting.
---

# Multi-Platform Social Posting Skill

## Purpose
Draft, schedule, and post content across multiple social platforms (Facebook, Instagram, Twitter/X) with platform-specific optimizations and post-performance tracking.

## When to Use This Skill
- When creating social media content based on Business_Goals.md
- When user requests cross-platform social posting
- When executing scheduled social media campaigns
- When updating company social presence

## Prerequisites
- Company_Handbook.md must be available for reference
- Business_Goals.md must be available for content ideas
- MCP servers for each platform must be configured (facebook, instagram, twitter)
- Social_Drafts/ and Social_Summaries/ directories must exist

## Steps

### 1. Content Analysis
1. **Read Business_Goals.md** to understand current marketing objectives
2. **Analyze input** from user prompt or Business_Goals.md
3. **Identify key message** and target audience
4. **Apply safety-check skill** to ensure content complies with guidelines

### 2. Platform-Specific Drafting
1. **Create tailored content** for each platform:
   - **Twitter/X**: Short, punchy text (under 280 chars), trending hashtags, engaging question
   - **Instagram**: Visual-focused, longer captions with emojis, story hooks, relevant hashtags
   - **Facebook**: Balanced text and visuals, detailed information, community-focused
2. **Optimize for platform specs**:
   - Character limits
   - Image/video dimensions
   - Best posting times
   - Hashtag limits

### 3. Draft Creation
1. **Write draft to Social_Drafts/** with filenames:
   - `twitter_[YYYYMMDD_HHMM]_[topic].md`
   - `instagram_[YYYYMMDD_HHMM]_[topic].md`
   - `facebook_[YYYYMMDD_HHMM]_[topic].md`
2. **Include frontmatter**:
   ```
   ---
   type: social_draft
   platform: [twitter|instagram|facebook]
   topic: "[brief topic description]"
   created: "[YYYY-MM-DD HH:MM]"
   scheduled: "[YYYY-MM-DD HH:MM]" (optional)
   status: pending
   ---
   ```
3. **Structure draft** with:
   - Main content
   - Suggested hashtags
   - Alt text for images (where applicable)
   - Call-to-action

### 4. Risk Assessment & Approval
1. **Evaluate risk level** based on:
   - Content sensitivity
   - Brand alignment
   - Potential controversy
   - Company_Handbook guidelines
2. **For low-risk content**:
   - Use MCP to send directly if approved
   - Log action to Dashboard.md
3. **For medium/high-risk content**:
   - Create approval request in Pending_Approval/
   - Filename: `SOCIAL_POST_APPROVAL_[platform]_[YYYYMMDD].md`
   - Include frontmatter with action details
   - Wait for approval before posting

### 5. Posting Execution
1. **Use appropriate MCP server** for each platform:
   - `mcp_servers/twitter` for Twitter/X
   - `mcp_servers/instagram` for Instagram
   - `mcp_servers/facebook` for Facebook
2. **Call platform-specific endpoints**:
   - `post_tweet(content, hashtags, media_url)`
   - `post_instagram(caption, image_url, hashtags)`
   - `post_facebook(content, link, image_url)`
3. **Handle responses** appropriately:
   - Success: Log and proceed
   - Error: Queue for retry or escalate

### 6. Post-Activity Summary
1. **Generate performance summary**:
   - If platform provides analytics endpoint, call it
   - Otherwise, use reasoning-loop to generate summary
2. **Create summary file** in Social_Summaries/ with filename:
   - `summary_[platform]_[YYYYMMDD].md`
3. **Include in summary**:
   - Post content and timing
   - Engagement metrics (reach, likes, shares, comments)
   - Performance against goals
   - Recommendations for future posts

### 7. Logging & Tracking
1. **Log all activities** to Dashboard.md with format:
   `- [YYYY-MM-DD HH:MM] | Posted to [platform] | [brief description] | [status]`
2. **Track engagement** with placeholders for:
   - Reach: [TBD]
   - Impressions: [TBD]
   - Likes: [TBD]
   - Shares: [TBD]
   - Comments: [TBD]
   - Click-through rate: [TBD]

## Platform-Specific Guidelines

### Twitter/X
- Keep text under 280 characters
- Use 1-2 relevant hashtags
- Include engaging question or call-to-action
- Optimize for mobile viewing

### Instagram
- Focus on visual appeal
- Use 5-10 relevant hashtags
- Include alt text for accessibility
- Consider carousel or story formats

### Facebook
- Provide more detailed information
- Include relevant links
- Encourage community discussion
- Use Facebook-specific features (polls, etc.)

## Error Handling
- If MCP server unavailable, queue post for retry
- If content violates platform policies, revise and resubmit
- If approval is denied, archive draft and log reason
- For technical errors, log to Dashboard.md and notify administrator

## Safety Measures
- Always run safety-check skill before posting
- Verify content aligns with Company_Handbook
- Respect platform-specific community guidelines
- Maintain brand consistency across platforms