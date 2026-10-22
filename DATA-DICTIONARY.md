# Data dictionary

## state-reliability-saidi-saifi-2013-2025.csv
| Column | Meaning |
|---|---|
| year | EIA data year |
| state, state_name | USPS code / name (50 states + DC) |
| utilities_reporting | utility rows used (any standard) |
| utilities_ieee | of those, rows on IEEE 1366 |
| customers_covered | sum of customers of utilities used |
| saidi_med | customer-weighted SAIDI incl. major event days (minutes/customer/year) |
| saifi_med | customer-weighted SAIFI incl. major event days (interruptions/customer/year) |
| saidi_nomed / saifi_nomed | same, excluding major event days |
| customers_saidi_med … customers_saifi_nomed | customer base behind each metric |
| med_share_of_saidi_pct | % of SAIDI-with-MED due to major event days (utilities reporting both) |
| saidi_med_hours | saidi_med / 60 |
| rank_saidi_med_in_year | 1 = most outage minutes that year (of 51) |
| source | source file |

## national-reliability-2013-2025.csv
year, utilities_reporting, customers_covered, saidi_med, saifi_med, saidi_nomed, saifi_nomed (same method, all states pooled).

## eia861-utility-reliability-2013-2025.csv
year, state, utility_id (EIA utility number), utility_name, ownership, standard_used (IEEE / Other / blank = unusable), customers, saidi_med, saifi_med, saidi_nomed, saifi_nomed (the values used), then the raw `ieee_*` and `oth_*` columns as reported (missing = blank).

## state-doe417-event-summary-2013-2025.csv
| Column | Meaning |
|---|---|
| year, state, state_name | 50 states + DC + PR, every combination listed (zeros are real zeros among matched events) |
| events_total | DOE-417 events naming the state |
| events_weather | subset with a weather/natural-hazard event type |
| events_single_state / events_multi_state | split by number of states named |
| events_customers_reported | single-state events with a numeric customer count |
| customers_affected_single_state_sum | sum of reported customers affected, single-state events only (can double count customers hit by several events) |
| max_customers_single_event | largest reported customer count among events naming the state (blank if none reported) |

## doe417-events-2013-2025.csv
year, date_began, area_affected (verbatim), states (parsed, ";"-separated), n_states, event_type (verbatim), demand_loss_mw, customers_affected (numeric or blank), customers_affected_raw (verbatim), source_file, weather (flag).

## validation-vs-eia-state-totals.csv
year, state, eia_any_customers, our_customers, eia_any_saidi_med, our_saidi_med, eia_any_saidi_nomed, our_saidi_nomed.
