#!/usr/bin/env python3
"""
Indiana Scraper
Source: Indiana MPH Open Data Portal
SourceType: CSV_DOWNLOAD
URL: https://hub.mph.in.gov/dataset/food-establishment-inspections
"""

import csv
import requests
import io
from datetime import datetime
from lib.schema import empty_record
from lib.priority import score_violations

# Direct CSV download URL from Indiana MPH open data
# Update this URL if Indiana changes their export endpoint
DOWNLOAD_URL = "https://hub.mph.in.gov/datastore/dump/food-establishment-inspections"

def fetch(source_url):
    """Fetch Indiana inspection data and return list of standardized records."""
    records = []

    try:
        response = requests.get(source_url, timeout=30)
        response.raise_for_status()
        reader = csv.DictReader(io.StringIO(response.text))

        for row in reader:
            rec = empty_record()
            rec['State'] = 'Indiana'
            rec['StateCode'] = 'IN'
            rec['County'] = row.get('COUNTY_NAME', '').strip().title()
            rec['Establishment'] = row.get('FACILITY_NAME', '').strip().title()
            rec['Address'] = row.get('ADDRESS', '').strip().title()
            rec['City'] = row.get('CITY', '').strip().title()
            rec['ZIP'] = row.get('ZIP', '').strip()[:5]
            rec['Phone'] = row.get('PHONE', '').strip()
            rec['LastInspection'] = row.get('INSPECTION_DATE', '').strip()
            rec['Priority'] = score_violations(row.get('VIOLATIONS', ''))
            rec['InspectionURL'] = source_url
            rec['LastUpdated'] = datetime.now().strftime('%Y-%m-%d')
            records.append(rec)

    except Exception as e:
        print(f"    Indiana fetch error: {e}")

    return records
