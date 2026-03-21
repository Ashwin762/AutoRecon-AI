import requests

def find_subdomains(domain: str) -> list:
    print(f"[*] Finding subdomains for: {domain}")
    
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    
    try:
        response = requests.get(url, timeout=60)  # increased from 10 to 60
        data = response.json()
        
        subdomains = set()
        for entry in data:
            name = entry["name_value"]
            for sub in name.split("\n"):
                if domain in sub:
                    subdomains.add(sub.strip())
        
        subdomains = sorted(list(subdomains))
        print(f"[+] Found {len(subdomains)} subdomains!")
        return subdomains

    except Exception as e:
        print(f"[-] Error: {e}")
        return []