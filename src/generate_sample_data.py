"""
Generate a synthetic, illustrative dataset of state-level education indicators
for India.

IMPORTANT: These numbers are SYNTHETIC and meant only to make the analysis
pipeline runnable out of the box. They are loosely inspired by the real shape of
Indian education data but are NOT official figures. Before publishing any
findings, replace this file with real data from:
  - Census of India (censusindia.gov.in)
  - UDISE+ (udiseplus.gov.in)
  - NSSO / Periodic Labour Force Survey
  - UNESCO Institute for Statistics (uis.unesco.org)
"""

import numpy as np
import pandas as pd
from pathlib import Path

rng = np.random.default_rng(42)

states = [
    "Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh", "Delhi", "Gujarat",
    "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Odisha", "Punjab", "Rajasthan",
    "Tamil Nadu", "Telangana", "Uttar Pradesh", "Uttarakhand", "West Bengal",
]

# A rough "development tier" per state to make correlations realistic.
# 0 = higher indicators, 2 = more challenged. Purely illustrative.
tier = {
    "Kerala": 0, "Delhi": 0, "Himachal Pradesh": 0, "Tamil Nadu": 0,
    "Punjab": 0, "Uttarakhand": 0, "Maharashtra": 0, "Gujarat": 1,
    "Karnataka": 1, "Haryana": 1, "Telangana": 1, "Andhra Pradesh": 1,
    "West Bengal": 1, "Odisha": 1, "Assam": 2, "Chhattisgarh": 2,
    "Jharkhand": 2, "Madhya Pradesh": 2, "Rajasthan": 2, "Bihar": 2,
    "Uttar Pradesh": 2,
}

rows = []
for year in [2011, 2015, 2019, 2023]:
    year_lift = (year - 2011) * 0.9  # literacy generally improves over time
    for s in states:
        t = tier[s]
        base = 88 - t * 9 + rng.normal(0, 2.0) + year_lift
        male_lit = float(np.clip(base + rng.normal(4, 1.2), 40, 99))
        female_lit = float(np.clip(base - rng.normal(6, 2.0), 30, 99))
        overall_lit = round((male_lit + female_lit) / 2, 1)

        dropout = float(np.clip(4 + t * 4 + rng.normal(0, 1.2) - year_lift * 0.15, 0.5, 30))
        ptr = float(np.clip(24 + t * 6 + rng.normal(0, 2.5) - year_lift * 0.1, 12, 60))
        gross_enroll = float(np.clip(102 - t * 5 + rng.normal(0, 3) + year_lift * 0.3, 60, 115))

        rows.append({
            "state": s,
            "year": year,
            "literacy_overall": overall_lit,
            "literacy_male": round(male_lit, 1),
            "literacy_female": round(female_lit, 1),
            "gender_gap": round(male_lit - female_lit, 1),
            "dropout_rate_secondary": round(dropout, 1),
            "pupil_teacher_ratio": round(ptr, 1),
            "gross_enrollment_ratio": round(gross_enroll, 1),
        })

df = pd.DataFrame(rows)
out = Path(__file__).resolve().parents[1] / "data" / "india_education_sample.csv"
df.to_csv(out, index=False)
print(f"Wrote {len(df)} rows to {out}")
