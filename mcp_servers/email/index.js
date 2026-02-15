#!/usr/bin/env node

const nodemailer = require('nodemailer');

// MCP Server for Email Sending via Gmail
const server = {
  name: 'email',
  version: '1.0.0',
  tools: [
    {
      name: 'send_email',
      description: 'Send an email via Gmail',
      parameters: {
        type: 'object',
        properties: {
          to: {
            type: 'string',
            description: 'Recipient email address'
          },
          subject: {
            type: 'string',
            description: 'Email subject line'
          },
          body: {
            type: 'string',
            description: 'Email body content'
          }
        },
        required: ['to', 'subject', 'body']
      }
    }
  ]
};

// Create Gmail transporter using environment variables
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.GMAIL_USER,
    pass: process.env.GMAIL_APP_PASSWORD
  }
});

// Handle MCP tool calls
async function handleToolCall(name, args) {
  if (name === 'send_email') {
    const { to, subject, body } = args;

    if (!process.env.GMAIL_USER || !process.env.GMAIL_APP_PASSWORD) {
      return {
        error: 'Missing credentials. Set GMAIL_USER and GMAIL_APP_PASSWORD environment variables.'
      };
    }

    try {
      const mailOptions = {
        from: process.env.GMAIL_USER,
        to: to,
        subject: subject,
        text: body
      };

      const info = await transporter.sendMail(mailOptions);
      return {
        success: true,
        messageId: info.messageId,
        response: `Email sent successfully to ${to}`
      };
    } catch (error) {
      return {
        error: `Failed to send email: ${error.message}`
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
      const result = await handleToolCall(request.params.name, request.params.arguments);
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

process.stderr.write('Email MCP Server started\n');
