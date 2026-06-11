"""
generate_data.py
----------------
Creates a realistic sample supplier dataset and saves it to data/sample_suppliers.csv.
Run this once to get started, or replace with your own CSV.

Expected CSV columns (if using your own data):
  supplier_id, supplier_name, orders_total, orders_on_time,
  avg_lead_time_days, promised_lead_time_days, defects_total, units_delivered
"""

import pandas as pd
import numpy as np
import os

SEED = 42
np.random.seed(SEED)

SUPPLIERS = [
    "Alpha Logistics GmbH",
    "Beta Components Ltd",
    "Gamma Supplies AG",
    "Delta Parts KG",
    "Epsilon Materials BV",
    "Zeta Freight SE",
    "Eta Industrial Co",
    "Theta Packaging Ltd",
    "Iota Raw Materials",
    "Kappa Tech Supplies",
]

def generate_supplier_data(n_suppliers=10, n_months=6):
    records = []
    for i, name in enumerate(SUPPLIERS[:n_suppliers]):
        # Vary quality tier per supplier
        tier = np.random.choice(["good", "average", "poor"], p=[0.4, 0.4, 0.2])

        if tier == "good":
            otd_rate     = np.random.uniform(0.88, 0.98)   # on-time delivery %
            lead_ratio   = np.random.uniform(0.95, 1.05)   # actual vs promised lead time
            defect_rate  = np.random.uniform(0.001, 0.010) # defects per unit
        elif tier == "average":
            otd_rate     = np.random.uniform(0.72, 0.87)
            lead_ratio   = np.random.uniform(1.05, 1.20)
            defect_rate  = np.random.uniform(0.010, 0.025)
        else:
            otd_rate     = np.random.uniform(0.50, 0.71)
            lead_ratio   = np.random.uniform(1.20, 1.60)
            defect_rate  = np.random.uniform(0.025, 0.060)

        orders_total          = int(np.random.uniform(80, 300) * n_months)
        orders_on_time        = int(orders_total * otd_rate)
        promised_lead_time    = int(np.random.choice([5, 7, 10, 14]))
        avg_lead_time_days    = round(promised_lead_time * lead_ratio, 1)
        units_delivered       = int(np.random.uniform(500, 3000) * n_months)
        defects_total         = int(units_delivered * defect_rate)

        records.append({
            "supplier_id":             f"SUP-{i+1:03d}",
            "supplier_name":           name,
            "orders_total":            orders_total,
            "orders_on_time":          orders_on_time,
            "promised_lead_time_days": promised_lead_time,
            "avg_lead_time_days":      avg_lead_time_days,
            "units_delivered":         units_delivered,
            "defects_total":           defects_total,
        })

    df = pd.DataFrame(records)
    return df


if __name__ == "__main__":
    df = generate_supplier_data()
    out_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_suppliers.csv")
    df.to_csv(out_path, index=False)
    print(f"Sample data saved → {out_path}")
    print(df.to_string(index=False))
