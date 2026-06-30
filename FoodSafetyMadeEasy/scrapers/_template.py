#!/usr/bin/env python3
"""
[STATE NAME] Scraper — TEMPLATE
Copy this file, rename to [statecode].py, fill in the fetch() function.
SourceType: [CSV_DOWNLOAD | API | HTML_TABLE | HEALTHINSPECTIONS]
"""

import requests
from datetime import datetime
from lib.schema import empty_record
from lib.priority import score_violations

def fetch(source_url):
    """Fetch [STATE] inspection data and return list of standardized records."""
    records = []

    # TODO: implement fetch logic for this state
    # Each record must use empty_record() and populate SCHEMA_COLUMNS
    # Priority must be set using score_violations(violation_text)

    return records
