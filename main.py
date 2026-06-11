"""
main.py
-------
End-to-end runner for the Supplier KPI Tracker.

Usage:
    python main.py                         # uses generated sample data
    python main.py --input your_data.csv   # uses your own CSV

Your CSV must contain these columns:
    supplier_id, supplier_name, orders_total, orders_on_time,
    promised_lead_time_days, avg_lead_time_days,
    units_delivered, defects_total
"""

import argparse
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from generate_data import generate_supplier_data
from kpi_scoring import run_scoring
from export_report import export_report

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "output", "supplier_kpi_report.xlsx")
DATA_PATH   = os.path.join(os.path.dirname(__file__), "data", "sample_suppliers.csv")


def main():
    parser = argparse.ArgumentParser(description="Supplier KPI Tracker")
    parser.add_argument("--input", type=str, default=None,
                        help="Path to your own supplier CSV file (optional)")
    parser.add_argument("--output", type=str, default=OUTPUT_PATH,
                        help="Path for the Excel output file")
    args = parser.parse_args()

    # ── 1. Load or generate data ──────────────────────────────────────────────
    if args.input:
        print(f"Loading data from: {args.input}")
        df_raw = pd.read_csv(args.input)
    else:
        print("No input file specified — generating sample data...")
        df_raw = generate_supplier_data()
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        df_raw.to_csv(DATA_PATH, index=False)
        print(f"Sample data saved → {DATA_PATH}")

    print(f"\nSuppliers loaded: {len(df_raw)}")

    # ── 2. Score & rank suppliers ─────────────────────────────────────────────
    print("Calculating KPI scores...")
    df_scored = run_scoring(df_raw)

    # ── 3. Print summary to terminal ──────────────────────────────────────────
    display_cols = ["rank", "supplier_name", "otd_score", "ltc_score",
                    "defect_score", "composite_score", "tier"]
    print("\n" + "="*75)
    print("SUPPLIER KPI RESULTS")
    print("="*75)
    print(df_scored[display_cols].to_string(index=False))

    tier_summary = df_scored["tier"].value_counts()
    print("\nTier Summary:")
    for tier in ["A – Strategic", "B – Approved", "C – At Risk"]:
        count = tier_summary.get(tier, 0)
        print(f"  {tier}: {count} supplier(s)")
    print("="*75)

    # ── 4. Export Excel report ────────────────────────────────────────────────
    export_report(df_scored, args.output)
    print(f"\nDone! Open your report: {args.output}")


if __name__ == "__main__":
    main()
