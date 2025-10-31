# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-31

### Added
- **Namecheap API Integration** - Direct verification via Namecheap's official API
- **DNS Verification** - Check for active DNS records (A, AAAA, MX, NS)
- **Multi-layer verification system** - Combines WHOIS, DNS, and API checks
- **Premium domain detection** - Identifies domains with premium pricing
- **Enhanced status reporting** - More detailed availability information
- **Environment variable support** - Secure credential management via `.env` file
- **Three output formats**:
  - `domain_results.csv` - Summary table
  - `domain_results_detailed.csv` - Complete details with API status
  - `available_domains.csv` - Only purchasable domains
- **Comprehensive documentation** - Enhanced README with setup instructions
- **Security features** - `.gitignore` for API credentials
- **Python-dotenv** for environment management

### Changed
- **Improved accuracy** - Filters out reserved and restricted domains
- **Better error handling** - More robust connection and retry logic
- **Enhanced worker function** - Now includes all verification methods
- **Updated output format** - Added Namecheap API status column
- **Refined status messages** - Clearer console output during checks

### Fixed
- False positives for reserved domains
- DNS-based availability detection
- Rate limiting issues with better delays

## [1.0.0] - 2025-10-30

### Added
- Initial release
- Basic WHOIS lookup functionality
- Multi-threaded domain checking
- CSV output in table format
- Folder-based input system
- Support for multiple domain name files
- Support for multiple TLD files
- Error handling and retry logic
- Rate limiting with configurable delays

### Features
- Check domain availability using WHOIS
- Parallel processing with threading
- Organized folder structure
- Duplicate removal
- Professional CSV reports

---

## Upcoming Features

### [2.1.0] - Planned
- [ ] GoDaddy API integration
- [ ] Google Domains API support
- [ ] GUI interface
- [ ] Domain price comparison
- [ ] Export to multiple formats (JSON, Excel)

### [3.0.0] - Future
- [ ] Web-based dashboard
- [ ] Real-time monitoring
- [ ] Email notifications
- [ ] Database integration
- [ ] Advanced filtering options
- [ ] Bulk domain suggestions

---

## Version History

- **2.0.0** - Enhanced with Namecheap API and DNS verification
- **1.0.0** - Initial release with basic WHOIS checking
