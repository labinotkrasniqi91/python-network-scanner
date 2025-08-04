#!/usr/bin/env python3
"""
Simple Network Scanner for macOS
A lightweight network scanning tool with host discovery and port scanning.
"""

import socket
import ipaddress
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import subprocess
import platform

class SimpleNetworkScanner:
    def __init__(self, timeout=1):
        self.timeout = timeout
        self.common_ports = {
            21: "FTP",
            22: "SSH", 
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            993: "IMAPS",
            995: "POP3S",
            1433: "MSSQL",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            5900: "VNC",
            6379: "Redis",
            8080: "HTTP-Proxy",
            8443: "HTTPS-Alt"
        }
    
    def ping_host(self, ip):
        """Ping a host to check if it's alive using system ping command."""
        try:
            # Use system ping command for better compatibility
            if platform.system().lower() == "darwin":  # macOS
                result = subprocess.run(['ping', '-c', '1', '-t', str(self.timeout), ip], 
                                      capture_output=True, text=True, timeout=self.timeout + 1)
            else:  # Linux/Windows
                result = subprocess.run(['ping', '-c', '1', '-W', str(self.timeout), ip], 
                                      capture_output=True, text=True, timeout=self.timeout + 1)
            
            return result.returncode == 0
        except:
            return False
    
    def scan_port(self, ip, port):
        """Scan a specific port on a host."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            
            if result == 0:
                service = self.common_ports.get(port, "Unknown")
                return port, service
            return None
        except:
            return None
    
    def get_hostname(self, ip):
        """Try to get the hostname for an IP address."""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return None
    
    def scan_host(self, ip, ports=None):
        """Scan a single host for open ports."""
        if ports is None:
            ports = list(self.common_ports.keys())
        
        print(f"\n[*] Scanning host: {ip}")
        
        # Get hostname if available
        hostname = self.get_hostname(ip)
        if hostname:
            print(f"[+] Hostname: {hostname}")
        
        open_ports = []
        
        # Use ThreadPoolExecutor for faster port scanning
        with ThreadPoolExecutor(max_workers=50) as executor:
            future_to_port = {executor.submit(self.scan_port, ip, port): port for port in ports}
            
            for future in future_to_port:
                result = future.result()
                if result:
                    port, service = result
                    open_ports.append((port, service))
                    print(f"[+] Open port {port}/tcp - {service}")
        
        if not open_ports:
            print(f"[!] No open ports found on {ip}")
        
        return open_ports
    
    def discover_hosts(self, network):
        """Discover alive hosts in a network."""
        print(f"[*] Discovering hosts in network: {network}")
        
        alive_hosts = []
        network_obj = ipaddress.IPv4Network(network, strict=False)
        
        # Use ThreadPoolExecutor for faster host discovery
        with ThreadPoolExecutor(max_workers=50) as executor:
            future_to_ip = {executor.submit(self.ping_host, str(ip)): str(ip) for ip in network_obj.hosts()}
            
            for future in future_to_ip:
                ip = future_to_ip[future]
                if future.result():
                    alive_hosts.append(ip)
                    print(f"[+] Host discovered: {ip}")
        
        print(f"\n[+] Found {len(alive_hosts)} alive hosts")
        return alive_hosts
    
    def scan_network(self, network, ports=None):
        """Scan an entire network for hosts and open ports."""
        print(f"[*] Starting network scan: {network}")
        print(f"[*] Timeout: {self.timeout} seconds")
        print(f"[*] Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Discover alive hosts
        alive_hosts = self.discover_hosts(network)
        
        if not alive_hosts:
            print("[!] No hosts found in the network")
            return
        
        # Scan each alive host
        results = {}
        for host in alive_hosts:
            open_ports = self.scan_host(host, ports)
            results[host] = open_ports
        
        # Print summary
        self.print_summary(results)
    
    def print_summary(self, results):
        """Print a summary of the scan results."""
        print("\n" + "="*50)
        print("SCAN SUMMARY")
        print("="*50)
        
        for host, ports in results.items():
            hostname = self.get_hostname(host)
            print(f"\nHost: {host}")
            if hostname:
                print(f"Hostname: {hostname}")
            
            if ports:
                print("Open ports:")
                for port, service in ports:
                    print(f"  {port}/tcp - {service}")
            else:
                print("  No open ports found")
        
        print("\n" + "="*50)
        print(f"Scan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    parser = argparse.ArgumentParser(description="Simple Network Scanner")
    parser.add_argument("-n", "--network", required=True, 
                       help="Network to scan (e.g., 192.168.1.0/24)")
    parser.add_argument("-p", "--ports", 
                       help="Ports to scan (e.g., 80,443,8080 or 1-1000)")
    parser.add_argument("-t", "--timeout", type=float, default=1.0,
                       help="Timeout in seconds (default: 1.0)")
    parser.add_argument("--host-only", action="store_true",
                       help="Only discover hosts, don't scan ports")
    
    args = parser.parse_args()
    
    # Validate network
    try:
        network_obj = ipaddress.IPv4Network(args.network, strict=False)
    except ValueError as e:
        print(f"[!] Invalid network: {e}")
        sys.exit(1)
    
    # Parse ports
    ports = None
    if args.ports:
        try:
            if "-" in args.ports:
                # Range of ports
                start, end = map(int, args.ports.split("-"))
                ports = list(range(start, end + 1))
            else:
                # Specific ports
                ports = [int(p) for p in args.ports.split(",")]
        except ValueError:
            print("[!] Invalid port specification")
            sys.exit(1)
    
    # Create scanner and start scanning
    scanner = SimpleNetworkScanner(timeout=args.timeout)
    
    if args.host_only:
        # Only discover hosts
        alive_hosts = scanner.discover_hosts(args.network)
        print(f"\n[+] Total hosts found: {len(alive_hosts)}")
    else:
        # Full network scan
        scanner.scan_network(args.network, ports)

if __name__ == "__main__":
    main() 