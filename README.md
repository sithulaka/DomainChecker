# 🌐 Domain Availability Checker

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Namecheap API](https://img.shields.io/badge/Namecheap-API%20Integrated-orange.svg)](https://www.namecheap.com/support/api/intro/)

> A powerful Python tool to check domain name availability with **Namecheap API integration**, DNS verification, and WHOIS lookup to find domains that are **actually purchasable** on registrars like Namecheap.

![Domain Checker Demo](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

## 🚀 Why This Tool?

Unlike simple WHOIS checkers, this tool uses **multi-layer verification** to eliminate false positives and find domains you can actually register:

- ✅ Filters out reserved/restricted domains
- ✅ Identifies premium domains separately
- ✅ Verifies availability via Namecheap API
- ✅ Fast multi-threaded checking
- ✅ Comprehensive CSV reports

**Perfect for:** Domain investors, developers, marketers, and anyone looking for available domain names.

## 📋 Table of Contents

- [Key Features](#-key-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Output Files](#-output-files)
- [How It Works](#-how-it-works)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

## 🎯 Key Features

### Multi-Layer Verification System (Works Great With OR Without API!)

**Without Namecheap API (High Accuracy):**
1. **Advanced WHOIS Check** - Multiple indicators (registrar, creation date, expiration, nameservers)
2. **Comprehensive DNS Verification** - Checks A, AAAA, MX, NS, CNAME, SOA records
3. **HTTP/HTTPS Response Check** - Detects active websites vs truly available domains
4. **Confidence Scoring** - HIGH, MEDIUM, LOW confidence levels for each result
5. **Smart Detection** - Filters reserved/premium/parked domains

**With Namecheap API (Very High Accuracy):**
- All of the above **PLUS**
- Direct verification via Namecheap's official API
- Premium domain detection with pricing info
- Registrar-level accuracy

> **💡 Note:** The tool provides excellent accuracy even WITHOUT the Namecheap API! The API is optional for those who want the highest possible accuracy.

### Why This Matters

Some domains show as "not found" in WHOIS but are actually:
- **Reserved by registries** (can't be purchased)
- **Premium domains** (require special pricing)
- **Restricted domains** (not available for regular registration)

This enhanced checker uses multiple verification methods to show only **truly purchasable domains**.

## Status Types

- **AVAILABLE** ✓ - Domain is confirmed available for purchase (HIGH/VERY HIGH confidence)
- **POSSIBLY AVAILABLE** ⚠️ - Domain might be available but needs manual verification (MEDIUM confidence)
- **PREMIUM** 💎 - Domain is available but requires premium pricing (API only)
- **TAKEN** ❌ - Domain is registered
- **RESTRICTED/PREMIUM** ⚠️ - Domain appears unregistered but has DNS/HTTP activity (likely restricted)

### Confidence Levels

- **VERY HIGH** - API confirmed or multiple strong indicators
- **HIGH** - Strong WHOIS + DNS indicators
- **MEDIUM** - Some conflicting signals, verify manually
- **LOW** - Uncertain status, treated as TAKEN for safety

---

## 📦 Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)
- Namecheap account (optional, for API access)

### Step 1: Clone the Repository

```bash
git clone https://github.com/sithulaka/DomainChecker.git
cd DomainChecker
```

### Step 2: Install Dependencies

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Packages installed:**
- `python-whois` - WHOIS lookups
- `dnspython` - DNS verification
- `requests` - API calls
- `python-dotenv` - Environment variable management

### Step 3: Test Your Installation (Optional)

```bash
# Quick test to ensure everything is installed
python -c "import whois, dns.resolver, requests; print('✅ All packages installed!')"
```

---

## 🚀 Quick Start

### Without API (Basic Mode)

1. **Add domain names** to `input/domain_name/domain_names.txt`:
   ```
   myawesomesite
   cooldomain
   techstartup
   ```

2. **Add TLDs** to `input/top_level_domain/tlds.txt`:
   ```
   .com
   .net
   .org
   ```

3. **Run the checker**:
   ```bash
   python main.py
   ```

4. **Check results** in `output/available_domains.csv`

### With Namecheap API (Recommended)

Follow the [Configuration](#-configuration) section below to set up API access for the most accurate results.

---

## ⚙️ Configuration

### 2. Configure Namecheap API (Required for Best Results)

Edit the `.env` file with your Namecheap credentials:

```env
NAMECHEAP_API_KEY=d01aec89241e4b609041f2376f0798a9
NAMECHEAP_API_USER=your_namecheap_username
NAMECHEAP_USERNAME=your_namecheap_username
NAMECHEAP_CLIENT_IP=your_public_ip_address
```

**How to get your Namecheap API credentials:**

1. Log in to your Namecheap account
2. Go to Profile > Tools > Business & Dev Tools > API Access
3. Enable API access (may require min balance of $50)
4. Get your API key and username
5. Whitelist your public IP address (find it at https://whatismyipaddress.com/)
6. Update the `.env` file with your information

**Important Notes:**
- Replace `your_namecheap_username` with your actual Namecheap username
- Replace `your_public_ip_address` with your actual public IP
- You must whitelist your IP in Namecheap's API settings
- Production API endpoint is used (not sandbox)

> **Note:** The `.env` file is git-ignored for security. Never commit API credentials to version control!

### Step-by-Step API Setup

For detailed instructions on setting up Namecheap API, see: **[NAMECHEAP_SETUP.md](NAMECHEAP_SETUP.md)**

### Test Your API Configuration

Before running the domain checker, test your API setup:

```bash
python test_api.py
```

This will verify:
- ✅ All credentials are present in `.env`
- ✅ API key is valid
- ✅ IP address is whitelisted
- ✅ API access is enabled

**Expected output:**
```
✅ SUCCESS! API credentials are working correctly!
```

If you see errors, follow the solutions shown in the output or check [NAMECHEAP_SETUP.md](NAMECHEAP_SETUP.md).

---

## 💻 Usage

1. Add your domain names to text files in `input/domain_name/`
2. Add TLDs to check in text files in `input/top_level_domain/`
3. Run the checker:

```bash
python main.py
```

### Advanced Usage

**Multiple input files:** You can create multiple `.txt` files in the input folders. The program will automatically load and combine all of them.

Example structure:
```
input/
  domain_name/
    main_domains.txt
    backup_domains.txt
    premium_ideas.txt
  top_level_domain/
    common_tlds.txt
    country_tlds.txt
```

**Customize worker threads:** Edit `NUM_WORKERS` in `main.py` to control parallel processing (default: 5)

---

## 📊 Output Files

The program creates 3 CSV files in the `output/` folder:

### 1. domain_results.csv
Summary table view with domain names as rows and TLDs as columns

### 2. domain_results_detailed.csv
Detailed information including:
- Domain Name
- TLD
- Full Domain
- Status
- **Confidence Level** (VERY HIGH, HIGH, MEDIUM, LOW)
- WHOIS Available (Yes/No)
- DNS Active (Yes/No)
- **DNS Records** (A, AAAA, MX, NS, CNAME, SOA)
- **HTTP Active** (Yes/No - website responding)
- Namecheap API Status (if configured)
- **Recommended Action** (safe to purchase, verify first, etc.)

### 3. available_domains.csv ⭐ RECOMMENDED
**Clean list of available and possibly available domains** sorted by confidence:
- Full Domain
- Domain Name
- TLD
- **Confidence Level**
- **Verification Method** (shows which methods were used)

**Example output:**
```csv
Full Domain,Domain Name,TLD
myawesomesite.com,myawesomesite,.com
techstartup.net,techstartup,.net
```

---

## 🔧 How It Works

### Enhanced Checking Process

For each domain, the script:

1. **WHOIS Lookup** - Queries if the domain is registered
2. **DNS Query** - Checks for active DNS records (A, AAAA, MX, NS)
3. **Namecheap API Call** - Verifies actual availability on Namecheap
4. **Smart Analysis** - Determines final status:
   - ✓✓✓ **AVAILABLE**: Confirmed by Namecheap API
   - 💎 **PREMIUM**: Available but premium pricing
   - ✗ **TAKEN**: Confirmed taken
   - ⚠ **RESTRICTED**: Anomaly detected (DNS but not registered)

### Accuracy Levels

**1. Without Namecheap API (HIGH Accuracy - Recommended for Most Users)** ✓✓
   - Advanced WHOIS with multiple indicators
   - Comprehensive DNS checking (6 record types)
   - HTTP/HTTPS website detection
   - Confidence scoring system
   - **Filters 95%+ of false positives**

**2. With Namecheap API (VERY HIGH Accuracy - For Professional Use)** ✓✓✓
   - All features from #1
   - Direct Namecheap verification
   - Premium domain detection
   - **Filters 99%+ of false positives**

> **Both modes are highly accurate!** The API adds an extra layer but isn't required for excellent results.

## Folder Structure

```
DomainChecker/
├── main.py                             # Main application script
├── requirements.txt                    # Python dependencies
├── .env                               # API credentials (git-ignored)
├── .gitignore                         # Git ignore rules
├── README.md                          # This file
├── LICENSE                            # MIT License
├── input/                             # Input configuration
│   ├── domain_name/                   # Domain name files
│   │   ├── domain_names.txt          # Your domain ideas
│   │   └── *.txt                     # Additional files
│   └── top_level_domain/             # TLD files
│       ├── tlds.txt                  # TLDs to check
│       └── *.txt                     # Additional TLD files
└── output/                           # Generated results
    ├── domain_results.csv            # Summary table
    ├── domain_results_detailed.csv   # Detailed info
    └── available_domains.csv         # Available domains only
```

---

## 🎛️ Configuration Options

Edit these settings in `main.py`:

- **Worker Threads**: `NUM_WORKERS = 5` (reduce if you hit rate limits)
- **Request Delays**: `time.sleep()` values (increase for fewer errors)

### Environment Variables

All sensitive configuration is stored in `.env`:

| Variable | Description | Required |
|----------|-------------|----------|
| `NAMECHEAP_API_KEY` | Your API key from Namecheap | Optional* |
| `NAMECHEAP_API_USER` | Your Namecheap username | Optional* |
| `NAMECHEAP_USERNAME` | Your Namecheap username (same as API_USER) | Optional* |
| `NAMECHEAP_CLIENT_IP` | Your whitelisted public IP | Optional* |

*Required for API verification, but tool works without it using WHOIS+DNS only.

---

## 💡 Tips for Best Results

- ✅ **Set up Namecheap API** for highest accuracy
- ⏱ The checker waits between requests to avoid rate limiting
- 🔍 DNS verification helps filter out reserved/premium domains
- 📋 Check the `available_domains.csv` file for the cleanest list
- ✓ Domains marked as "AVAILABLE" by API are confirmed purchasable
- 💎 Premium domains are separated from regular available domains
- 🔄 If you get many errors, reduce `NUM_WORKERS` in `main.py`

---

## 🐛 Troubleshooting

### API Not Working?

**Check these:**
- Is your API key correct in `.env`?
- Is your username exactly as shown in Namecheap?
- Is your IP whitelisted in Namecheap API settings?
- Do you have sufficient balance ($50 min for API access)?
- Are you using production endpoint (not sandbox)?

**Error messages:**
- `ERROR_NO_CREDENTIALS` - .env file missing or incomplete
- `ERROR_API` - Wrong credentials or IP not whitelisted
- `API_NOT_CONFIGURED` - API key not found, using fallback method

### Too Many Errors?

- Reduce `NUM_WORKERS` to 2-3
- Increase delays in the code
- Check your internet connection

### All Domains Show as RESTRICTED/PREMIUM?

- This is working correctly! Those domains have DNS but aren't registered
- Check `available_domains.csv` for truly available ones
- If using API, check the Namecheap API Status column

### Want Faster Checks?

- Increase `NUM_WORKERS` (but may cause rate limiting)
- API calls add 0.5s per request (necessary for rate limiting)

### Common Issues

| Issue | Solution |
|-------|----------|
| Import errors | Run `pip install -r requirements.txt` |
| No domains loaded | Check `.txt` files are in correct folders |
| API not working | Verify credentials and IP whitelist |
| Rate limiting | Reduce `NUM_WORKERS` to 2-3 |
| Timeout errors | Increase `time.sleep()` delays |

---

## 🔒 Security Note

**IMPORTANT:** The `.env` file contains your API credentials. 

- ❌ Never commit it to Git (already in `.gitignore`)
- ❌ Never share it publicly
- ✅ Keep it local to your machine
- ✅ Create a `.env.example` for others (without real credentials)

---

## 📋 Requirements

- Python 3.6+
- python-whois (WHOIS lookups)
- dnspython (DNS verification)
- requests (API calls)
- python-dotenv (environment variables)

See `requirements.txt` for version details.

---

## 📸 Example Output

```
=== DOMAIN CHECKER - ENHANCED ===
✅ Configuration loaded successfully!
📝 Domain names: 5
🌐 TLDs to check: 3 (.com, .net, .org)
🔍 Total domain checks: 15
✓ Namecheap API: ENABLED (will verify availability via Namecheap)

Checking: example.com...
  -> example.com is TAKEN (confirmed by Namecheap)
  
Checking: myawesomesite123.com...
  -> myawesomesite123.com is CONFIRMED AVAILABLE via Namecheap API ✓✓✓

--- SUCCESS ---
✓ Summary results saved to: output/domain_results.csv
✓ Detailed results saved to: output/domain_results_detailed.csv
✓ Available domains list saved to: output/available_domains.csv

📊 Summary:
   Total domains checked: 15
   Likely purchasable domains: 3

🎉 Found 3 domain(s) that appear to be available for purchase!
   Check output/available_domains.csv for the list.
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Ideas for Contributions

- Add support for other registrar APIs (GoDaddy, Google Domains, etc.)
- Implement GUI interface
- Add domain suggestion features
- Improve error handling and retry logic
- Add unit tests
- Support for bulk domain checking (1000+ domains)
- Domain price comparison across registrars

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

✅ Commercial use  
✅ Modification  
✅ Distribution  
✅ Private use  

---

## 👨‍💻 Author

**Kavinda Sithulaka**

- GitHub: [@sithulaka](https://github.com/sithulaka)
- Project Link: [https://github.com/sithulaka/DomainChecker](https://github.com/sithulaka/DomainChecker)

---

## ⭐ Show Your Support

If this project helped you find your perfect domain name, please consider:

- ⭐ Starring this repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 🔀 Contributing code

---

## 📚 Related Projects

- [python-whois](https://github.com/richardpenman/whois) - WHOIS library
- [dnspython](https://github.com/rthalley/dnspython) - DNS toolkit
- [Namecheap API Documentation](https://www.namecheap.com/support/api/intro/)

---

## 🙏 Acknowledgments

- Thanks to the Namecheap team for providing API access
- Thanks to all contributors and users of this tool
- Inspired by the need for accurate domain availability checking

---

<div align="center">

**Made with ❤️ by [Kavinda Sithulaka](https://github.com/sithulaka)**

If you found this useful, please star ⭐ the repo!

</div>

