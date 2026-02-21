# Facebook MCP Server

MCP server for Facebook Page posting via the Facebook Graph API.

## Prerequisites

1. Facebook Developer Account
2. Facebook Page with admin access
3. Page Access Token with required permissions

## Environment Variables

```bash
FACEBOOK_PAGE_ACCESS_TOKEN=your_page_access_token
FACEBOOK_PAGE_ID=your_page_id
```

## Required Permissions

- `pages_manage_posts` - Create and manage posts
- `pages_read_engagement` - Read engagement metrics
- `pages_read_user_content` - Read user content on page

## Available Tools

### post_facebook
Post content to a Facebook Page.

**Parameters:**
- `content` (required): Text content of the post
- `link` (optional): URL to share with the post
- `image_url` (optional): Image URL to include

### create_poll
Create a poll on the Facebook Page.

**Parameters:**
- `question` (required): Poll question
- `options` (required): Array of 2-4 poll options

### get_page_insights
Get insights and metrics for the page.

**Parameters:**
- `metrics` (optional): Specific metrics to retrieve
- `period` (optional): Time period (day, week, month)

### schedule_post
Schedule a post for later publication.

**Parameters:**
- `content` (required): Text content
- `scheduled_time` (required): ISO 8601 datetime
- `link` (optional): URL to share

## Usage

```bash
node index.js
```

## Notes

- Page Access Tokens expire; use long-lived tokens
- Scheduled posts must be at least 10 minutes in the future
- Some features require Business Manager verification
