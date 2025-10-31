# Contributing to Domain Availability Checker

First off, thank you for considering contributing to Domain Availability Checker! 🎉

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the behavior
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Error messages or logs**

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear and descriptive title**
- **Detailed description** of the suggested enhancement
- **Use cases** - explain why this would be useful
- **Possible implementation** approach (if you have ideas)

### 🔀 Pull Requests

1. Fork the repo and create your branch from `main`
2. Make your changes
3. Test your changes thoroughly
4. Update documentation if needed
5. Ensure code follows Python PEP 8 style guide
6. Write clear commit messages
7. Submit a pull request!

#### Pull Request Guidelines

- Keep PRs focused - one feature/fix per PR
- Update the README if you're adding features
- Add comments to complex code
- Test with and without Namecheap API configured
- Ensure no API credentials are committed

### 🎯 Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/DomainChecker.git
cd DomainChecker

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env and configure (optional)
cp .env.example .env
```

### 📝 Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and not too long
- Comment complex logic

### 🧪 Testing

Before submitting:

- Test with various domain names and TLDs
- Test with and without API credentials
- Test error handling (network issues, rate limiting, etc.)
- Verify all output files are generated correctly

### 💭 Feature Ideas

Looking for inspiration? Here are some features we'd love to see:

- [ ] Support for GoDaddy API
- [ ] Support for Google Domains API
- [ ] GUI interface (Tkinter, PyQt, or web-based)
- [ ] Domain name suggestions based on keywords
- [ ] Price comparison across registrars
- [ ] Email notifications when domains become available
- [ ] Database integration for tracking checks over time
- [ ] Docker support
- [ ] Unit tests
- [ ] CI/CD pipeline

### 📧 Questions?

Feel free to open an issue with your question or reach out to [@sithulaka](https://github.com/sithulaka).

---

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Respecting differing viewpoints
- Accepting constructive criticism gracefully
- Focusing on what's best for the community

**Unacceptable behavior includes:**
- Harassment or discriminatory language
- Trolling or insulting comments
- Publishing others' private information
- Unprofessional conduct

### Enforcement

Project maintainers have the right to remove comments, commits, or contributions that don't align with this Code of Conduct.

---

Thank you for contributing! 🙌
