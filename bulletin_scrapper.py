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