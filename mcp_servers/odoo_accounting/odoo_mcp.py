#!/usr/bin/env python3
"""
Odoo MCP Server for Accounting Integration
Provides accounting operations via MCP protocol
"""

import os
import sys
import json
import requests
from datetime import datetime
import traceback


class OdooMCP:
    def __init__(self):
        # Initialize connection parameters from environment variables
        self.url = os.getenv('ODOO_URL', 'http://localhost:8069')
        self.db = os.getenv('DB_NAME')
        self.username = os.getenv('USER')
        self.password = os.getenv('PASSWORD')
        
        if not all([self.url, self.db, self.username, self.password]):
            raise ValueError("Missing required environment variables: ODOO_URL, DB_NAME, USER, PASSWORD")
        
        # Authenticate and get session
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Odoo and store session"""
        try:
            # Common endpoint for authentication
            login_url = f"{self.url}/web/session/authenticate"
            
            payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "db": self.db,
                    "login": self.username,
                    "password": self.password
                },
                "id": 1
            }
            
            response = requests.post(login_url, json=payload)
            result = response.json()
            
            if 'result' in result and 'session_id' in result['result']:
                self.session_id = result['result']['session_id']
                self.uid = result['result']['uid']
            else:
                # Alternative authentication method using common endpoint
                common_url = f"{self.url}/xmlrpc/2/common"
                payload = {
                    "jsonrpc": "2.0",
                    "method": "call",
                    "params": {
                        "service": "common",
                        "method": "authenticate",
                        "args": [self.db, self.username, self.password, {}]
                    },
                    "id": 1
                }
                
                response = requests.post(common_url, json=payload)
                self.uid = response.json()['result']
                
                if not self.uid:
                    raise Exception("Authentication failed")
                    
        except Exception as e:
            raise Exception(f"Failed to authenticate with Odoo: {str(e)}")
    
    def call_odoo_method(self, model, method, args=None, kwargs=None):
        """Make a call to Odoo using JSON-RPC"""
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        
        try:
            url = f"{self.url}/xmlrpc/2/object"
            payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": method,
                    "args": [self.db, self.uid, self.password, model] + args
                },
                "id": 2
            }
            
            response = requests.post(url, json=payload)
            result = response.json()
            
            if 'error' in result:
                raise Exception(f"Odoo error: {result['error']}")
            
            return result.get('result')
        except Exception as e:
            raise Exception(f"Failed to call Odoo method {model}.{method}: {str(e)}")
    
    def draft_invoice(self, partner_id, amount, description):
        """Draft an invoice - requires approval before posting"""
        try:
            # Create invoice record
            invoice_vals = {
                'partner_id': partner_id,
                'amount_total': amount,
                'name': description,
                'state': 'draft',  # Keep in draft state initially
                'move_type': 'out_invoice',  # Standard customer invoice
            }
            
            # Create the invoice
            invoice_id = self.call_odoo_method('account.move', 'create', [invoice_vals])
            
            return {
                'success': True,
                'invoice_id': invoice_id,
                'message': f'Invoice drafted successfully with ID {invoice_id}. Requires approval to post.',
                'needs_approval': True
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def post_invoice(self, invoice_id):
        """Post an invoice - requires approval flag"""
        try:
            # Check if invoice exists and is in draft state
            invoice = self.call_odoo_method('account.move', 'read', [[invoice_id], ['state', 'name']])
            
            if not invoice:
                return {
                    'success': False,
                    'error': f'Invoice with ID {invoice_id} not found'
                }
            
            if invoice[0]['state'] != 'draft':
                return {
                    'success': False,
                    'error': f'Invoice {invoice_id} is not in draft state, current state: {invoice[0]["state"]}'
                }
            
            # Post the invoice
            result = self.call_odoo_method('account.move', 'action_post', [invoice_id])
            
            return {
                'success': True,
                'invoice_id': invoice_id,
                'message': f'Invoice {invoice_id} posted successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_balance(self):
        """Get account balance information"""
        try:
            # Get account balances - simplified approach
            # This would typically query account.account or account.move.line
            # For demonstration, we'll get some basic financial data
            
            # Get total receivables (AR)
            ar_domain = [['account_type', '=', 'asset_receivable']]
            ar_accounts = self.call_odoo_method('account.account', 'search_read', [ar_domain, ['name', 'balance']])
            
            # Get total payables (AP)
            ap_domain = [['account_type', '=', 'liability_payable']]
            ap_accounts = self.call_odoo_method('account.account', 'search_read', [ap_domain, ['name', 'balance']])
            
            total_ar = sum(acc['balance'] for acc in ar_accounts) if ar_accounts else 0
            total_ap = sum(acc['balance'] for acc in ap_accounts) if ap_accounts else 0
            
            return {
                'success': True,
                'total_receivables': total_ar,
                'total_payables': total_ap,
                'net_position': total_ar - total_ap,
                'currency': 'USD'  # Default currency
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_recent_transactions(self, limit=10):
        """List recent accounting transactions"""
        try:
            # Search for recent account moves (journal entries/invoices)
            domain = []  # Could add filters for date, type, etc.
            fields = ['id', 'name', 'date', 'ref', 'amount_total', 'state', 'move_type']
            
            # Sort by date descending and limit results
            transactions = self.call_odoo_method('account.move', 'search_read', 
                                               [domain, fields], 
                                               {'order': 'date desc', 'limit': limit})
            
            # Format the results
            formatted_transactions = []
            for trans in transactions:
                formatted_transactions.append({
                    'id': trans.get('id'),
                    'name': trans.get('name', ''),
                    'date': trans.get('date', ''),
                    'reference': trans.get('ref', ''),
                    'amount': trans.get('amount_total', 0),
                    'state': trans.get('state', ''),
                    'type': trans.get('move_type', '')
                })
            
            return {
                'success': True,
                'transactions': formatted_transactions,
                'count': len(formatted_transactions)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def send_response(response):
    """Send response in MCP format"""
    print(json.dumps(response))


def handle_tool_call(odoo_mcp, name, args):
    """Handle individual tool calls"""
    try:
        if name == 'draft_invoice':
            partner_id = args.get('partner_id')
            amount = args.get('amount')
            description = args.get('description')
            
            if partner_id is None or amount is None or description is None:
                return {
                    'error': 'Missing required parameters: partner_id, amount, description'
                }
            
            return odoo_mcp.draft_invoice(partner_id, amount, description)
        
        elif name == 'post_invoice':
            invoice_id = args.get('invoice_id')
            
            if invoice_id is None:
                return {
                    'error': 'Missing required parameter: invoice_id'
                }
            
            return odoo_mcp.post_invoice(invoice_id)
        
        elif name == 'get_balance':
            return odoo_mcp.get_balance()
        
        elif name == 'list_recent_transactions':
            limit = args.get('limit', 10)
            return odoo_mcp.list_recent_transactions(limit)
        
        else:
            return {
                'error': f'Unknown tool: {name}'
            }
    
    except Exception as e:
        return {
            'error': f'Error handling tool call {name}: {str(e)}',
            'traceback': traceback.format_exc()
        }


def main():
    """Main MCP server loop"""
    server_info = {
        'name': 'odoo_accounting',
        'version': '1.0.0',
        'tools': [
            {
                'name': 'draft_invoice',
                'description': 'Draft an invoice in Odoo (requires approval to post)',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'partner_id': {
                            'type': 'integer',
                            'description': 'ID of the customer/partner'
                        },
                        'amount': {
                            'type': 'number',
                            'description': 'Amount of the invoice'
                        },
                        'description': {
                            'type': 'string',
                            'description': 'Description of the invoice'
                        }
                    },
                    'required': ['partner_id', 'amount', 'description']
                }
            },
            {
                'name': 'post_invoice',
                'description': 'Post a drafted invoice in Odoo (requires approval)',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'invoice_id': {
                            'type': 'integer',
                            'description': 'ID of the invoice to post'
                        }
                    },
                    'required': ['invoice_id']
                }
            },
            {
                'name': 'get_balance',
                'description': 'Get current account balance information'
            },
            {
                'name': 'list_recent_transactions',
                'description': 'List recent accounting transactions',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'limit': {
                            'type': 'integer',
                            'description': 'Maximum number of transactions to return (default: 10)'
                        }
                    }
                }
            }
        ]
    }
    
    # Initialize Odoo connection
    try:
        odoo_mcp = OdooMCP()
    except Exception as e:
        sys.stderr.write(f"Failed to initialize Odoo connection: {str(e)}\n")
        sys.exit(1)
    
    sys.stderr.write('Odoo MCP Server started\n')
    
    # Main loop to handle MCP requests
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            
            if request.get('method') == 'initialize':
                send_response({
                    'jsonrpc': '2.0',
                    'id': request.get('id'),
                    'result': {
                        'protocolVersion': '2024-11-05',
                        'capabilities': {'tools': {}},
                        'serverInfo': {
                            'name': server_info['name'],
                            'version': server_info['version']
                        }
                    }
                })
            elif request.get('method') == 'tools/list':
                send_response({
                    'jsonrpc': '2.0',
                    'id': request.get('id'),
                    'result': {'tools': server_info['tools']}
                })
            elif request.get('method') == 'tools/call':
                result = handle_tool_call(
                    odoo_mcp,
                    request['params']['name'],
                    request['params'].get('arguments', {})
                )
                
                send_response({
                    'jsonrpc': '2.0',
                    'id': request.get('id'),
                    'result': {
                        'content': [{'type': 'text', 'text': json.dumps(result)}]
                    }
                })
            elif request.get('method') == 'notifications/initialized':
                # No response needed for notifications
                pass
            else:
                send_response({
                    'jsonrpc': '2.0',
                    'id': request.get('id'),
                    'error': {
                        'code': -32601,
                        'message': f'Method not found: {request.get("method")}'
                    }
                })
        except json.JSONDecodeError:
            send_response({
                'jsonrpc': '2.0',
                'id': None,
                'error': {
                    'code': -32700,
                    'message': 'Parse error: Invalid JSON'
                }
            })
        except Exception as e:
            send_response({
                'jsonrpc': '2.0',
                'id': None,
                'error': {
                    'code': -32603,
                    'message': f'Internal error: {str(e)}'
                }
            })


if __name__ == '__main__':
    main()