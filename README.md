[README.md](https://github.com/user-attachments/files/28834992/README.md)
# Supplier KPI Tracker

A Python tool that scores, ranks, and reports on supplier performance across three operational KPIs — built to support procurement and supply chain decisions.

---

## What it does

1. **Loads supplier data** — from a CSV you provide, or generates realistic sample data
2. **Calculates three KPIs** per supplier:
   - On-Time Delivery Rate (OTD)
   - Lead Time Compliance (LTC) — actual vs. promised lead time
   - Defect Rate — defects per unit delivered
3. **Scores each KPI** (0–100) using min-max normalisation
4. **Applies weighted scoring** (OTD 45% | LTC 35% | Defect Rate 20%)
5. **Assigns supplier tiers**: A – Strategic / B – Approved / C – At Risk
6. **Exports a formatted Excel report** with colour-coded tiers and conditional formatting

---

## Quick start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/supplier-kpi-tracker.git
cd supplier-kpi-tracker

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run with sample data
python main.py

# 4. Open the report
open output/supplier_kpi_report.xlsx   # macOS
# or navigate to output/ in Explorer on Windows
```

---

## Using your own data

Prepare a CSV with these columns:

| Column | Description |
|---|---|
| `supplier_id` | Unique ID (e.g. SUP-001) |
| `supplier_name` | Supplier display name |
| `orders_total` | Total orders placed in period |
| `orders_on_time` | Orders delivered on or before due date |
| `promised_lead_time_days` | Agreed lead time (days) |
| `avg_lead_time_days` | Actual average lead time (days) |
| `units_delivered` | Total units received |
| `defects_total` | Units rejected / defective |

Then run:

```bash
python main.py --input path/to/your_suppliers.csv
```

---

## Scoring logic

```
OTD Score       = normalised(orders_on_time / orders_total)           × 45
LTC Score       = normalised(1 - |actual_lead_time / promised - 1|)   × 35
Defect Score    = normalised(1 - defect_rate)                          × 20

Composite Score = OTD Score + LTC Score + Defect Score   (0–100)
```

| Tier | Composite Score | Action |
|---|---|---|
| A – Strategic | ≥ 75 | Preferred supplier, consider long-term contracts |
| B – Approved | 50–74 | Monitor; set improvement targets |
| C – At Risk | < 50 | Escalate; review or replace |

---

## Project structure

```
supplier-kpi-tracker/
├── data/
│   └── sample_suppliers.csv       ← auto-generated input
├── output/
│   └── supplier_kpi_report.xlsx   ← generated report (git-ignored)
├── src/
│   ├── generate_data.py           ← sample data generator
│   ├── kpi_scoring.py             ← KPI calculation & scoring pipeline
│   └── export_report.py           ← Excel formatter
├── main.py                        ← entry point
├── requirements.txt
└── README.md
```

---

## Example output (terminal)

```
Suppliers loaded: 10

SUPPLIER KPI RESULTS
======================================================================
rank          supplier_name  otd_score  ltc_score  defect_score  composite_score           tier
   1     Alpha Logistics GmbH       92.4       88.1          97.2             92.0   A – Strategic
   2      Gamma Supplies AG         84.1       91.3          78.3             85.6   A – Strategic
   3  Epsilon Materials BV          71.2       75.5          85.0             74.9   B – Approved
...

Tier Summary:
  A – Strategic: 3 supplier(s)
  B – Approved:  5 supplier(s)
  C – At Risk:   2 supplier(s)
```

---

## Skills demonstrated

- **Python data pipeline** (pandas, numpy, openpyxl)
- **KPI design** — weighted scoring, normalisation, tiering
- **Supply chain domain knowledge** — OTD, lead time compliance, defect rate
- **Excel automation** — conditional formatting, colour-coded tiers, data validation
- **Lean methodology** — mirrors supplier review frameworks used in procurement

---

## Potential extensions

- [ ] Add trend analysis across multiple periods
- [ ] Integrate with SAP data export (CSV via MM60)
- [ ] Build a Power BI `.pbix` companion dashboard
- [ ] Add email alert for C-tier suppliers using `smtplib`
- [ ] Deploy as a Streamlit web app

---

## Author

**Karthik Nagaraju** — M.Sc. Supply Chain Management & Logistics, SRH University Hamm  
[linkedin.com/in/karthik-nagaraju](https://linkedin.com/in/karthik-nagaraju)
