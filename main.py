import whois
import time
import csv
import threading
import queue
import os
import glob
import socket
import dns.resolver
import requests
import re
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_domain_names_from_folder(folder_path="input/domain_name"):
    """Load domain names from all text files in the specified folder."""
    all_names = []
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} does not exist")
        return []
    
    # Find all .txt files in the folder
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    
    if not txt_files:
        print(f"No .txt files found in {folder_path}")
        return []
    
    print(f"Found {len(txt_files)} domain name file(s) in {folder_path}")
    
    for file_path in txt_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                names = [line.strip() for line in f if line.strip()]
                all_names.extend(names)
                print(f"  Loaded {len(names)} domain names from {os.path.basename(file_path)}")
        except Exception as e:
            print(f"  Error reading {file_path}: {e}")
    
    # Remove duplicates while preserving order
    unique_names = []
    seen = set()
    for name in all_names:
        if name not in seen:
            unique_names.append(name)
            seen.add(name)
    
    print(f"Total unique domain names loaded: {len(unique_names)}")
    return unique_names

def load_tlds_from_folder(folder_path="input/top_level_domain"):
    """Load TLDs from all text files in the specified folder."""
    all_tlds = []
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} does not exist")
        return []
    
    # Find all .txt files in the folder
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    
    if not txt_files:
        print(f"No .txt files found in {folder_path}")
        return []
    
    print(f"Found {len(txt_files)} TLD file(s) in {folder_path}")
    
    for file_path in txt_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tlds = [line.strip() for line in f if line.strip()]
                all_tlds.extend(tlds)
                print(f"  Loaded {len(tlds)} TLDs from {os.path.basename(file_path)}")
        except Exception as e:
            print(f"  Error reading {file_path}: {e}")
    
    # Remove duplicates while preserving order
    unique_tlds = []
    seen = set()
    for tld in all_tlds:
        if tld not in seen:
            unique_tlds.append(tld)
            seen.add(tld)
    
    print(f"Total unique TLDs loaded: {len(unique_tlds)}")
    return unique_tlds

def check_dns_exists(domain):
    """
    Check if domain has DNS records (A, AAAA, MX, NS records).
    Returns tuple: (has_dns, dns_details)
    """
    dns_details = {
        'A': False,
        'AAAA': False,
        'MX': False,
        'NS': False,
        'CNAME': False,
        'SOA': False
    }
    
    has_any_dns = False
    
    # Check for A records (IPv4 - most common for websites)
    try:
        dns.resolver.resolve(domain, 'A')
        dns_details['A'] = True
        has_any_dns = True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.Timeout):
        pass
    
    # Check for AAAA records (IPv6)
    try:
        dns.resolver.resolve(domain, 'AAAA')
        dns_details['AAAA'] = True
        has_any_dns = True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.Timeout):
        pass
    
    # Check for MX records (email servers - strong indicator domain is in use)
    try:
        dns.resolver.resolve(domain, 'MX')
        dns_details['MX'] = True
        has_any_dns = True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.Timeout):
        pass
    
    # Check for NS records (nameservers - indicates domain is configured)
    try:
        dns.resolver.resolve(domain, 'NS')
        dns_details['NS'] = True
        has_any_dns = True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.Timeout):
        pass
    
    # Check for CNAME records
    try:
        dns.resolver.resolve(domain, 'CNAME')
        dns_details['CNAME'] = True
        has_any_dns = True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.Timeout):
        pass
    
    # Check for SOA records (Start of Authority - indicates DNS zone exists)
    try:
        dns.resolver.resolve(domain, 'SOA')
        dns_details['SOA'] = True
        has_any_dns = True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.Timeout):
        pass
    
    return has_any_dns, dns_details

def check_http_response(domain):
    """
    Check if domain responds to HTTP/HTTPS requests.
    This helps identify domains that are actively being used.
    """
    for protocol in ['https', 'http']:
        try:
            url = f"{protocol}://{domain}"
            response = requests.head(url, timeout=5, allow_redirects=True)
            return True  # Domain responds to HTTP
        except:
            pass
    return False

def advanced_whois_check(domain):
    """
    Perform advanced WHOIS check with multiple verification methods.
    Returns: (is_available, confidence_level, details)
    """
    try:
        time.sleep(0.3)  # Rate limiting
        w = whois.whois(domain)
        
        # Check multiple indicators
        has_domain_name = bool(w.domain_name)
        has_registrar = bool(w.registrar) if hasattr(w, 'registrar') else False
        has_creation_date = bool(w.creation_date) if hasattr(w, 'creation_date') else False
        has_expiration_date = bool(w.expiration_date) if hasattr(w, 'expiration_date') else False
        has_name_servers = bool(w.name_servers) if hasattr(w, 'name_servers') else False
        
        # Strong indicators that domain is TAKEN
        if has_domain_name or has_registrar or has_creation_date:
            return False, 'HIGH', {
                'domain_name': has_domain_name,
                'registrar': has_registrar,
                'creation_date': has_creation_date,
                'expiration_date': has_expiration_date,
                'name_servers': has_name_servers
            }
        
        # If no clear indicators, likely available
        return True, 'MEDIUM', {}
        
    except Exception as e:
        error_str = str(e).lower()
        
        # Strong indicators domain is AVAILABLE
        if any(phrase in error_str for phrase in [
            'domain not found',
            'no match',
            'not found',
            'no entries found',
            'no data found',
            'status: free',
            'no match for',
            'not registered',
            'available for registration'
        ]):
            return True, 'HIGH', {'whois_message': 'Domain not found'}
        
        # If we can't determine, be conservative
        return False, 'LOW', {'error': str(e)[:100]}
    
    return True, 'MEDIUM', {}

def check_namecheap_availability(domain):
    """
    Check domain availability via Namecheap API.
    Returns: 'AVAILABLE', 'TAKEN', 'PREMIUM', 'RESTRICTED', or 'ERROR'
    
    Requires environment variables:
    - NAMECHEAP_API_KEY
    - NAMECHEAP_API_USER
    - NAMECHEAP_USERNAME
    - NAMECHEAP_CLIENT_IP
    """
    try:
        # Get API credentials from environment
        api_key = os.getenv('NAMECHEAP_API_KEY')
        api_user = os.getenv('NAMECHEAP_API_USER')
        username = os.getenv('NAMECHEAP_USERNAME')
        client_ip = os.getenv('NAMECHEAP_CLIENT_IP')
        
        # Check if credentials are configured
        if not all([api_key, api_user, username, client_ip]):
            return 'ERROR_NO_CREDENTIALS'
        
        # Namecheap API endpoint for domain availability check
        # Use sandbox for testing: https://api.sandbox.namecheap.com/xml.response
        # Use production: https://api.namecheap.com/xml.response
        api_url = "https://api.namecheap.com/xml.response"
        
        params = {
            'ApiUser': api_user,
            'ApiKey': api_key,
            'UserName': username,
            'ClientIp': client_ip,
            'Command': 'namecheap.domains.check',
            'DomainList': domain
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        
        # Parse XML response
        if response.status_code == 200:
            content = response.text
            content_lower = content.lower()
            
            # Check for API errors and extract error message
            if 'status="error"' in content_lower:
                # Try to extract the error message from XML
                error_match = re.search(r'<error[^>]*>(.*?)</error>', content, re.IGNORECASE)
                if error_match:
                    error_msg = error_match.group(1)
                    print(f"    ❌ Namecheap API Error for {domain}: {error_msg}")
                else:
                    print(f"    ❌ Namecheap API Error for {domain}: Check credentials/IP whitelist")
                # Print full response for debugging (first check only)
                if domain.endswith(('.com', '.net', '.org')):
                    print(f"    Debug - API Response: {content[:500]}")
                return 'ERROR_API'
            
            # Parse availability from XML
            # Look for Available="true" or Available="false"
            if 'available="true"' in content_lower:
                # Check if it's premium
                if 'ispremiumname="true"' in content_lower or 'premium' in content_lower:
                    return 'PREMIUM'
                return 'AVAILABLE'
            elif 'available="false"' in content_lower:
                return 'TAKEN'
            else:
                print(f"    ⚠️  Could not parse API response for {domain}")
                return 'ERROR_PARSE'
        else:
            print(f"    ❌ HTTP Error {response.status_code} for {domain}")
            return 'ERROR_HTTP'
            
    except requests.exceptions.Timeout:
        return 'ERROR_TIMEOUT'
    except Exception as e:
        print(f"    Namecheap API exception for {domain}: {type(e).__name__}")
        return 'ERROR'

def enhanced_availability_check(domain):
    """
    Enhanced availability check combining multiple methods.
    Returns tuple: (whois_available, confidence, dns_active, dns_details, http_active, registrar_status)
    
    Without API:
    - Uses advanced WHOIS checking
    - Comprehensive DNS verification (A, AAAA, MX, NS, CNAME, SOA)
    - HTTP/HTTPS response checking
    - Multi-factor confidence scoring
    
    With API (optional):
    - All of the above PLUS
    - Namecheap API verification
    """
    # 1. Advanced WHOIS Check
    whois_available, confidence, whois_details = advanced_whois_check(domain)
    
    # 2. Comprehensive DNS Check
    dns_active = False
    dns_details = {}
    http_active = False
    
    if whois_available:
        try:
            dns_active, dns_details = check_dns_exists(domain)
        except Exception:
            dns_active = False
            dns_details = {}
        
        # 3. HTTP Check (only if WHOIS says available and DNS is active)
        # This helps identify parked domains vs truly available
        if dns_active:
            try:
                http_active = check_http_response(domain)
            except:
                http_active = False
    
    # 4. Namecheap API Check (optional - only if configured)
    registrar_status = 'API_NOT_CONFIGURED'
    api_key = os.getenv('NAMECHEAP_API_KEY')
    
    # Only use API if:
    # - API key exists AND is not placeholder
    # - Domain appears available from WHOIS
    # - DNS doesn't indicate heavy use
    if api_key and api_key != 'your_api_key_here' and whois_available:
        if not dns_active or confidence == 'HIGH':
            try:
                time.sleep(0.5)  # API rate limiting
                registrar_status = check_namecheap_availability(domain)
            except:
                registrar_status = 'API_ERROR'
    
    return whois_available, confidence, dns_active, dns_details, http_active, registrar_status

# Load domain names and TLDs from folders
NAMES = load_domain_names_from_folder()
TLDS_TO_CHECK = load_tlds_from_folder()

# --- Threading Setup ---
# Using threads makes this process *significantly* faster.
# We will check this many domains at the same time.
# Reduced from 10 to 5 to avoid rate limiting
NUM_WORKERS = 5 
task_queue = queue.Queue()
results_queue = queue.Queue()
# -----------------------

def domain_checker_worker():
    """The function each thread will run - with enhanced multi-layer availability checking."""
    while True:
        try:
            name, tld = task_queue.get(timeout=3) # Wait 3s for a task
        except queue.Empty:
            return # No more tasks, thread can exit

        full_domain = name.lower() + tld
        
        print(f"Checking: {full_domain}...")
        
        # Use enhanced checking with multiple verification layers
        whois_available, confidence, dns_active, dns_details, http_active, registrar_status = enhanced_availability_check(full_domain)
        
        # Advanced decision logic for accurate availability determination
        # Priority: Namecheap API > Multi-factor analysis > WHOIS
        
        if registrar_status == 'AVAILABLE':
            # Namecheap API confirms it's available - HIGHEST confidence!
            print(f"  -> {full_domain} is ✅ CONFIRMED AVAILABLE via Namecheap API (HIGH CONFIDENCE)")
            status = "AVAILABLE"
            final_confidence = "VERY HIGH"
            
        elif registrar_status == 'PREMIUM':
            # Domain is available but premium pricing
            print(f"  -> {full_domain} is 💎 PREMIUM (available but special pricing)")
            status = "PREMIUM"
            final_confidence = "HIGH"
            
        elif registrar_status == 'TAKEN':
            # Namecheap says taken - trust it
            print(f"  -> {full_domain} is ❌ TAKEN (confirmed by Namecheap)")
            status = "TAKEN"
            final_confidence = "VERY HIGH"
            
        elif not whois_available:
            # WHOIS shows it's registered - definitely taken
            print(f"  -> {full_domain} is ❌ TAKEN (registered in WHOIS)")
            status = "TAKEN"
            final_confidence = "HIGH"
            
        elif whois_available and not dns_active and not http_active:
            # WHOIS says available, NO DNS, NO HTTP - BEST case for availability!
            dns_info = "No DNS records"
            print(f"  -> {full_domain} is ✅ LIKELY AVAILABLE ({confidence} confidence - {dns_info})")
            status = "AVAILABLE"
            final_confidence = confidence
            
        elif whois_available and dns_active and not http_active:
            # Has DNS but no HTTP response - might be parked/reserved/premium
            active_records = [k for k, v in dns_details.items() if v]
            dns_info = f"Has {', '.join(active_records)} records but no website"
            
            # If only NS/SOA (basic DNS), might still be available
            if set(active_records).issubset({'NS', 'SOA'}):
                print(f"  -> {full_domain} is ⚠️  POSSIBLY AVAILABLE ({dns_info} - may be parking)")
                status = "POSSIBLY AVAILABLE"
                final_confidence = "MEDIUM"
            else:
                # Has A, MX, or other records - likely reserved/premium
                print(f"  -> {full_domain} appears ⚠️  RESTRICTED/PREMIUM ({dns_info})")
                status = "RESTRICTED/PREMIUM"
                final_confidence = "MEDIUM"
                
        elif whois_available and http_active:
            # Responds to HTTP but WHOIS says available - likely reserved/premium
            active_records = [k for k, v in dns_details.items() if v]
            dns_info = f"Active website with {', '.join(active_records)} records"
            print(f"  -> {full_domain} is ⚠️  RESTRICTED/PREMIUM (WHOIS shows available but {dns_info})")
            status = "RESTRICTED/PREMIUM"
            final_confidence = "HIGH"
            
        else:
            # Fallback - be conservative
            print(f"  -> {full_domain} status UNCERTAIN - assuming TAKEN for safety")
            status = "TAKEN"
            final_confidence = "LOW"
        
        results_queue.put((name, tld, whois_available, confidence, dns_active, dns_details, http_active, status, final_confidence, registrar_status))
        task_queue.task_done()

def main():
    """Main function to run the threaded domain check."""
    
    print("=== DOMAIN CHECKER - ENHANCED ===")
    print("Reading configuration files...")
    
    # Check if domain names and TLDs were loaded successfully
    if not NAMES:
        print("\n❌ No domain names loaded.")
        print("Please add .txt files with domain names to: input/domain_name/")
        return
    
    if not TLDS_TO_CHECK:
        print("\n❌ No TLDs loaded.")
        print("Please add .txt files with TLDs to: input/top_level_domain/")
        return
    
    # Check Namecheap API configuration
    api_key = os.getenv('NAMECHEAP_API_KEY')
    api_configured = all([
        api_key,
        os.getenv('NAMECHEAP_API_USER'),
        os.getenv('NAMECHEAP_USERNAME'),
        os.getenv('NAMECHEAP_CLIENT_IP')
    ]) and api_key != 'your_api_key_here'
    
    print(f"\n✅ Configuration loaded successfully!")
    print(f"📝 Domain names: {len(NAMES)}")
    print(f"🌐 TLDs to check: {len(TLDS_TO_CHECK)} ({', '.join(TLDS_TO_CHECK)})")
    print(f"🔍 Total domain checks: {len(NAMES) * len(TLDS_TO_CHECK)}")
    
    print(f"\n🔬 Verification Methods:")
    print(f"   ✓ Advanced WHOIS lookup (multiple indicators)")
    print(f"   ✓ Comprehensive DNS verification (A, AAAA, MX, NS, CNAME, SOA)")
    print(f"   ✓ HTTP/HTTPS response checking")
    
    # Show API status
    if api_configured:
        print(f"   ✓ Namecheap API verification (ENABLED)")
        print(f"\n💎 ACCURACY LEVEL: VERY HIGH (All verification methods active)")
    else:
        print(f"   ⚠ Namecheap API: NOT CONFIGURED (using WHOIS+DNS+HTTP)")
        print(f"\n💎 ACCURACY LEVEL: HIGH (Multi-layer verification without API)")
        print(f"   Note: Results are still very accurate!")
        print(f"   To enable API: Edit .env file or run `python test_api.py`")
    
    print(f"\n--- Starting domain check with {NUM_WORKERS} workers ---")
    
    # 1. Start all the worker threads
    threads = []
    for _ in range(NUM_WORKERS):
        t = threading.Thread(target=domain_checker_worker)
        t.daemon = True # Allows program to exit even if threads are running
        t.start()
        threads.append(t)

    # 2. Load the task queue with all domains to check
    print("Loading task queue...")
    total_checks = 0
    for name in NAMES:
        for tld in TLDS_TO_CHECK:
            task_queue.put((name, tld))
            total_checks += 1
    
    print(f"Queue loaded with {total_checks} domains. Waiting for completion...")
    
    # 3. Wait for all tasks in the queue to be processed
    task_queue.join()
    print("All domains checked. Processing results...")

    # 4. Process all results from the results_queue
    # We use a dict to store detailed availability status for each domain+TLD combination
    domain_availability = {}
    
    while not results_queue.empty():
        name, tld, whois_available, whois_confidence, dns_active, dns_details, http_active, status, final_confidence, registrar_status = results_queue.get()
        if name not in domain_availability:
            domain_availability[name] = {}
        domain_availability[name][tld] = {
            'whois_available': whois_available,
            'whois_confidence': whois_confidence,
            'dns_active': dns_active,
            'dns_details': dns_details,
            'http_active': http_active,
            'status': status,
            'confidence': final_confidence,
            'registrar_status': registrar_status
        }

    # 5. Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 6. Write the final results to a CSV file in the output directory (table format)
    csv_filename = os.path.join(output_dir, "domain_results.csv")
    csv_detailed = os.path.join(output_dir, "domain_results_detailed.csv")
    
    try:
        # Write simplified results (original format with enhanced status)
        with open(csv_filename, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write the header row - Domain Name + each TLD as separate columns
            header = ["Domain Name"] + TLDS_TO_CHECK
            writer.writerow(header)
            
            # Write data for each name, maintaining original order
            for name in NAMES:
                row = [name]
                for tld in TLDS_TO_CHECK:
                    # Check if this domain+TLD combination is available
                    domain_info = domain_availability.get(name, {}).get(tld, {})
                    status = domain_info.get('status', 'ERROR')
                    row.append(status)
                writer.writerow(row)
        
        # Write detailed results with all information
        with open(csv_detailed, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header with comprehensive information
            header = [
                "Domain Name", "TLD", "Full Domain", "Status", "Confidence Level",
                "WHOIS Available", "DNS Active", "DNS Records", "HTTP Active",
                "Namecheap API Status", "Recommended Action"
            ]
            writer.writerow(header)
            
            # Write detailed data
            for name in NAMES:
                for tld in TLDS_TO_CHECK:
                    domain_info = domain_availability.get(name, {}).get(tld, {})
                    full_domain = name.lower() + tld
                    status = domain_info.get('status', 'ERROR')
                    confidence = domain_info.get('confidence', 'UNKNOWN')
                    whois_avail = 'Yes' if domain_info.get('whois_available', False) else 'No'
                    dns_active = 'Yes' if domain_info.get('dns_active', False) else 'No'
                    
                    # Format DNS records
                    dns_details = domain_info.get('dns_details', {})
                    active_dns = [k for k, v in dns_details.items() if v] if dns_details else []
                    dns_records = ', '.join(active_dns) if active_dns else 'None'
                    
                    http_active = 'Yes' if domain_info.get('http_active', False) else 'No'
                    registrar_status = domain_info.get('registrar_status', 'UNKNOWN')
                    
                    # Recommended action based on status and confidence
                    if status == 'AVAILABLE' and confidence in ['HIGH', 'VERY HIGH']:
                        action = '✓ Safe to purchase'
                    elif status == 'AVAILABLE':
                        action = '⚠ Check manually before purchase'
                    elif status == 'POSSIBLY AVAILABLE':
                        action = '⚠ Verify on registrar website'
                    elif status == 'PREMIUM':
                        action = '💎 Premium pricing - check cost'
                    else:
                        action = '✗ Not available'
                    
                    row = [name, tld, full_domain, status, confidence, whois_avail, dns_active, 
                           dns_records, http_active, registrar_status, action]
                    writer.writerow(row)
        
        # Create a summary file with only truly available domains
        csv_available = os.path.join(output_dir, "available_domains.csv")
        with open(csv_available, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            header = ["Full Domain", "Domain Name", "TLD", "Confidence Level", "Verification Method"]
            writer.writerow(header)
            
            available_count = 0
            possibly_available_count = 0
            for name in NAMES:
                for tld in TLDS_TO_CHECK:
                    domain_info = domain_availability.get(name, {}).get(tld, {})
                    status = domain_info.get('status', '')
                    confidence = domain_info.get('confidence', 'UNKNOWN')
                    registrar_status = domain_info.get('registrar_status', 'UNKNOWN')
                    
                    # Include AVAILABLE and POSSIBLY AVAILABLE domains
                    if status in ['AVAILABLE', 'POSSIBLY AVAILABLE']:
                        full_domain = name.lower() + tld
                        
                        # Determine verification method
                        if registrar_status == 'AVAILABLE':
                            verification = 'Namecheap API'
                        else:
                            verification = 'WHOIS + DNS + HTTP'
                        
                        writer.writerow([full_domain, name, tld, confidence, verification])
                        
                        if status == 'AVAILABLE':
                            available_count += 1
                        else:
                            possibly_available_count += 1
                
        print(f"\n--- SUCCESS ---")
        print(f"✓ Summary results saved to: {csv_filename}")
        print(f"✓ Detailed results saved to: {csv_detailed}")
        print(f"✓ Available domains list saved to: {csv_available}")
        print(f"\n📊 Summary:")
        print(f"   Total domains checked: {len(NAMES) * len(TLDS_TO_CHECK)}")
        print(f"   Likely available domains: {available_count}")
        if possibly_available_count > 0:
            print(f"   Possibly available domains: {possibly_available_count} (verify manually)")
        
        if available_count > 0:
            print(f"\n🎉 Found {available_count} domain(s) that appear to be available for purchase!")
            print(f"   Check {csv_available} for the complete list.")
            print(f"\n💡 Recommendation:")
            print(f"   - HIGH/VERY HIGH confidence = Safe to proceed")
            print(f"   - MEDIUM confidence = Verify on registrar website first")
        
        if possibly_available_count > 0:
            print(f"\n⚠️  {possibly_available_count} domain(s) are POSSIBLY available but need manual verification")
        
        # Show verification method used
        if api_configured:
            print(f"\n✓ Verification: Namecheap API + WHOIS + DNS + HTTP (Highest Accuracy)")
        else:
            print(f"\n✓ Verification: Advanced WHOIS + Comprehensive DNS + HTTP (High Accuracy)")
            print(f"   Note: Results are accurate even without API!")
        
    except IOError as e:
        print(f"\n--- ERROR ---")
        print(f"Could not write to file: {e}")
    except Exception as e:
        print(f"\n--- UNEXPECTED ERROR ---")
        print(f"An error occurred: {e}")

# --- Main execution ---
if __name__ == "__main__":
    main()

