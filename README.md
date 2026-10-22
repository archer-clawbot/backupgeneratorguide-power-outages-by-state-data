# US Power Outage Burden by State, 2013–2025 (EIA-861 SAIDI/SAIFI and DOE-417 disturbance events)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23548861.svg)](https://doi.org/10.5281/zenodo.23548861)

Published by **Backup Generator Guide** (https://backupgeneratorguide.com/). This GitHub repository is a mirror; the canonical, versioned release is on Zenodo.

- **DOI:** [10.5281/zenodo.23548861](https://doi.org/10.5281/zenodo.23548861)
- **Zenodo record:** https://zenodo.org/records/23548861
- **Data page:** https://backupgeneratorguide.com/data/power-outages-by-state/
- **License:** CC BY 4.0 (see LICENSE)

## How to cite
Backup Generator Guide. *US Power Outage Burden by State, 2013–2025 (EIA-861 SAIDI/SAIFI and DOE-417 disturbance events)*. Zenodo. https://doi.org/10.5281/zenodo.23548861

---

---
license: cc-by-4.0
language:
- en
pretty_name: US Power Outage Burden by State (EIA-861 reliability + DOE-417 events, 2013–2025)
tags: [electricity, power-outages, reliability, saidi, saifi, united-states, backup-power]
configs:
- config_name: default
  data_files: state-reliability-saidi-saifi-2013-2025.csv
---

# US Power Outage Burden by State, 2013–2025

How many minutes of power the average electricity customer in each US state lost each year, and how often, with and without major storm days. Plus a state-by-year count of the large grid disturbances reported to the US Department of Energy.

Compiled by **Backup Generator Guide** ([backupgeneratorguide.com](https://backupgeneratorguide.com/)) from public-domain US government data. Every value comes from an unmodified federal file kept in `raw/`; nothing is estimated or filled in.

## At a glance
| | |
|---|---|
| Reliability coverage | 50 states + DC, data years 2013–2025 (13 years), 663 state-year rows |
| Utility rows | 13,155 utility-state-year records from EIA Form 861 |
| Disturbance events | 3,876 DOE-417 events, 2013–2025, summarised into 676 state-year rows (50 states + DC + PR) |
| Retrieved | October 21, 2026 |
| License | CC BY 4.0 for the compilation; underlying federal data are public domain |

## Files
| File | Rows | What it is |
|---|---|---|
| `state-reliability-saidi-saifi-2013-2025.csv` | 663 | **Main table.** Customer-weighted SAIDI/SAIFI per state per year, with and without major event days |
| `national-reliability-2013-2025.csv` | 13 | Same method across all reporting utilities, per year |
| `eia861-utility-reliability-2013-2025.csv` | 13,155 | Utility-level inputs as reported, with the standard used |
| `state-doe417-event-summary-2013-2025.csv` | 676 | DOE-417 event counts and reported customers affected, per state per year |
| `doe417-events-2013-2025.csv` | 3,876 | Event-level DOE-417 rows with parsed state codes |
| `doe417-unmatched-areas.csv` | 62 | Events whose "Area Affected" names no US state (Canada, utility names only, "Unknown"); excluded from state totals |
| `validation-vs-eia-state-totals.csv` | 153 | Our state figures next to EIA's own "State Totals" sheet (2023–2025) |
| `FINDINGS.md` | – | Short findings derived from the tables |
| `METHODS.md`, `DATA-DICTIONARY.md` | – | Method and column definitions |
| `src/build.py` | – | Script that rebuilds every CSV from `raw/` |
| `raw/` | – | Original downloads + `SOURCES.md` (URLs, dates, SHA-256) |

## Key terms
- **SAIDI**: average minutes without power per customer per year.
- **SAIFI**: average number of sustained interruptions per customer per year.
- **Major event days (MED)**: IEEE 1366 days with unusually high outage totals, usually big storms. "With MED" is everything a customer experienced; "without MED" is day-to-day reliability.

## Citation
Backup Generator Guide (2026). *US Power Outage Burden by State, 2013–2025* [Data set]. https://backupgeneratorguide.com/. Built from U.S. Energy Information Administration Form EIA-861 and U.S. Department of Energy Form DOE-417 data.

See `CITATION.cff`. Please also credit EIA and DOE as the original sources.

## Caveats (read before citing)
See METHODS.md. In short: utilities self-report, not every utility reports (coverage is listed per row), Puerto Rico and territories are not in the reliability table, DOE-417 reporting rules changed over time so event counts are not strictly comparable across years, and DOE-417 customer counts are utility estimates that can overlap.
