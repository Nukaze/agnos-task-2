#!/usr/bin/env python3
"""
Kill Symptom Recommendation System Server

This script finds and terminates the server process.
"""

import subprocess
import os
import sys
import psutil

def find_server_process():
    """Find the server process by looking for uvicorn"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and any('uvicorn' in arg for arg in cmdline if arg):
                if 'app:app' in cmdline:
                    return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None

def kill_process_by_pid(pid):
    """Kill process by PID"""
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/PID', str(pid), '/F'], check=True)
        else:  # Linux/Mac
            subprocess.run(['kill', '-9', str(pid)], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("=" * 50)
    print("Kill Symptom Recommendation System Server")
    print("=" * 50)
    
    # Check if PID was provided as argument
    if len(sys.argv) > 1:
        try:
            pid = int(sys.argv[1])
            print(f"Attempting to kill process with PID: {pid}")
            if kill_process_by_pid(pid):
                print(f"✓ Successfully killed process {pid}")
            else:
                print(f"✗ Failed to kill process {pid}")
            return
        except ValueError:
            print("Invalid PID provided")
    
    # Find server process automatically
    print("Searching for server process...")
    proc = find_server_process()
    
    if proc:
        print(f"Found server process:")
        print(f"  PID: {proc.pid}")
        print(f"  Name: {proc.name()}")
        print(f"  Command: {' '.join(proc.cmdline())}")
        
        # Ask for confirmation
        confirm = input("\nKill this process? (y/n): ").strip().lower()
        if confirm == 'y':
            if kill_process_by_pid(proc.pid):
                print(f"✓ Successfully killed server process {proc.pid}")
            else:
                print(f"✗ Failed to kill process {proc.pid}")
        else:
            print("Operation cancelled")
    else:
        print("No server process found")
        print("\nYou can also kill by PID:")
        print("  python kill_server.py <PID>")

if __name__ == "__main__":
    main() 