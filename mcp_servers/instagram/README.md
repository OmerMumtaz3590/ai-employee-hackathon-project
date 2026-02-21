# Instagram MCP Server

MCP server for Instagram posting via the Instagram Graph API.

## Prerequisites

1. Facebook Developer Account
2. Instagram Business or Creator Account connected to a Facebook Page
3. Instagram Graph API access token

## Environment Variables

```bash
INSTAGRAM_ACCESS_TOKEN=your_access_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_business_account_id
```

## Available Tools

### post_instagram
Post content to Instagram feed.

**Parameters:**
- `caption` (required): Caption for the post
- `image_url` (required): Public URL of the image to post
- `hashtags` (optional): Array of hashtags to append

### post_story
Post a story to Instagram.

**Parameters:**
- `image_url` (required): Public URL of the image
- `text_overlay` (optional): Text to overlay on the story

### get_engagement
Get engagement metrics for recent posts.

**Parameters:**
- `limit` (optional): Number of posts to analyze (default: 5)

## Usage

```bash
node index.js
```

## Notes

- Image URLs must be publicly accessible
- Stories expire after 24 hours
- Hashtag limit: 30 per post (Instagram enforced)
