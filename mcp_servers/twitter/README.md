# Twitter MCP Server

A placeholder MCP (Model Context Protocol) server that simulates Twitter/X posting functionality.

## Overview

This server provides a placeholder implementation for posting tweets to Twitter/X. It validates inputs and simulates the posting process without actually connecting to the Twitter API.

## Environment Variables

The server requires the following environment variables to simulate a real Twitter API connection:

- `TWITTER_API_KEY`: Twitter API key
- `TWITTER_API_SECRET`: Twitter API secret
- `TWITTER_ACCESS_TOKEN`: Twitter access token
- `TWITTER_ACCESS_TOKEN_SECRET`: Twitter access token secret
- `TWITTER_BEARER_TOKEN`: Twitter bearer token

## Available Tools

### `post_tweet(text)`
Posts a tweet to Twitter/X.

Parameters:
- `text`: Text content of the tweet (max 280 characters)

## Limitations

This is a placeholder implementation that:
- Validates tweet length (max 280 characters)
- Simulates API call behavior
- Generates mock tweet IDs
- Does not actually post to Twitter/X

A real implementation would connect to the Twitter API using the provided credentials.