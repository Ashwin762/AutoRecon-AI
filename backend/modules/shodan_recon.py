import requests

def shodan_lookup(domain: str, ip_addresses: list) -> dict:
    print(f"[*] Running port & service recon for: {domain}")
    
    results = {
        "domain": domain,
        "exposed_services": [],
        "vulnerabilities": [],
        "total_open_ports": 0
    }
    
    for ip in ip_addresses[:3]:  # Check first 3 IPs
        try:
            print(f"[*] Checking IP: {ip}")
            
            # Shodan InternetDB - completely free, no API key needed!
            response = requests.get(
                f"https://internetdb.shodan.io/{ip}",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Open ports
                ports = data.get("ports", [])
                results["total_open_ports"] += len(ports)
                
                # Services running
                services = data.get("cpes", [])  # CPE = software identifiers
                hostnames = data.get("hostnames", [])
                tags = data.get("tags", [])
                
                exposed_service = {
                    "ip": ip,
                    "open_ports": ports,
                    "hostnames": hostnames,
                    "services": services,
                    "tags": tags
                }
                results["exposed_services"].append(exposed_service)
                print(f"[+] Found {len(ports)} open ports on {ip}")
                
                # Vulnerabilities (CVEs)
                vulns = data.get("vulns", [])
                for vuln in vulns:
                    results["vulnerabilities"].append({
                        "id": vuln,
                        "ip": ip
                    })
                
                if vulns:
                    print(f"[!] Found {len(vulns)} vulnerabilities on {ip}!")
                    
            elif response.status_code == 404:
                print(f"[-] No data found for IP: {ip}")
                
        except Exception as e:
            print(f"[-] Error checking {ip}: {e}")
    
    return results