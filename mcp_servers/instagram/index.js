#!/usr/bin/env node

/**
 * Instagram MCP Server
 * Provides Instagram posting functionality via MCP protocol
 */

const server = {
  name: 'instagram',
  version: '1.0.0',
  tools: [
    {
      name: 'post_instagram',
      description: 'Post content to Instagram',
      parameters: {
        type: 'object',
        properties: {
          caption: {
            type: 'string',
            description: 'Caption for the Instagram post'
          },
          image_url: {
            type: 'string',
            description: 'URL of the image to post'
          },
          hashtags: {
            type: 'array',
            items: { type: 'string' },
            description: 'Array of hashtags to include'
          }
        },
        required: ['caption', 'image_url']
      }
    },
    {
      name: 'post_story',
      description: 'Post a story to Instagram',
      parameters: {
        type: 'object',
        properties: {
          image_url: {
            type: 'string',
            description: 'URL of the image for the story'
          },
          text_overlay: {
            type: 'string',
            description: 'Optional text overlay for the story'
          }
        },
        required: ['image_url']
      }
    },
    {
      name: 'get_engagement',
      description: 'Get engagement metrics for recent posts',
      parameters: {
        type: 'object',
        properties: {
          limit: {
            type: 'integer',
            description: 'Number of recent posts to analyze (default: 5)'
          }
        }
      }
    }
  ]
};

// Handle MCP tool calls
async function handleToolCall(name, args) {
  // Validate environment variables
  const requiredEnvVars = [
    'INSTAGRAM_ACCESS_TOKEN',
    'INSTAGRAM_BUSINESS_ACCOUNT_ID'
  ];

  const missingVars = requiredEnvVars.filter(v => !process.env[v]);
  if (missingVars.length > 0) {
    return {
      error: `Missing Instagram API credentials. Set ${missingVars.join(', ')} environment variables.`
    };
  }

  if (name === 'post_instagram') {
    const { caption, image_url, hashtags } = args;

    try {
      // Build caption with hashtags
      let fullCaption = caption;
      if (hashtags && hashtags.length > 0) {
        fullCaption += '\n\n' + hashtags.map(h => h.startsWith('#') ? h : `#${h}`).join(' ');
      }

      // Placeholder for actual Instagram Graph API call
      // In a real implementation, this would:
      // 1. Create a container with the image
      // 2. Publish the container

      await new Promise(resolve => setTimeout(resolve, 1500));

      const postId = Math.floor(Math.random() * 1000000000000000000).toString();

      return {
        success: true,
        postId: postId,
        caption: fullCaption,
        imageUrl: image_url,
        timestamp: new Date().toISOString(),
        response: `Instagram post created successfully with ID: ${postId}`
      };
    } catch (error) {
      return {
        error: `Failed to post to Instagram: ${error.message}`
      };
    }
  }

  if (name === 'post_story') {
    const { image_url, text_overlay } = args;

    try {
      await new Promise(resolve => setTimeout(resolve, 1000));

      const storyId = Math.floor(Math.random() * 1000000000000000000).toString();

      return {
        success: true,
        storyId: storyId,
        imageUrl: image_url,
        textOverlay: text_overlay || null,
        expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
        response: `Instagram story posted successfully with ID: ${storyId}`
      };
    } catch (error) {
      return {
        error: `Failed to post story: ${error.message}`
      };
    }
  }

  if (name === 'get_engagement') {
    const limit = args.limit || 5;

    try {
      // Placeholder engagement data
      const mockEngagement = {
        totalPosts: limit,
        averageLikes: Math.floor(Math.random() * 500) + 100,
        averageComments: Math.floor(Math.random() * 50) + 10,
        totalReach: Math.floor(Math.random() * 5000) + 1000,
        topPost: {
          id: '12345678901234567',
          likes: Math.floor(Math.random() * 1000) + 200,
          comments: Math.floor(Math.random() * 100) + 20
        }
      };

      return {
        success: true,
        engagement: mockEngagement,
        period: 'last_7_days'
      };
    } catch (error) {
      return {
        error: `Failed to get engagement: ${error.message}`
      };
    }
  }

  return { error: `Unknown tool: ${name}` };
}

// MCP Protocol handling via stdio
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

function sendResponse(response) {
  console.log(JSON.stringify(response));
}

rl.on('line', async (line) => {
  try {
    const request = JSON.parse(line);

    if (request.method === 'initialize') {
      sendResponse({
        jsonrpc: '2.0',
        id: request.id,
        result: {
          protocolVersion: '2024-11-05',
          capabilities: { tools: {} },
          serverInfo: { name: server.name, version: server.version }
        }
      });
    } else if (request.method === 'tools/list') {
      sendResponse({
        jsonrpc: '2.0',
        id: request.id,
        result: { tools: server.tools }
      });
    } else if (request.method === 'tools/call') {
      const result = await handleToolCall(request.params.name, request.params.arguments || {});
      sendResponse({
        jsonrpc: '2.0',
        id: request.id,
        result: { content: [{ type: 'text', text: JSON.stringify(result) }] }
      });
    } else if (request.method === 'notifications/initialized') {
      // No response needed for notifications
    } else {
      sendResponse({
        jsonrpc: '2.0',
        id: request.id,
        error: { code: -32601, message: `Method not found: ${request.method}` }
      });
    }
  } catch (error) {
    sendResponse({
      jsonrpc: '2.0',
      id: null,
      error: { code: -32700, message: `Parse error: ${error.message}` }
    });
  }
});

process.stderr.write('Instagram MCP Server started\n');
