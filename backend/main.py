from modules.subdomain_finder import find_subdomains
from modules.dns_lookup import dns_lookup
import json

if __name__ == "__main__":
    domain = "tesla.com"
    
    # Test subdomain finder
    # subdomains = find_subdomains(domain)
    # print("\n--- SUBDOMAINS FOUND ---")
    # for sub in subdomains:
    #     print(sub)
    
    # Test DNS lookup
    dns_results = dns_lookup(domain)
    print("\n--- DNS RESULTS ---")
    print(json.dumps(dns_results, indent=2))
    
from modules.breach_checker import check_breach

if __name__ == "__main__":
    # Using HIBP test account
    result = check_breach("account-exists@hibp-integration-tests.com")
    
    import json
    print("\n--- BREACH RESULTS ---")
    print(json.dumps(result, indent=2))