# Simple Network Scanner

A lightweight Python network scanning tool with host discovery and port scanning capabilities. This scanner is designed to work on macOS, Linux, and Windows systems.

## Features

- **Host Discovery**: Find alive hosts in a network using ping
- **Port Scanning**: Scan for open ports on discovered hosts
- **Service Detection**: Identify common services running on open ports
- **Multi-threaded**: Fast scanning using ThreadPoolExecutor
- **Cross-platform**: Works on macOS, Linux, and Windows
- **Configurable**: Customizable timeout and port ranges

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Installation

1. Download the scanner files:
   ```bash
   # The scanner is already created in your home directory
   cd ~
   ls -la *.py
   ```

2. Make the script executable:
   ```bash
   chmod +x simple_network_scanner.py
   ```

## Usage

### Basic Host Discovery

Discover all alive hosts in a network:
```bash
python3 simple_network_scanner.py -n 192.168.1.0/24 --host-only
```

### Full Network Scan

Scan a network for hosts and their open ports:
```bash
python3 simple_network_scanner.py -n 192.168.1.0/24
```

### Custom Port Range

Scan specific ports:
```bash
python3 simple_network_scanner.py -n 192.168.1.0/24 -p 80,443,8080
```

Scan a range of ports:
```bash
python3 simple_network_scanner.py -n 192.168.1.0/24 -p 1-1000
```

### Custom Timeout

Set a custom timeout (in seconds):
```bash
python3 simple_network_scanner.py -n 192.168.1.0/24 -t 2.0
```

## Command Line Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `-n, --network` | Network to scan (required) | `192.168.1.0/24` |
| `-p, --ports` | Ports to scan | `80,443,8080` or `1-1000` |
| `-t, --timeout` | Timeout in seconds | `1.0` |
| `--host-only` | Only discover hosts, don't scan ports | Flag |

## Common Ports Scanned

The scanner checks these common ports by default:

| Port | Service | Port | Service |
|------|---------|------|---------|
| 21 | FTP | 443 | HTTPS |
| 22 | SSH | 993 | IMAPS |
| 23 | Telnet | 995 | POP3S |
| 25 | SMTP | 1433 | MSSQL |
| 53 | DNS | 3306 | MySQL |
| 80 | HTTP | 3389 | RDP |
| 110 | POP3 | 5432 | PostgreSQL |
| 143 | IMAP | 5900 | VNC |
| 6379 | Redis | 8080 | HTTP-Proxy |
| 8443 | HTTPS-Alt |

## Examples

### Example 1: Quick Network Discovery
```bash
python3 simple_network_scanner.py -n 192.168.1.0/24 --host-only
```

Output:
```
[*] Discovering hosts in network: 192.168.1.0/24
[+] Host discovered: 192.168.1.1
[+] Host discovered: 192.168.1.5
[+] Host discovered: 192.168.1.10

[+] Found 3 alive hosts
[+] Total hosts found: 3
```

### Example 2: Full Network Scan
```bash
python3 simple_network_scanner.py -n 192.168.1.0/24
```

Output:
```
[*] Starting network scan: 192.168.1.0/24
[*] Timeout: 1.0 seconds
[*] Start time: 2024-01-15 14:30:25

[*] Discovering hosts in network: 192.168.1.0/24
[+] Host discovered: 192.168.1.1
[+] Host discovered: 192.168.1.5

[+] Found 2 alive hosts

[*] Scanning host: 192.168.1.1
[+] Hostname: router.local
[+] Open port 80/tcp - HTTP
[+] Open port 443/tcp - HTTPS

[*] Scanning host: 192.168.1.5
[+] Open port 22/tcp - SSH
[+] Open port 80/tcp - HTTP

==================================================
SCAN SUMMARY
==================================================

Host: 192.168.1.1
Hostname: router.local
Open ports:
  80/tcp - HTTP
  443/tcp - HTTPS

Host: 192.168.1.5
Open ports:
  22/tcp - SSH
  80/tcp - HTTP

==================================================
Scan completed at: 2024-01-15 14:30:45
```

### Example 3: Custom Port Scan
```bash
python3 simple_network_scanner.py -n 192.168.1.0/24 -p 22,80,443,8080
```

## Security and Legal Considerations

⚠️ **Important**: This tool is for educational and authorized network testing purposes only.

- **Only scan networks you own or have explicit permission to scan**
- **Respect network policies and terms of service**
- **Be aware that port scanning may be detected by security systems**
- **Some networks may block or log scanning activities**

## Troubleshooting

### Permission Denied
If you get permission errors, make sure the script is executable:
```bash
chmod +x simple_network_scanner.py
```

### No Hosts Found
- Check if the network range is correct
- Verify that hosts are actually online
- Try increasing the timeout: `-t 3.0`

### Slow Scanning
- Reduce the number of worker threads in the code
- Increase timeout for better reliability
- Use `--host-only` first to identify alive hosts

## Advanced Usage

### Scanning Large Networks
For large networks, consider scanning in smaller ranges:
```bash
# Scan first 50 hosts
python3 simple_network_scanner.py -n 192.168.1.0/26

# Scan next 50 hosts
python3 simple_network_scanner.py -n 192.168.1.64/26
```

### Custom Port Lists
You can modify the `common_ports` dictionary in the code to add or remove ports:
```python
self.common_ports = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    # Add your custom ports here
    9000: "Custom-Service"
}
```

## Code Structure

The scanner consists of one main class `SimpleNetworkScanner` with methods:

- `ping_host()`: Check if a host is alive
- `scan_port()`: Scan a specific port
- `get_hostname()`: Resolve hostname from IP
- `scan_host()`: Scan all ports on a host
- `discover_hosts()`: Find alive hosts in network
- `scan_network()`: Complete network scan
- `print_summary()`: Display results

## Contributing

Feel free to modify and improve the scanner:

1. Add new port scanning techniques
2. Implement UDP scanning
3. Add banner grabbing capabilities
4. Improve error handling
5. Add output formats (JSON, CSV, etc.)

## License

This tool is provided for educational purposes. Use responsibly and only on networks you own or have permission to test. 
