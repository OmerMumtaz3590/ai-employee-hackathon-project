# Odoo MCP Server

An MCP (Model Context Protocol) server that integrates with Odoo for accounting operations.

## Overview

This server provides accounting functionality by connecting to an Odoo ERP instance. It supports drafting invoices, posting invoices, checking balances, and viewing recent transactions.

## Environment Variables

The server requires the following environment variables to connect to your Odoo instance:

- `ODOO_URL`: URL of your Odoo instance (default: http://localhost:8069)
- `DB_NAME`: Name of your Odoo database
- `USER`: Username for authentication
- `PASSWORD`: Password for authentication

## Available Tools

### `draft_invoice(partner_id, amount, description)`
Drafts a new invoice in Odoo. The invoice remains in draft state and requires approval before posting.

Parameters:
- `partner_id`: ID of the customer/partner
- `amount`: Amount of the invoice
- `description`: Description of the invoice

### `post_invoice(invoice_id)`
Posts a drafted invoice to make it official. This action requires approval.

Parameters:
- `invoice_id`: ID of the invoice to post

### `get_balance()`
Retrieves current account balance information including receivables, payables, and net position.

### `list_recent_transactions(limit=10)`
Lists recent accounting transactions.

Parameters:
- `limit`: Maximum number of transactions to return (default: 10)

## Security Note

For safety, draft actions are performed automatically, but posting invoices requires an approval flag as per the system's human-in-the-loop workflow.

## Usage

This server is designed to work with the AI Employee system and follows the MCP protocol. It integrates with the human approval workflow for sensitive operations like posting invoices.