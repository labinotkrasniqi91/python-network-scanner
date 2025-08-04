#!/usr/bin/env python3
"""
Test script for the Simple Network Scanner
This script demonstrates basic usage of the network scanner.
"""

import subprocess
import sys
import os

def test_scanner():
    """Test the network scanner with different scenarios."""
    
    print("🧪 Testing Simple Network Scanner")
    print("=" * 50)
    
    # Check if the scanner script exists
    scanner_path = "simple_network_scanner.py"
    if not os.path.exists(scanner_path):
        print(f"❌ Error: {scanner_path} not found!")
        return False
    
    print(f"✅ Found scanner: {scanner_path}")
    
    # Test 1: Help message
    print("\n📋 Test 1: Help message")
    try:
        result = subprocess.run([sys.executable, scanner_path, "--help"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Help message works correctly")
        else:
            print("❌ Help message failed")
    except Exception as e:
        print(f"❌ Error testing help: {e}")
    
    # Test 2: Invalid network
    print("\n📋 Test 2: Invalid network")
    try:
        result = subprocess.run([sys.executable, scanner_path, "-n", "invalid"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print("✅ Correctly rejected invalid network")
        else:
            print("❌ Should have rejected invalid network")
    except Exception as e:
        print(f"❌ Error testing invalid network: {e}")
    
    # Test 3: Localhost scan (safe test)
    print("\n📋 Test 3: Localhost scan")
    try:
        result = subprocess.run([sys.executable, scanner_path, "-n", "127.0.0.1/32", "--host-only"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Localhost scan completed")
            print("Output:")
            print(result.stdout)
        else:
            print("❌ Localhost scan failed")
            print("Error:", result.stderr)
    except Exception as e:
        print(f"❌ Error testing localhost scan: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Scanner Test Complete!")
    print("\nTo use the scanner:")
    print("1. Host discovery: python3 simple_network_scanner.py -n 192.168.1.0/24 --host-only")
    print("2. Full scan: python3 simple_network_scanner.py -n 192.168.1.0/24")
    print("3. Custom ports: python3 simple_network_scanner.py -n 192.168.1.0/24 -p 80,443,8080")
    
    return True

if __name__ == "__main__":
    test_scanner() 