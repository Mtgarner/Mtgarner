"""Review a synthetic clinic's access roster against a local policy."""
import argparse
import csv
import json
from pathlib import Path

ROLES = {
    "scheduler": {"calendar.read", "calendar.write"},
    "clinician": {"chart.read", "chart.write", "calendar.read"},
    "auditor": {"audit.read"},
}


def review(rows):
    findings = []
    for row in rows:
        user = row["account"]
        grants = set(row["grants"].split())
        status = row["status"]
        if status not in {"active", "departed"}:
            raise ValueError(f"Unknown status on {user}")
        if status == "departed":
            if grants:
                findings.append([user, "departed account retains access", sorted(grants)])
            continue
        role = row["role"]
        if role not in ROLES:
            findings.append([user, "role needs owner review", sorted(grants)])
            continue
        excess = grants - ROLES[role]
        if excess:
            findings.append([user, "outside approved role", sorted(excess)])
    return findings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roster", nargs="?", type=Path, default=Path(__file__).with_name("roster.csv"))
    with parser.parse_args().roster.open(newline="", encoding="utf-8") as stream:
        print(json.dumps(review(csv.DictReader(stream)), indent=2))
