from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from modules.subdomain_finder import find_subdomains
from modules.dns_lookup import dns_lookup
from modules.breach_checker import check_breach
from modules.shodan_recon import shodan_lookup

# Initialize FastAPI app
app = FastAPI(
    title="AutoRecon AI",
    description="AI-Powered Attack Surface Intelligence Platform",
    version="1.0.0"
)

# Allow React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model - what the user sends us
class ScanRequest(BaseModel):
    domain: str

# Response model - what we send back
class ScanResponse(BaseModel):
    domain: str
    subdomains: list
    dns_info: dict
    breach_results: list
    port_scan: dict
    status: str

@app.get("/")
def root():
    return {
        "message": "AutoRecon AI is running 🚀",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/scan")
def scan_domain(request: ScanRequest):
    domain = request.domain.strip().lower()
    
    # Basic validation
    if not domain or "." not in domain:
        raise HTTPException(
            status_code=400,
            detail="Invalid domain format. Example: tesla.com"
        )
    
    print(f"\n[*] Starting full scan for: {domain}")
    
    try:
        # Run all OSINT modules
        print("[*] Step 1: Finding subdomains...")
        subdomains = find_subdomains(domain)
        
        print("[*] Step 2: DNS lookup...")
        dns_info = dns_lookup(domain)
        
        print("[*] Step 3: Port scanning...")
        ips = dns_info.get("ip_addresses", [])
        port_scan = shodan_lookup(domain, ips)
        
        print("[*] Step 4: Checking breaches...")
        breach_results = []
        common_emails = [
            f"admin@{domain}",
            f"info@{domain}",
            f"security@{domain}",
        ]
        for email in common_emails:
            result = check_breach(email)
            if result["breached"]:
                breach_results.append(result)
        
        print(f"[+] Scan complete for {domain}!")
        
        return {
            "domain": domain,
            "subdomains": subdomains,
            "dns_info": dns_info,
            "breach_results": breach_results,
            "port_scan": port_scan,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Scan failed: {str(e)}"
        )

@app.get("/api/subdomains/{domain}")
def get_subdomains(domain: str):
    """Get only subdomains for a domain"""
    subdomains = find_subdomains(domain)
    return {
        "domain": domain,
        "count": len(subdomains),
        "subdomains": subdomains
    }

@app.get("/api/dns/{domain}")
def get_dns(domain: str):
    """Get DNS info for a domain"""
    return dns_lookup(domain)