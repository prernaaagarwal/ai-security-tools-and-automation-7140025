#!/usr/bin/env python3
"""
Privacy Policy Scraper
Finds and downloads privacy policy pages from company websites as PDFs.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys
import os
from playwright.sync_api import sync_playwright
import re


def find_privacy_policy_link(homepage_url):
    """
    Scans a homepage for privacy policy links using Playwright.

    Args:
        homepage_url: The homepage URL to scan

    Returns:
        The privacy policy URL if found, None otherwise
    """
    try:
        # Use Playwright to fetch the homepage (avoids blocking)
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(homepage_url, wait_until='domcontentloaded', timeout=30000)

            # Get page content
            html_content = page.content()
            browser.close()

        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Keywords to search for in links
        privacy_keywords = [
            'privacy',
            'privacy-policy',
            'privacy_policy',
            'privacypolicy',
            'privacy-notice',
            'data-protection'
        ]

        # Find all links
        links = soup.find_all('a', href=True)

        for link in links:
            href = link.get('href', '').lower()
            text = link.get_text().lower().strip()

            # Check if link text or href contains privacy keywords
            for keyword in privacy_keywords:
                if keyword in href or keyword in text:
                    # Convert relative URL to absolute
                    full_url = urljoin(homepage_url, link['href'])
                    print(f"✓ Found privacy policy link: {full_url}")
                    return full_url

        return None

    except Exception as e:
        print(f"✗ Error fetching homepage: {e}")
        return None


def download_privacy_policy_as_pdf(privacy_url, output_filename=None):
    """
    Downloads a privacy policy page and saves it as PDF.

    Args:
        privacy_url: The privacy policy URL
        output_filename: Optional filename for the PDF (auto-generated if not provided)
    """
    try:
        # Generate filename if not provided
        if not output_filename:
            domain = urlparse(privacy_url).netloc
            domain = re.sub(r'^www\.', '', domain)  # Remove www. prefix
            output_filename = f"{domain}_privacy_policy.pdf"

        # Ensure .pdf extension
        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'

        print(f"⏳ Downloading privacy policy from: {privacy_url}")

        # Use Playwright to render and save as PDF
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(privacy_url, wait_until='domcontentloaded', timeout=60000)

            # Wait a bit for dynamic content to load
            page.wait_for_timeout(2000)

            # Save as PDF
            page.pdf(path=output_filename, format='A4')
            browser.close()

        print(f"✓ Privacy policy saved as: {output_filename}")
        return output_filename

    except Exception as e:
        print(f"✗ Error downloading privacy policy: {e}")
        return None


def scrape_privacy_policy(homepage_url, output_filename=None):
    """
    Main function to scrape and download privacy policy.

    Args:
        homepage_url: The company's homepage URL
        output_filename: Optional filename for the PDF

    Returns:
        Path to the downloaded PDF if successful, None otherwise
    """
    print(f"\n{'='*60}")
    print(f"Privacy Policy Scraper")
    print(f"{'='*60}")
    print(f"Scanning: {homepage_url}\n")

    # Ensure URL has protocol
    if not homepage_url.startswith(('http://', 'https://')):
        homepage_url = 'https://' + homepage_url

    # Step 1: Find privacy policy link
    privacy_url = find_privacy_policy_link(homepage_url)

    if not privacy_url:
        print(f"\n⚠️  WARNING: No privacy policy link found on {homepage_url}")
        print("   The website may not have a privacy policy, or it may be")
        print("   located in a place the scraper cannot detect.")
        return None

    # Step 2: Download as PDF
    pdf_path = download_privacy_policy_as_pdf(privacy_url, output_filename)

    if pdf_path:
        print(f"\n✓ SUCCESS: Privacy policy downloaded successfully!")
        print(f"  Location: {os.path.abspath(pdf_path)}")
    else:
        print(f"\n✗ FAILED: Could not download privacy policy")

    print(f"{'='*60}\n")
    return pdf_path


if __name__ == "__main__":
    # Check if URL provided as command line argument
    if len(sys.argv) > 1:
        url = sys.argv[1]
        filename = sys.argv[2] if len(sys.argv) > 2 else None
        scrape_privacy_policy(url, filename)
    else:
        # Interactive mode
        print("\n" + "="*60)
        print("Privacy Policy Scraper - Interactive Mode")
        print("="*60)
        url = input("\nEnter company homepage URL: ").strip()

        if url:
            scrape_privacy_policy(url)
        else:
            print("No URL provided. Exiting.")
