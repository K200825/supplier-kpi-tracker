"""
kpi_scoring.py
--------------
Calculates three KPIs for each supplier, scores them 0-100,
applies weights, and assigns an overall tier (A / B / C).

KPIs:
  1. On-Time Delivery Rate   (OTD)   — higher is better
  2. Lead Time Compliance    (LTC)   — closer to 1.0 ratio is better
  3. Defect Rate             (DR)    — lower is better

Weights (must sum to 1.0):
  OTD = 0.45 | LTC = 0.35 | DR = 0.20
"""

import pandas as pd
import numpy as np

# ── Configurable weights ──────────────────────────────────────────────────────
WEIGHTS = {
    "otd_score":  0.45,
    "ltc_score":  0.35,
    "defect_score": 0.20,
}

# ── Tier thresholds (composite score 0-100) ──────────────────────────────────
TIER_THRESHOLDS = {
    "A": 75,   # Strategic / preferred
    "B": 50,   # Approved / monitor
    # below 50 → C: At-risk / review
}


def calc_kpi_raw(df: pd.DataFrame) -> pd.DataFrame:
    """Add raw KPI columns derived from the source data."""
    df = df.copy()

    # 1. On-Time Delivery Rate  (0.0 – 1.0)
    df["otd_rate"] = df["orders_on_time"] / df["orders_total"]

    # 2. Lead Time Ratio  (actual / promised; 1.0 = perfect, >1 = late)
    df["lead_time_ratio"] = df["avg_lead_time_days"] / df["promised_lead_time_days"]

    # 3. Defect Rate  (defects per unit delivered)
    df["defect_rate"] = df["defects_total"] / df["units_delivered"]

    return df


def score_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert raw KPIs to 0-100 scores using min-max normalisation,
    then compute a weighted composite score.
    """
    df = df.copy()

    # ── OTD score: higher rate → higher score ────────────────────────────────
    otd_min, otd_max = df["otd_rate"].min(), df["otd_rate"].max()
    if otd_max > otd_min:
        df["otd_score"] = (df["otd_rate"] - otd_min) / (otd_max - otd_min) * 100
    else:
        df["otd_score"] = 100.0

    # ── LTC score: ratio closer to 1.0 → higher score ────────────────────────
    # Penalise both late (>1) and unexpectedly early (<0.8)
    df["ltc_penalty"] = (df["lead_time_ratio"] - 1.0).abs()
    pen_min, pen_max = df["ltc_penalty"].min(), df["ltc_penalty"].max()
    if pen_max > pen_min:
        df["ltc_score"] = 100 - (df["ltc_penalty"] - pen_min) / (pen_max - pen_min) * 100
    else:
        df["ltc_score"] = 100.0

    # ── Defect score: lower defect rate → higher score ────────────────────────
    dr_min, dr_max = df["defect_rate"].min(), df["defect_rate"].max()
    if dr_max > dr_min:
        df["defect_score"] = 100 - (df["defect_rate"] - dr_min) / (dr_max - dr_min) * 100
    else:
        df["defect_score"] = 100.0

    # ── Composite weighted score ──────────────────────────────────────────────
    df["composite_score"] = (
        df["otd_score"]     * WEIGHTS["otd_score"] +
        df["ltc_score"]     * WEIGHTS["ltc_score"] +
        df["defect_score"]  * WEIGHTS["defect_score"]
    ).round(1)

    return df


def assign_tiers(df: pd.DataFrame) -> pd.DataFrame:
    """Add a tier label and rank column based on composite score."""
    df = df.copy()

    def _tier(score):
        if score >= TIER_THRESHOLDS["A"]:
            return "A – Strategic"
        elif score >= TIER_THRESHOLDS["B"]:
            return "B – Approved"
        else:
            return "C – At Risk"

    df["tier"] = df["composite_score"].apply(_tier)
    df["rank"] = df["composite_score"].rank(ascending=False, method="min").astype(int)
    df = df.sort_values("rank").reset_index(drop=True)

    return df


def run_scoring(df: pd.DataFrame) -> pd.DataFrame:
    """Full pipeline: raw KPIs → scores → tiers."""
    df = calc_kpi_raw(df)
    df = score_kpis(df)
    df = assign_tiers(df)
    return df


if __name__ == "__main__":
    # Quick smoke-test
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    sample_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_suppliers.csv")
    raw = pd.read_csv(sample_path)
    scored = run_scoring(raw)
    cols = ["rank", "supplier_name", "otd_score", "ltc_score",
            "defect_score", "composite_score", "tier"]
    print(scored[cols].to_string(index=False))
