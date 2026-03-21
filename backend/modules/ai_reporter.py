import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_threat_report(scan_data: dict) -> dict:
    print(f"[*] Generating AI threat report for: {scan_data['domain']}")
    
    domain = scan_data["domain"]
    subdomains = scan_data.get("subdomains", [])
    dns_info = scan_data.get("dns_info", {})
    port_scan = scan_data.get("port_scan", {})
    breach_results = scan_data.get("breach_results", [])
    
    # Build context for the AI
    prompt = f"""
You are a senior cybersecurity analyst. Analyze this OSINT reconnaissance data 
and generate a professional threat intelligence report.

TARGET: {domain}

RECONNAISSANCE DATA:
===================

1. SUBDOMAINS FOUND: {len(subdomains)} total
   Sample subdomains: {subdomains[:10]}

2. DNS INTELLIGENCE:
   - IP Addresses: {dns_info.get('ip_addresses', [])}
   - Mail Servers: {dns_info.get('mail_servers', [])}
   - Nameservers: {dns_info.get('nameservers', [])}

3. EXPOSED SERVICES & PORTS:
   - Total Open Ports: {port_scan.get('total_open_ports', 0)}
   - Services: {port_scan.get('exposed_services', [])}
   - Vulnerabilities: {port_scan.get('vulnerabilities', [])}

4. DATA BREACH STATUS:
   - Breached accounts found: {len(breach_results)}
   - Details: {breach_results}

Generate a professional threat intelligence report with these sections:

## EXECUTIVE SUMMARY
(2-3 sentences for non-technical management)

## RISK LEVEL
(Critical/High/Medium/Low with justification)

## KEY FINDINGS
(Bullet points of most important discoveries)

## ATTACK VECTORS
(Potential ways an attacker could exploit findings)

## RECOMMENDATIONS
(Specific actionable steps to reduce attack surface)

## TECHNICAL DETAILS
(Deeper technical analysis for security team)

Be specific, professional, and reference actual data from the scan.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert cybersecurity analyst specializing in attack surface management and threat intelligence. Write clear, actionable, professional security reports."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.3  # Lower = more focused, less creative
        )
        
        report_text = response.choices[0].message.content
        
        # Calculate risk score based on findings
        risk_score = calculate_risk_score(scan_data)
        
        print(f"[+] AI report generated successfully!")
        
        return {
            "domain": domain,
            "risk_score": risk_score,
            "report": report_text,
            "stats": {
                "subdomains_found": len(subdomains),
                "open_ports": port_scan.get("total_open_ports", 0),
                "breaches_found": len(breach_results),
                "vulnerabilities": len(port_scan.get("vulnerabilities", []))
            }
        }
        
    except Exception as e:
        print(f"[-] AI report generation failed: {e}")
        return {
            "domain": domain,
            "risk_score": 0,
            "report": f"Report generation failed: {str(e)}",
            "stats": {}
        }


def calculate_risk_score(scan_data: dict) -> int:
    """Calculate a 0-100 risk score based on findings"""
    score = 0
    
    # Subdomains — more exposed surface = higher risk
    subdomain_count = len(scan_data.get("subdomains", []))
    if subdomain_count > 100:
        score += 20
    elif subdomain_count > 50:
        score += 10
    elif subdomain_count > 10:
        score += 5
    
    # Open ports — more open ports = higher risk
    open_ports = scan_data.get("port_scan", {}).get("total_open_ports", 0)
    if open_ports > 10:
        score += 25
    elif open_ports > 5:
        score += 15
    elif open_ports > 0:
        score += 5
    
    # Breaches — any breach = serious risk
    breaches = len(scan_data.get("breach_results", []))
    if breaches > 3:
        score += 35
    elif breaches > 0:
        score += 25
    
    # Vulnerabilities — CVEs found = critical
    vulns = len(scan_data.get("port_scan", {}).get("vulnerabilities", []))
    if vulns > 0:
        score += 20
    
    return min(score, 100)  # Cap at 100