from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from modules.subdomain_finder import find_subdomains
from modules.dns_lookup import dns_lookup
from modules.breach_checker import check_breach
from modules.shodan_recon import shodan_lookup
from modules.ai_reporter import generate_threat_report
from database import create_tables, get_db, ScanResult
from sqlalchemy.orm import Session
from fastapi import Depends
from modules.pdf_generator import generate_pdf_report
from fastapi.responses import FileResponse
import tempfile
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Initialize FastAPI app
app = FastAPI(
   
    
    title="AutoRecon AI",
    description="AI-Powered Attack Surface Intelligence Platform",
    version="1.0.0"
)

create_tables()

# Allow React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],

)

# Request model
class ScanRequest(BaseModel):
    domain: str


@app.get("/")
def root():
    return {
        "message": "AutoRecon AI is running 🚀",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


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


@app.post("/api/scan")
def scan_domain(request: ScanRequest):
    """Run all OSINT modules without AI report"""
    domain = request.domain.strip().lower()

    if not domain or "." not in domain:
        raise HTTPException(
            status_code=400,
            detail="Invalid domain format. Example: tesla.com"
        )

    print(f"\n[*] Starting full scan for: {domain}")

    try:
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


@app.post("/api/scan/full")
def full_scan_with_report(request: ScanRequest, db: Session = Depends(get_db)):
    """Full scan + AI generated threat report with parallel execution"""
    domain = request.domain.strip().lower()

    if not domain or "." not in domain:
        raise HTTPException(
            status_code=400,
            detail="Invalid domain format. Example: tesla.com"
        )

    print(f"\n[*] Starting FULL AI scan for: {domain}")

    # Check cache first — if scanned in last 24 hours, return cached result
    from datetime import datetime, timedelta
    cached = db.query(ScanResult).filter(
        ScanResult.domain == domain,
        ScanResult.created_at >= datetime.utcnow() - timedelta(hours=24)
    ).order_by(ScanResult.created_at.desc()).first()

    if cached:
        print(f"[+] Cache hit! Returning cached scan for {domain}")
        return {
            "domain": cached.domain,
            "subdomains": cached.subdomains or [],
            "dns_info": cached.dns_info or {},
            "breach_results": cached.breach_results or [],
            "port_scan": cached.port_scan or {},
            "ai_report": cached.ai_report or {},
            "status": "success",
            "cached": True
        }

    try:
        # Run subdomain + DNS in parallel using threads
        print("[*] Running parallel recon modules...")
        with ThreadPoolExecutor(max_workers=4) as executor:
            subdomain_future = executor.submit(find_subdomains, domain)
            dns_future = executor.submit(dns_lookup, domain)

            # Get results
            subdomains = subdomain_future.result()
            dns_info = dns_future.result()

        # Port scan needs IPs from DNS
        print("[*] Running port scan...")
        ips = dns_info.get("ip_addresses", [])
        port_scan = shodan_lookup(domain, ips)

        # Breach checks in parallel
        print("[*] Running parallel breach checks...")
        common_emails = [
            f"admin@{domain}",
            f"info@{domain}",
            f"security@{domain}",
        ]
        with ThreadPoolExecutor(max_workers=3) as executor:
            breach_futures = [executor.submit(check_breach, email) for email in common_emails]
            breach_results = [f.result() for f in breach_futures if f.result()["breached"]]

        # Compile scan data
        scan_data = {
            "domain": domain,
            "subdomains": subdomains,
            "dns_info": dns_info,
            "breach_results": breach_results,
            "port_scan": port_scan,
        }

        # Generate AI report
        print("[*] Generating AI threat report...")
        ai_report = generate_threat_report(scan_data)

        print(f"[+] Full AI scan complete for {domain}!")

        # Save to database
        db_scan = ScanResult(
            domain=domain,
            subdomains=subdomains,
            dns_info=dns_info,
            port_scan=port_scan,
            breach_results=breach_results,
            ai_report=ai_report,
            risk_score=ai_report.get("risk_score", 0)
        )
        db.add(db_scan)
        db.commit()
        print(f"[+] Scan saved to database with ID: {db_scan.id}")

        return {
            **scan_data,
            "ai_report": ai_report,
            "status": "success",
            "cached": False
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Scan failed: {str(e)}"
        )
        
@app.get("/api/history")
def get_scan_history(db: Session = Depends(get_db)):
    """Get all previous scans"""
    scans = db.query(ScanResult).order_by(ScanResult.created_at.desc()).limit(20).all()
    return [
        {
            "id": s.id,
            "domain": s.domain,
            "risk_score": s.risk_score,
            "subdomains_count": len(s.subdomains) if s.subdomains else 0,
            "created_at": s.created_at.isoformat()
        }
        for s in scans
    ]

@app.get("/api/history/{scan_id}")
def get_scan_by_id(scan_id: int, db: Session = Depends(get_db)):
    """Get a specific scan by ID"""
    scan = db.query(ScanResult).filter(ScanResult.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return {
        "id": scan.id,
        "domain": scan.domain,
        "subdomains": scan.subdomains,
        "dns_info": scan.dns_info,
        "port_scan": scan.port_scan,
        "breach_results": scan.breach_results,
        "ai_report": scan.ai_report,
        "risk_score": scan.risk_score,
        "created_at": scan.created_at.isoformat()
    }
    
@app.post("/api/report/pdf")
def generate_pdf(request: ScanRequest, db: Session = Depends(get_db)):
    """Generate PDF report for a domain's latest scan"""
    domain = request.domain.strip().lower()

    # Get latest scan from DB
    scan = db.query(ScanResult).filter(
        ScanResult.domain == domain
    ).order_by(ScanResult.created_at.desc()).first()

    if not scan:
        raise HTTPException(
            status_code=404,
            detail="No scan found for this domain. Run a scan first."
        )

    scan_data = {
        "domain": scan.domain,
        "subdomains": scan.subdomains or [],
        "dns_info": scan.dns_info or {},
        "port_scan": scan.port_scan or {},
        "breach_results": scan.breach_results or [],
        "ai_report": scan.ai_report or {}
    }

    # Generate PDF
    output_path = f"reports/{domain.replace('.', '_')}_report.pdf"
    os.makedirs("reports", exist_ok=True)
    generate_pdf_report(scan_data, output_path)

    return FileResponse(
        output_path,
        media_type="application/pdf",
        filename=f"AutoRecon_{domain}_report.pdf"
    )