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

| Scenario | Correction | Pit Bull RR |
|----------|------------|-------------|
| **Cremieux Original** | None | **12.96×** |
| **+ Bite Misattribution** | 2.5× over-ID, redistributed to lookalikes + Unknown | **5.18×** (Rank #3) |
| **+ Pop 2× (Conservative)** | Above + 2× under-registration | **2.59×** |
| **+ Pop 4× (Evidence-Based)** | Above + 4× under-registration | **1.30×** |

### What This Means

With corrections applied, pit bulls have a relative risk of **1.30× - 2.59×**, which is:
- **Less than** Mastiff (8.49×), Rottweiler (8.52×), Doberman (4.67×), and Chow Chow (4.61×)
- **Still 1.5-3× higher** than low-risk breeds like Shih Tzu (0.85×) or Maltese (1.0× baseline)

The corrected risk places pit bulls in the **middle of the pack**, not as extreme outliers.

### How Bite Redistribution Works

When we correct for the 2.5× over-identification, 3,793 bites are removed from pit bulls and redistributed to big dogs + Unknown proportionally **by their original bite counts**:

| Category | Original Bites | Share | + Redistributed |
|----------|----------------|-------|-----------------|
| Unknown | 6,206 | 64.9% | +2,462 |
| German Shepherd | 852 | 8.9% | +338 |
| Siberian Husky | 505 | 5.3% | +200 |
| Rottweiler | 404 | 4.2% | +170 |
| Labrador Retriever | 659 | 6.9% | +277 |
| **Pit Bull** | 6,321 | — | **−3,793** |

### After Bite Redistribution: New Rankings

| Rank | Original | After Correction |
|------|----------|------------------|
| 1 | Pit Bull (12.96×) | Rottweiler (8.52×) |
| 2 | Rottweiler (6.00×) | Mastiff (8.49×) |
| 3 | Mastiff (5.98×) | **Pit Bull (5.18×)** |
| 4 | Chow Chow (4.61×) | Doberman Pinscher (4.67×) |
| 5 | Akita (4.09×) | Chow Chow (4.61×) |

### Step-by-Step Math Verification

**Original (Cremieux)**
```
Pit Bull Risk = 6,321 / 21,739 = 0.2908
Maltese Risk  = 581 / 25,901 = 0.0224
Relative Risk = 0.2908 / 0.0224 = 12.96×
```

**After Bite Correction (redistribute to lookalikes + Unknown by bite share)**
```
True Pit Bull Bites = 6,321 / 2.5 = 2,528
Pit Bull Risk = 2,528 / 21,739 = 0.1163
Relative Risk = 0.1163 / 0.0224 = 5.18×
```

**+ Population Correction (2×)**
```
True Pit Bull Pop = 21,739 × 2 = 43,478
Pit Bull Risk = 2,528 / 43,478 = 0.0582
Relative Risk = 0.0582 / 0.0224 = 2.59×
```

**+ Population Correction (4×)**
```
True Pit Bull Pop = 21,739 × 4 = 86,956
Pit Bull Risk = 2,528 / 86,956 = 0.0291
Relative Risk = 0.0291 / 0.0224 = 1.30×
```

> **Why Maltese is unchanged**: Maltese are not commonly misidentified as other breeds, and Maltese owners don't face breed-specific registration barriers.

> **Why include Unknown?** Most misattributed bites go to Unknown (65%) because when a dog isn't easily identified, it's often called a pit bull. The redistribution reflects that many "pit bull" reports should have been "unknown."

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
