#!/usr/bin/env python3
import sys
import requests
from bs4 import BeatifulSoup
from tabulate import tabulate

def scrap_cisa_table(url):
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