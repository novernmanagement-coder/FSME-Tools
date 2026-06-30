# ProctorHub Inspection Data Schema
# All scrapers must output records matching this structure

SCHEMA_COLUMNS = [
    'State',
    'StateCode',
    'County',
    'Establishment',
    'Address',
    'City',
    'ZIP',
    'Phone',
    'LastInspection',
    'Priority',        # High | Medium | Low | Review
    'InspectionURL',
    'LastUpdated',
]

def empty_record():
    return {col: '' for col in SCHEMA_COLUMNS}
