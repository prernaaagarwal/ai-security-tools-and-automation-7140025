# Privacy Policy Scraper

Automatically finds and downloads privacy policy pages from company websites as PDFs.

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install chromium
```

## Usage

### Command Line Mode

```bash
# Basic usage - auto-generates filename
python privacy_policy_scraper.py https://auditcaddie.com

# Specify custom output filename
python privacy_policy_scraper.py https://auditcaddie.com audit_caddie_privacy.pdf
```

### Interactive Mode

Run without arguments for interactive prompts:
```bash
python privacy_policy_scraper.py
```

## How It Works

1. **Scans Homepage**: Fetches the company homepage and parses HTML
2. **Finds Privacy Link**: Searches for links containing keywords like:
   - privacy
   - privacy-policy
   - privacy_policy
   - privacypolicy
   - privacy-notice
   - data-protection

3. **Downloads as PDF**: Uses Playwright to render the page and save as PDF
4. **Error Handling**: Displays warning if no privacy policy is found

## Output

- PDFs are saved in the current directory
- Filename format: `{domain}_privacy_policy.pdf`
- Example: `auditcaddie.com_privacy_policy.pdf`

## Examples

```bash
# Audit Caddie
python privacy_policy_scraper.py https://auditcaddie.com

# Other companies
python privacy_policy_scraper.py https://example.com
python privacy_policy_scraper.py www.company.com
```

## Use Case

This tool supports a Security's privacy compliance workflow:
- Quickly assess website privacy policies
- Identify non-compliant websites
- Generate reports on privacy statement gaps
- Automate privacy policy collection for multiple clients
