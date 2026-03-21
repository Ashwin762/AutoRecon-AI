import socket
import json

def dns_lookup(domain: str) -> dict:
    print(f"[*] Running DNS lookup for: {domain}")
    
    results = {
        "domain": domain,
        "ip_addresses": [],
        "mail_servers": [],
        "nameservers": []
    }
    
    # Get IP addresses
    try:
        ip_info = socket.getaddrinfo(domain, None)
        ips = list(set([info[4][0] for info in ip_info]))
        results["ip_addresses"] = ips
        print(f"[+] Found {len(ips)} IP address(es)")
    except Exception as e:
        print(f"[-] IP lookup failed: {e}")
    
    # Get mail servers and nameservers using dnspython
    try:
        import dns.resolver
        
        # Mail servers (MX records)
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            results["mail_servers"] = [str(r.exchange) for r in mx_records]
            print(f"[+] Found {len(results['mail_servers'])} mail server(s)")
        except:
            print("[-] No MX records found")
        
        # Nameservers (NS records)
        try:
            ns_records = dns.resolver.resolve(domain, 'NS')
            results["nameservers"] = [str(r) for r in ns_records]
            print(f"[+] Found {len(results['nameservers'])} nameserver(s)")
        except:
            print("[-] No NS records found")
            
    except ImportError:
        print("[-] dnspython not installed")
    
    return results