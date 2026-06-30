#!/usr/bin/env python3
"""
ProctorHub Inspection Data Master Script
Reads state_registry.csv, runs the appropriate scraper for each active state,
outputs to output/inspections.csv
"""

import csv
import os
import importlib
from datetime import datetime

REGISTRY_FILE = 'state_registry.csv'
OUTPUT_FILE = 'output/inspections.csv'

from lib.schema import SCHEMA_COLUMNS

def load_registry():
    with open(REGISTRY_FILE, newline='') as f:
        return list(csv.DictReader(f))

def run_scraper(state_row):
    state_code = state_row['StateCode'].lower()
    source_type = state_row['SourceType']
    source_url = state_row['SourceURL']

    scraper_path = f'scrapers.{state_code}'
    try:
        scraper = importlib.import_module(scraper_path)
        records = scraper.fetch(source_url)
        print(f"  ✓ {state_row['State']}: {len(records)} records")
        return records
    except ModuleNotFoundError:
        print(f"  ○ {state_row['State']}: no scraper yet (SourceType: {source_type})")
        return []
    except Exception as e:
        print(f"  ✗ {state_row['State']}: error — {e}")
        return []

def main():
    print(f"\nProctorHub Inspection Scraper — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    registry = load_registry()
    active = [r for r in registry if r['Status'] == 'Active']
    print(f"Active states: {len(active)} of {len(registry)}\n")

    all_records = []
    for state_row in active:
        records = run_scraper(state_row)
        all_records.extend(records)

    os.makedirs('output', exist_ok=True)
    with open(OUTPUT_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA_COLUMNS)
        writer.writeheader()
        writer.writerows(all_records)

    print(f"\nTotal records: {len(all_records)}")
    print(f"Output: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
