# Clinic access review

A fictional outpatient clinic asks a reviewer to reconcile its account roster with approved job roles. The Python report identifies which accounts need a decision and names the permissions involved.

## Reproduce the review

From this directory, run `python review.py` with Python 3.9 or later. To inspect another roster with the same columns, run `python review.py roster.csv`. Permission names are space-separated. [Sample roster](roster.csv) · [Policy and review code](review.py) · [Saved findings](access-review-results.json)

## Analyst work sample

| Account | Finding | Decision for the reviewer |
| --- | --- | --- |
| demo-02 | A scheduler has chart.write in addition to calendar.read. | Verify the assignment with the role owner and request removal of chart.write if no exception exists. |
| demo-04 | A departed auditor retains audit.read. | Reconcile the departure record, then verify revocation in the identity system. |
| demo-05 | A contractor holds calendar.read but has no role in the policy. | Identify the sponsor and obtain a documented access decision. |

Four accounts pass the checks, including a departed clinician with zero grants. The fictional policy treats role permissions as a maximum. A clinician with read-only access therefore passes. The roster describes direct grants only. Nested groups, temporary exceptions, and recent changes would require additional evidence before taking action.
