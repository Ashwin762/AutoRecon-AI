import httpx
import os
from dotenv import load_dotenv

load_dotenv()

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
            print("[-] Invalid API key")
            
    except Exception as e:
        print(f"[-] Error: {e}")
    
    return results