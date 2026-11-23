"""Fit a nearest-neighbor detector to synthetic cloud workload telemetry."""
import csv
import json
import math
from pathlib import Path
from statistics import mean, stdev

ROOT = Path(__file__).parent
FEATURES = ("object_reads", "denied_calls", "egress_mb")


def read_samples(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def vector(row):
    return tuple(float(row[key]) for key in FEATURES)


def experiment():
    training = [vector(row) for row in read_samples("reference.csv")]
    scales = [stdev(col) or 1 for col in zip(*training)]

    def score(point):
        distances = sorted(math.sqrt(sum(((a - b) / s) ** 2
                           for a, b, s in zip(point, neighbor, scales))) for neighbor in training)
        return mean(distances[:3])

    calibration = sorted(score(vector(row)) for row in read_samples("calibration.csv"))
    threshold = calibration[math.ceil(0.95 * len(calibration)) - 1]
    counts = dict(true_positive=0, false_positive=0, true_negative=0, false_negative=0)
    decisions = []
    for row in read_samples("evaluation.csv"):
        distance = score(vector(row))
        flagged = distance > threshold
        incident = row["label"] == "review"
        outcome = ("true_" if flagged == incident else "false_") + ("positive" if flagged else "negative")
        counts[outcome] += 1
        decisions.append(dict(window=row["window"], score=round(distance, 3),
                              flagged=flagged, expected=row["label"], context=row["context"]))
    return dict(threshold=round(threshold, 3), counts=counts, decisions=decisions)


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2))
