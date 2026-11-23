# Cloud workload anomaly triage

Can unusual activity volume help a reviewer prioritize cloud audit windows? This offline experiment models ten-minute windows for a fictional object-storage workload. Each window records object reads, denied API calls, and megabytes sent out.

## Reproduce the experiment

Run `python experiment.py` from this directory with Python 3.9 or later. The script uses the standard library and prints every decision alongside its scenario label. [Implementation](experiment.py) · [Saved run](cloud-triage-results.json)

1. Fit the reference distribution on [80 routine windows](reference.csv). Scale each feature by its reference standard deviation so transfer volume and call counts contribute on comparable scales.
2. Score a window by its mean distance to the three nearest reference windows. Choose the nearest-rank 95th percentile of [40 separate routine calibration scores](calibration.csv) as the alert threshold.
3. Freeze the reference set and threshold. Evaluate [24 held-out windows](evaluation.csv), using labels only to grade the predictions. Scores strictly above the threshold trigger review.

## Results and error analysis

| Decision on held-out data | Count |
| --- | ---: |
| Correct alert | 4 |
| Unnecessary alert | 1 |
| Correctly left unflagged | 18 |
| Missed review case | 1 |

Four of five alerts warranted review (80% precision). The detector caught four of the five labeled review cases (80% recall). Always predicting routine would catch zero of those five cases.

**Unnecessary alert.** Window evaluation-12 contains an approved monthly backfill. Its read volume is unusual, but the scenario provides a legitimate reason. A reviewer could check the change calendar.

**Missed case.** Window evaluation-16 contains an unauthorized read at ordinary volume. The model sees only counts and transfer size. Identity, resource sensitivity, and authorization records would help a reviewer investigate that case.

All records are synthetic. Routine values were sampled from bounded integer ranges, and selected evaluation windows were assigned scenarios. These results describe this fixture only. The script reads local CSV files and takes no action on cloud resources.
