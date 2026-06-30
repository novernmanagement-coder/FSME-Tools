#!/usr/bin/env python3
"""
healthinspections.us Shared Scraper
Used for counties on the healthinspections.us platform.
Pass the county subdomain URL e.g. https://madison-in.healthinspections.us
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from lib.schema import empty_record
from lib.priority import score_violations

def fetch(source_url, state='', state_code='', county=''):
    """Scrape a healthinspections.us county portal."""
    records = []

    try:
        # Search all establishments
        search_url = source_url.rstrip('/') + '/search'
        response = requests.get(search_url, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Parse establishment rows — structure varies slightly by county
        rows = soup.select('table.inspection-results tr')
        for row in rows[1:]:  # skip header
            cols = row.find_all('td')
            if len(cols) < 4:
                continue

            rec = empty_record()
            rec['State'] = state
            rec['StateCode'] = state_code
            rec['County'] = county
            rec['Establishment'] = cols[0].get_text(strip=True).title()
            rec['Address'] = cols[1].get_text(strip=True).title()
            rec['City'] = cols[2].get_text(strip=True).title()
            rec['ZIP'] = cols[3].get_text(strip=True)[:5]
            rec['LastInspection'] = cols[4].get_text(strip=True) if len(cols) > 4 else ''
            violations = cols[5].get_text(strip=True) if len(cols) > 5 else ''
            rec['Priority'] = score_violations(violations)
            rec['InspectionURL'] = source_url
            rec['LastUpdated'] = datetime.now().strftime('%Y-%m-%d')
            records.append(rec)

    except Exception as e:
        print(f"    healthinspections.us fetch error: {e}")

    return records
