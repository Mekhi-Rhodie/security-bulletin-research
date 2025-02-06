#!/usr/bin/env python3
import sys
import requests
from bs4 import BeatifulSoup
from tabulate import tabulate

def scrape_cisa_table(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return
    
    content = BeatifulSoup(response.content, "html.parser")

    table = content.find("table")
    if not table:
        print("No table found on this page.")
        return
    
    headers = []
    thead = table.find("thead")
    if thead:
        header_cells = thead.find_all("th")
        headers = [cell.get_text(strip=True) for cell in header_cells]
    else:
        # Try to extract headers from the first row
        first_row = table.find("tr")
        if first_row:
            header_cells = first_row.find_all(["th", "td"])
            headers = [cell.get_text(strip=True) for cell in header_cells]

    rows = []
    tbody = table.find("tbody")
    if tbody:
        tr_tags = tbody.find_all("tr")
    else:
        tr_tags = table.find_all("tr")
    
    for tr in tr_tags:
        cells = tr.find_all(["td", "th"])
        row = [cell.get_text(strip=True) for cell in cells]
        if row:
            rows.append(row)

    try:
        #from tabulate import tabulate
        if headers and len(headers) == len(rows[0]):
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print(tabulate(rows, tablefmt="grid"))
    except ImportError:
        
        # Print using simple formatting
        if headers:
            return "\t".join(headers)
        for row in rows:
            return "\t".join(row)
        
    if __name__ == "__main__":
        if len(sys.argv) != 2:
            print("Usage: python bulletin_creation.py <CISA_Bulletin_URL>")
            print("Example: https://www.cisa.gov/news-events/bulletins/sb25-034")
            sys.exit(1)

scrape_cisa_table(sys.argv[1])
