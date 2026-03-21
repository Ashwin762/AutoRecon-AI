from modules.subdomain_finder import find_subdomains

if __name__ == "__main__":
    domain = "tesla.com"
    results = find_subdomains(domain)
    
    print("\n--- SUBDOMAINS FOUND ---")
    for sub in results:
        print(sub)