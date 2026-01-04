# Reproducing and Correcting Cremieux's Pit Bull Analysis

This repository reproduces the dog bite risk analysis from Cremieux's "The Dogs of New York" (June 2024), then shows how his **12.59× relative risk** claim changes when corrected for documented biases in breed identification and population estimates.

## Key Findings

| Analysis | Relative Risk |
|----------|---------------|
| **Cremieux's Original Claim** | 12.59× |
| **Our Reproduction** (same methodology, current data) | 12.73× |
| **Corrected for Biases** (conservative) | 2.52× |
| **Corrected for Biases** (evidence-based) | 1.26× |

**Bottom line**: When corrected for documented over-identification of pit bulls in bite reports (2.5×) and under-registration in licensing data (2-4×), the relative risk drops by 80-90%.

---

## Part 1: Reproducing Cremieux's Analysis

### Methodology

We exactly replicated Cremieux's methodology:
- **Data sources**: NYC DOHMH Dog Licensing and Dog Bite datasets
- **Date ranges**: Bites (Jan 2015 - Dec 2022), Licenses (Sept 2014 - Nov 2023)
- **Breed classifications**: Used his exact breed strings from the PDF footnotes
- **Baseline**: Maltese dogs (including Maltese Crossbreed)

### Results

| Metric | Cremieux | Reproduction |
|--------|----------|--------------|
| Pit Bull Bites | 6,053 | 6,208 |
| Pit Bull Licenses | 21,915 | 21,739 |
| Maltese Bites | 469 | 581 |
| Maltese Licenses | 21,363 | 25,901 |
| **Relative Risk** | **12.59×** | **12.73×** |

The small difference (12.73× vs 12.59×) is due to data updates between his Feb 2024 snapshot and our Jan 2026 data.

**Script**: [`cremieux_analysis.py`](cremieux_analysis.py)

---

## Part 2: Correcting for Known Biases

### Problem 1: Bite Over-Identification (2.5×)

The NYC Department of Health states breed information *"has not been verified and is listed only as reported."* 

Research shows pit bulls are systematically over-identified:
- [Olson et al. (2015)](https://www.sciencedirect.com/science/article/pii/S109002331500310X): Trained shelter staff identified 52% of dogs as pit bulls; DNA showed only 21% actually were
- **Over-identification factor: 2.5×**

### Problem 2: Population Under-Registration (2-4×)

Cremieux uses licensing data as population proxy, but:
- Only ~20% of NYC dogs are licensed
- Pit bull owners face unique disincentives: housing bans, breed-specific laws, insurance exclusions
- Pit bulls are <5% of licenses but 10-20% of national dog population (per DNA studies)
- **Under-registration factor: 2-4×**

### Corrected Results

| Scenario | Bite Correction | Population Correction | Corrected Risk |
|----------|-----------------|----------------------|----------------|
| Original | 1× | 1× | 12.59× |
| Conservative | 2.5× | 2× | **2.52×** |
| Evidence-Based | 2.5× | 4× | **1.26×** |

**Full analysis**: [`corrected_risk_analysis.md`](corrected_risk_analysis.md)

---

## Repository Contents

| File | Description |
|------|-------------|
| `cremieux_analysis.py` | Script reproducing Cremieux's exact methodology |
| `corrected_risk_analysis.md` | Analysis showing impact of bias corrections |
| `The_Dogs_of_New_York.pdf` | Original Cremieux article |
| `pdf_images/` | Extracted images showing his classification rules |

---

## Data Sources

- **Dog Bite Data**: [NYC Open Data - DOHMH Dog Bite Data](https://data.cityofnewyork.us/Health/DOHMH-Dog-Bite-Data/rsgh-akpg)
- **Dog Licensing Data**: [NYC Open Data - Dog Licensing Dataset](https://data.cityofnewyork.us/Health/NYC-Dog-Licensing-Dataset/nu7n-tubp)

---

## Running the Analysis

```bash
# Reproduce Cremieux's analysis
python3 cremieux_analysis.py
```

Output:
```
RELATIVE RISK:    12.73×
(Cremieux's claim: 12.59×)
```

---

## References

1. Cremieux. "The Dogs of New York." June 29, 2024.
2. Olson KR, et al. (2015). "Inconsistent identification of pit bull-type dogs by shelter staff." *The Veterinary Journal*, 206(2):197-202.
3. NYC Department of Health and Mental Hygiene. Dog Bite Data documentation.
