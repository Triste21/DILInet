#!/usr/bin/env python3
"""Load, validate, split, and visualize the curated DILInet label files.

This repository ships the curated DHLD and DRCD sample identifiers and labels
used in the paper (label ``1`` = drug-induced, ``0`` = spontaneous). No model
code is released, so this utility exercises the data that *is* available: it
sanity-checks the label distributions against the numbers reported in the
paper, produces a reproducible slide-level stratified train/val/test split
(~7:1:2), and renders the class distribution as a figure.

Run:  python scripts/analyze_labels.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless-safe backend
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split

REPO_ROOT = Path(__file__).resolve().parent.parent

# Sample counts reported in README.md (drug-induced / spontaneous).
EXPECTED = {
    "DHLD": {"total": 617, "drug_induced": 377, "spontaneous": 240},
    "DRCD": {"total": 405, "drug_induced": 215, "spontaneous": 190},
}

LABEL_NAMES = {1: "drug-induced", 0: "spontaneous"}


def load_labels(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    expected_cols = {"slide_id", "label"}
    if set(df.columns) != expected_cols:
        raise ValueError(f"{csv_path.name}: expected columns {expected_cols}, got {set(df.columns)}")
    if not set(df["label"].unique()) <= {0, 1}:
        raise ValueError(f"{csv_path.name}: labels must be binary 0/1")
    if df["slide_id"].duplicated().any():
        raise ValueError(f"{csv_path.name}: duplicate slide_id values found")
    return df


def summarize(name: str, df: pd.DataFrame) -> dict[str, int]:
    counts = df["label"].value_counts().to_dict()
    summary = {
        "total": len(df),
        "drug_induced": int(counts.get(1, 0)),
        "spontaneous": int(counts.get(0, 0)),
    }
    exp = EXPECTED[name]
    status = "OK" if summary == exp else "MISMATCH"
    balance = summary["drug_induced"] / summary["total"]
    print(f"[{name}] total={summary['total']:>4}  "
          f"drug-induced={summary['drug_induced']:>4}  "
          f"spontaneous={summary['spontaneous']:>4}  "
          f"pos_rate={balance:.3f}  vs paper={exp}  -> {status}")
    if status != "OK":
        raise AssertionError(f"{name}: label counts {summary} do not match paper {exp}")
    return summary


def make_split(df: pd.DataFrame, seed: int = 42) -> dict[str, pd.DataFrame]:
    """Stratified slide-level split ~7:1:2 (train:val:test)."""
    train, temp = train_test_split(
        df, test_size=0.30, stratify=df["label"], random_state=seed
    )
    val, test = train_test_split(
        temp, test_size=2 / 3, stratify=temp["label"], random_state=seed
    )
    return {"train": train, "val": val, "test": test}


def plot_distribution(summaries: dict[str, dict[str, int]], out_path: Path) -> None:
    datasets = list(summaries.keys())
    drug = [summaries[d]["drug_induced"] for d in datasets]
    spont = [summaries[d]["spontaneous"] for d in datasets]

    x = range(len(datasets))
    width = 0.38
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar([i - width / 2 for i in x], drug, width, label=LABEL_NAMES[1], color="#c44e52")
    ax.bar([i + width / 2 for i in x], spont, width, label=LABEL_NAMES[0], color="#4c72b0")
    ax.set_xticks(list(x))
    ax.set_xticklabels(datasets)
    ax.set_ylabel("Number of slides")
    ax.set_title("DILInet curated label distribution")
    for i, (d, s) in enumerate(zip(drug, spont)):
        ax.text(i - width / 2, d + 5, str(d), ha="center", va="bottom", fontsize=9)
        ax.text(i + width / 2, s + 5, str(s), ha="center", va="bottom", fontsize=9)
    ax.legend()
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=120)
    print(f"[plot] wrote label distribution figure -> {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42, help="random seed for the split")
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "outputs" / "label_distribution.png",
        help="output path for the distribution figure",
    )
    args = parser.parse_args()

    files = {"DHLD": REPO_ROOT / "DHLD_label.csv", "DRCD": REPO_ROOT / "DRCD_label.csv"}
    summaries: dict[str, dict[str, int]] = {}

    for name, path in files.items():
        df = load_labels(path)
        summaries[name] = summarize(name, df)
        splits = make_split(df, seed=args.seed)
        parts = "  ".join(
            f"{k}={len(v)} (pos={int(v['label'].sum())})" for k, v in splits.items()
        )
        print(f"[{name}] stratified split (~7:1:2, seed={args.seed}):  {parts}")

    plot_distribution(summaries, args.out)
    print("\nAll label files loaded, validated, split, and visualized successfully.")


if __name__ == "__main__":
    main()
