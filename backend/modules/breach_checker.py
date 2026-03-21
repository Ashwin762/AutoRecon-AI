import httpx
import os
from dotenv import load_dotenv
from pathlib import Path

# This makes sure .env is found no matter where we run from
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def check_breach(email: str) -> dict:
    print(f"[*] Checking breaches for: {email}")
    
    results = {
        "email": email,
        "breached": False,
        "breach_count": 0,
        "breaches": []
    }
    
    try:
        api_key = os.getenv("HIBP_API_KEY")
        
        headers = {
            "hibp-api-key": api_key,
            "user-agent": "AutoRecon-AI"
        }
        
        # truncateResponse=false gets us FULL breach details
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"
        
        response = httpx.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            breaches = response.json()
            results["breached"] = True
            results["breach_count"] = len(breaches)
            results["breaches"] = [
                {
                    "name": b.get("Name", "Unknown"),
                    "date": b.get("BreachDate", "Unknown"),
                    "data_exposed": b.get("DataClasses", [])
                }
                for b in breaches
            ]
            print(f"[+] Found {len(breaches)} breach(es)!")
            
        elif response.status_code == 404:
            print("[+] No breaches found — clean!")
            
        elif response.status_code == 401:
            print(f"[-] Breach check unavailable for: {email} (API subscription required)")
            
    except Exception as e:
        print(f"[-] Error: {e}")
    
    return results


def check_domain_breaches(domain: str) -> list:
    """Check common employee email patterns for a domain"""
    print(f"[*] Checking domain breaches for: {domain}")
    
    test_emails = [
        f"info@{domain}",
        f"admin@{domain}",
        f"contact@{domain}",
        f"support@{domain}",
        f"security@{domain}",
    ]
    
    all_results = []
    for email in test_emails:
        result = check_breach(email)
        if result["breached"]:
            all_results.append(result)
    
    return all_results