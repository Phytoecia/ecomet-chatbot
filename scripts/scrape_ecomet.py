#!/usr/bin/env python3
"""
Scrape eCOMET documentation AND source code from GitHub.
This script is run by GitHub Actions weekly to keep the knowledge base up-to-date.
"""

import requests
from bs4 import BeautifulSoup
import os
import base64
from datetime import datetime

# Documentation website
DOCS_URL = "https://phytoecia.github.io/eCOMET"

# GitHub API for source code
GITHUB_API = "https://api.github.com/repos/Phytoecia/eCOMET/contents"

# Key documentation pages to scrape
DOC_PAGES = [
    "/index.html",
    "/reference/index.html",
    "/articles/index.html",
    "/articles/Treatment-based_study_tutorial.html",
    "/articles/Group-based_study_tutorial.html",
    "/articles/Longitudinal_study_tutorial.html",
    "/news/index.html",
]

# Reference function documentation pages
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

# Key source code files to include (R files from the package)
SOURCE_CODE_PATHS = [
    "R",  # All R source files
    "DESCRIPTION",
    "NAMESPACE",
]


def clean_text(soup):
    """Extract clean text from HTML, preserving code blocks."""
    for script in soup(["script", "style", "nav", "footer", "header"]):
        script.decompose()
    text = soup.get_text(separator='\n')
    lines = [line.strip() for line in text.splitlines()]
    return '\n'.join(line for line in lines if line)


def scrape_doc_page(url):
    """Scrape a single documentation page."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('h1')
        title_text = title.get_text() if title else url.split('/')[-1]
        
        main = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        content = clean_text(main) if main else clean_text(soup)
        
        return f"\n\n{'='*60}\n## {title_text}\nSource: {url}\n{'='*60}\n\n{content}"
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""


def fetch_github_file(path):
    """Fetch a file from GitHub API and return its content."""
    try:
        url = f"{GITHUB_API}/{path}"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, list):
            # It's a directory, return list of files
            return data
        else:
            # It's a file, decode content
            if data.get('encoding') == 'base64':
                content = base64.b64decode(data['content']).decode('utf-8')
                return content
            return None
    except Exception as e:
        print(f"Error fetching {path}: {e}")
        return None


def scrape_source_code():
    """Scrape R source code from GitHub."""
    all_code = []
    all_code.append("\n\n" + "="*60)
    all_code.append("# eCOMET R PACKAGE SOURCE CODE")
    all_code.append("# From: https://github.com/Phytoecia/eCOMET")
    all_code.append("="*60)
    
    # Fetch DESCRIPTION file
    print("Fetching DESCRIPTION...")
    desc = fetch_github_file("DESCRIPTION")
    if desc:
        all_code.append(f"\n\n## DESCRIPTION\n```\n{desc}\n```")
    
    # Fetch NAMESPACE file
    print("Fetching NAMESPACE...")
    ns = fetch_github_file("NAMESPACE")
    if ns:
        all_code.append(f"\n\n## NAMESPACE\n```\n{ns}\n```")
    
    # Fetch all R files from R/ directory
    print("Fetching R source files...")
    r_files = fetch_github_file("R")
    if r_files and isinstance(r_files, list):
        for file_info in r_files:
            if file_info.get('name', '').endswith('.R'):
                print(f"  Fetching R/{file_info['name']}...")
                content = fetch_github_file(f"R/{file_info['name']}")
                if content:
                    all_code.append(f"\n\n## R/{file_info['name']}\n```r\n{content}\n```")
    
    return '\n'.join(all_code)


def main():
    print("Starting eCOMET knowledge base update...")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    all_content = []
    all_content.append("# eCOMET Complete Knowledge Base")
    all_content.append(f"# Documentation from: {DOCS_URL}")
    all_content.append(f"# Source code from: https://github.com/Phytoecia/eCOMET")
    all_content.append(f"# Last updated: {datetime.now().isoformat()}")
    
    # Section 1: Documentation
    all_content.append("\n\n" + "#"*60)
    all_content.append("# PART 1: DOCUMENTATION")
    all_content.append("#"*60)
    
    # Scrape main doc pages
    for page in DOC_PAGES:
        url = DOCS_URL + page
        print(f"Scraping doc: {url}")
        content = scrape_doc_page(url)
        if content:
            all_content.append(content)
    
    # Scrape reference pages
    for func in REFERENCE_FUNCTIONS:
        url = f"{DOCS_URL}/reference/{func}"
        print(f"Scraping ref: {url}")
        content = scrape_doc_page(url)
        if content:
            all_content.append(content)
    
    # Section 2: Source Code
    all_content.append("\n\n" + "#"*60)
    all_content.append("# PART 2: SOURCE CODE")
    all_content.append("#"*60)
    
    source_code = scrape_source_code()
    all_content.append(source_code)
    
    # Write output
    output_file = "ecomet_reference_full.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_content))
    
    file_size = os.path.getsize(output_file) / 1024
    print(f"\nDone! Saved to {output_file}")
    print(f"Total size: {file_size:.1f} KB")


if __name__ == "__main__":
    main()
