#!/usr/bin/env python3
"""
Scrape eCOMET documentation from the pkgdown website.
This script is run by GitHub Actions weekly to keep the knowledge base up-to-date.
"""

import requests
from bs4 import BeautifulSoup
import os
import re

BASE_URL = "https://phytoecia.github.io/eCOMET"

# Key pages to scrape
PAGES = [
    "/index.html",
    "/reference/index.html",
    "/articles/index.html",
    "/articles/Treatment-based_study_tutorial.html",
    "/articles/Group-based_study_tutorial.html",
    "/articles/Longitudinal_study_tutorial.html",
    "/news/index.html",
]

# Also scrape all reference pages
REFERENCE_FUNCTIONS = [
    "add_env_trait.html",
    "analyze_env_change_by_treatment.html",
    "assign_env_groups.html",
    "eco.html",
    "ecoInt.html",
    "fiteco.html",
    "fitZicoSeq.html",
    "GetX2clineFeature.html",
    "load_demo_16S.html",
    "load_demo_ecocom.html",
    "load_demo_metabolome.html",
    "plotMDS.html",
    "plotPCA.html",
    "run_env_analysis.html",
    "run_PERMANOVA.html",
]

def clean_text(soup):
    """Extract clean text from HTML, preserving code blocks."""
    # Remove script and style elements
    for script in soup(["script", "style", "nav", "footer", "header"]):
        script.decompose()
    
    # Get text
    text = soup.get_text(separator='\n')
    
    # Clean up whitespace
    lines = [line.strip() for line in text.splitlines()]
    text = '\n'.join(line for line in lines if line)
    
    return text

def scrape_page(url):
    """Scrape a single page and return its content."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get page title
        title = soup.find('h1')
        title_text = title.get_text() if title else url.split('/')[-1]
        
        # Get main content
        main = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        if main:
            content = clean_text(main)
        else:
            content = clean_text(soup)
        
        return f"\n\n{'='*60}\n## {title_text}\nSource: {url}\n{'='*60}\n\n{content}"
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def main():
    print("Starting eCOMET documentation scrape...")
    
    all_content = []
    all_content.append("# eCOMET Documentation Knowledge Base")
    all_content.append(f"# Auto-generated from {BASE_URL}")
    all_content.append(f"# Last updated: {__import__('datetime').datetime.now().isoformat()}")
    
    # Scrape main pages
    for page in PAGES:
        url = BASE_URL + page
        print(f"Scraping: {url}")
        content = scrape_page(url)
        if content:
            all_content.append(content)
    
    # Scrape reference pages
    for func in REFERENCE_FUNCTIONS:
        url = f"{BASE_URL}/reference/{func}"
        print(f"Scraping: {url}")
        content = scrape_page(url)
        if content:
            all_content.append(content)
    
    # Write output
    output_file = "ecomet_reference_full.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_content))
    
    print(f"Done! Saved to {output_file}")
    print(f"Total size: {os.path.getsize(output_file) / 1024:.1f} KB")

if __name__ == "__main__":
    main()
