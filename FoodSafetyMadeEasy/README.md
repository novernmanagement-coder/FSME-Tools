# ProctorHub Inspection Scraper

Pulls food establishment inspection data from state health department sources,
scores each establishment by priority, and outputs a standardized CSV.

## Structure

```
state_registry.csv          — master list of state data sources
master.py                   — runs all active state scrapers
lib/schema.py               — output column definitions
lib/priority.py             — scoring logic (internal, never exposed)
scrapers/in.py              — Indiana scraper
scrapers/_template.py       — template for new state scrapers
scrapers/_healthinspections_us.py — shared scraper for healthinspections.us counties
output/inspections.csv      — final output (committed to repo)
```

## Output Schema

| Column | Description |
|--------|-------------|
| State | Full state name |
| StateCode | Two-letter code |
| County | County name |
| Establishment | Business name |
| Address | Street address |
| City | City |
| ZIP | ZIP code |
| Phone | Phone number |
| LastInspection | Date of last inspection |
| Priority | High / Medium / Low / Review |
| InspectionURL | Source URL |
| LastUpdated | Date this record was last pulled |

## Priority Tiers

- **High** — go now
- **Medium** — go soon  
- **Low** — worth a visit eventually
- **Review** — needs more information

## Adding a New State

1. Add a row to `state_registry.csv` with Status = `Pending`
2. Copy `scrapers/_template.py` to `scrapers/[statecode].py`
3. Implement the `fetch()` function
4. Set Status = `Active` in the registry
5. Run `python master.py`

## Running

```bash
pip install requests beautifulsoup4
python master.py
```
