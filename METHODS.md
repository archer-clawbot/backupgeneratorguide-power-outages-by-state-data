# Methods

## 1. EIA Form 861 reliability → state SAIDI/SAIFI
**Source:** the `Reliability_States` sheet in each year's EIA-861 zip, 2013–2025 (see raw/SOURCES.md). Each row is one utility in one state, reporting SAIDI and SAIFI with and without major event days (MED), plus its customer count, under the IEEE 1366 standard and/or an "Other" standard.

**Choosing a standard per row.** If a row has IEEE 1366 values (IEEE customer count > 0 and IEEE SAIDI-with-MED present), we use IEEE. Otherwise we use the "Other Standard" block if it has a customer count and SAIDI-with-MED. Rows with neither are kept in the utility file with `standard_used` blank and are not used. This mirrors EIA's "any standard" state totals. Values shown as "." in the source are treated as missing, never as zero.

**Aggregating to state.** For each state and year and each metric (SAIDI with MED, SAIFI with MED, SAIDI without MED, SAIFI without MED):

    state_metric = Σ(utility_metric × utility_customers) / Σ(utility_customers)

summed only over utilities that reported that metric. `customers_<metric>` gives the customer base behind each figure. `med_share_of_saidi_pct` is computed only on utilities reporting both SAIDI values: (SAIDI with MED − SAIDI without MED) / SAIDI with MED.

**Layout handling.** The 2019 file has an extra "Short Form" column, and 2024–2025 files have three header rows. The script checks the header labels before reading (it stops with an error if columns don't line up).

**Validation.** The 2023–2025 files include EIA's own `State Totals` sheet. `validation-vs-eia-state-totals.csv` compares the two. For 153 state-years the median absolute difference in SAIDI-with-MED is 0.03 minutes. A handful of 2025 states differ more (for example Missouri: our 457.2 vs EIA 369.1 minutes) because EIA's total uses a smaller customer base than the sum of the utility rows (1.47M vs 2.91M customers in Missouri). We have not been able to identify which utilities EIA leaves out, so we publish the utility-row aggregation and flag the gap rather than adjusting.

## 2. DOE-417 annual summaries → state event counts
**Source:** DOE-417 Annual Summary spreadsheets for 2013–2025. Each row is one reported electric emergency or disturbance with an "Area Affected" text field, event type, demand loss (MW) and number of customers affected.

**State assignment.** We match full state names (plus DC and Puerto Rico) in the "Area Affected" text, ignoring spaces and punctuation (the 2024–2025 files write names like "SouthDakota"). Longer names are matched first so "West Virginia" doesn't also count as "Virginia" and "Arkansas" not as "Kansas". One misspelling, "Connecicut", is mapped to CT. 62 events name no US state (Canadian provinces, utility names only, "Unknown") and are listed in `doe417-unmatched-areas.csv`. We don't guess a state for them.

**Counting.** An event touching several states counts once in each (`events_total`). Customer counts are summed **only for single-state events** (`customers_affected_single_state_sum`), because the source doesn't split multi-state totals by state. "Unknown"/blank customer values are missing, not zero. `events_weather` flags event types mentioning weather, storms, hurricanes, natural disasters, fire, ice, heat, wind, flood or earthquake.

**Comparability.** The DOE-417 form, its alert criteria and the summary file layout changed over the period (the files add an "Alert Criteria" column from 2015 and switch to a new system and layout for 2024). Some events are cyber/physical-security or system-operations alerts that don't involve customer outages. Year-over-year changes in event counts partly reflect reporting changes, not only grid conditions.

## 3. What we did not do
No imputation, interpolation or smoothing. No values from news reports or other secondary sources. Territories other than PR are not in the outputs (EIA reports them in a separate `Reliability_Territories` sheet, which we did not use).
