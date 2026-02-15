#!/usr/bin/env python3
"""
MCP Server Manager
Utility script to start, stop, and check status of MCP servers
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path


def check_environment_variables():
    """Check if required environment variables are set"""
    print("Checking environment variables...")
    
    # Check Odoo variables
    odoo_vars = ['ODOO_URL', 'DB_NAME', 'USER', 'PASSWORD']
    odoo_missing = [var for var in odoo_vars if not os.getenv(var)]
    
    if odoo_missing:
        print(f"⚠️  Missing Odoo environment variables: {', '.join(odoo_missing)}")
        print("   Please set these before starting the Odoo MCP server")
    else:
        print("✅ Odoo environment variables are set")
    
    # Check Twitter variables
    twitter_vars = ['TWITTER_API_KEY', 'TWITTER_API_SECRET', 'TWITTER_ACCESS_TOKEN', 
                   'TWITTER_ACCESS_TOKEN_SECRET', 'TWITTER_BEARER_TOKEN']
    twitter_missing = [var for var in twitter_vars if not os.getenv(var)]
    
    if twitter_missing:
        print(f"⚠️  Missing Twitter environment variables: {', '.join(twitter_missing)}")
        print("   Please set these before starting the Twitter MCP server")
    else:
        print("✅ Twitter environment variables are set")
    
    # Check Email variables
    email_vars = ['GMAIL_USER', 'GMAIL_APP_PASSWORD']
    email_missing = [var for var in email_vars if not os.getenv(var)]
    
    if email_missing:
        print(f"⚠️  Missing Email environment variables: {', '.join(email_missing)}")
        print("   Please set these before starting the Email MCP server")
    else:
        print("✅ Email environment variables are set")


def start_mcp_server(server_name, command, args):
    """Start an MCP server"""
    try:
        full_command = [command] + args
        print(f"Starting {server_name} server...")
        print(f"Command: {' '.join(full_command)}")
        
        # Start the process
        process = subprocess.Popen(full_command)
        
        # Give it a moment to start
        time.sleep(2)
        
        # Check if it's still running
        if process.poll() is None:
            print(f"✅ {server_name} server started successfully (PID: {process.pid})")
            return process
        else:
            print(f"❌ {server_name} server failed to start")
            return None
    except Exception as e:
        print(f"❌ Error starting {server_name} server: {e}")
        return None


def check_server_status(server_name, port_or_process_name):
    """Check if a server is running"""
    try:
        # This is a simplified check - in a real system, you might ping the server
        result = subprocess.run(['tasklist'], capture_output=True, text=True)
        if server_name.lower() in result.stdout.lower():
            print(f"✅ {server_name} server is running")
            return True
        else:
            print(f"❌ {server_name} server is not running")
            return False
    except:
        # Fallback for non-Windows systems
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            if server_name.lower() in result.stdout.lower():
                print(f"✅ {server_name} server is running")
                return True
            else:
                print(f"❌ {server_name} server is not running")
                return False
        except:
            print(f"? Could not check {server_name} server status")
            return None


def main():
    print("=" * 50)
    print("MCP SERVER MANAGER")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python mcp_manager.py check    # Check all server statuses")
        print("  python mcp_manager.py start    # Start all servers")
        print("  python mcp_manager.py env      # Check environment variables")
        print("  python mcp_manager.py [server] # Check specific server (odoo, twitter, email)")
        return
    
    action = sys.argv[1].lower()
    
    if action == 'env':
        check_environment_variables()
    elif action == 'check':
        print("\nChecking server statuses...")
        check_server_status("Odoo", "odoo_mcp.py")
        check_server_status("Twitter", "index.js")
        check_server_status("Email", "email/index.js")
    elif action == 'start':
        print("\nChecking environment variables...")
        check_environment_variables()
        
        print("\nStarting MCP servers...")
        servers_started = 0
        
        # Start Odoo server
        odoo_process = start_mcp_server(
            "Odoo", 
            "python", 
            ["mcp_servers/odoo_accounting/odoo_mcp.py"]
        )
        if odoo_process:
            servers_started += 1
        
        # Start Twitter server
        twitter_process = start_mcp_server(
            "Twitter", 
            "node", 
            ["mcp_servers/twitter/index.js"]
        )
        if twitter_process:
            servers_started += 1
        
        # Start Email server
        email_process = start_mcp_server(
            "Email", 
            "node", 
            ["mcp_servers/email/index.js"]
        )
        if email_process:
            servers_started += 1
        
        print(f"\n✅ Started {servers_started} MCP servers")
        print("\nServers are now running in the background.")
        print("Press Ctrl+C to stop all servers.")
        
        try:
            # Keep the script running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping MCP servers...")
            if 'odoo_process' in locals() and odoo_process:
                odoo_process.terminate()
            if 'twitter_process' in locals() and twitter_process:
                twitter_process.terminate()
            if 'email_process' in locals() and email_process:
                email_process.terminate()
            print("All MCP servers stopped.")
    elif action in ['odoo', 'twitter', 'email']:
        print(f"\nChecking {action.capitalize()} server...")
        check_server_status(action.capitalize(), f"{action}*")
    else:
        print(f"Unknown action: {action}")
        print("Use 'check', 'start', 'env', or specific server name (odoo, twitter, email)")


if __name__ == "__main__":
    main()