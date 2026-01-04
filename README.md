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
| **+ Bite Misattribution** | 2.5× over-ID, redistributed to lookalikes | **5.18×** (Rank #4) |
| **+ Pop 2× (Conservative)** | Above + 2× under-registration | **2.59×** |
| **+ Pop 4× (Evidence-Based)** | Above + 4× under-registration | **1.30×** |

### How Bite Redistribution Works

When we correct for the 2.5× over-identification, 3,793 bites are removed from pit bulls and redistributed to visually similar breeds proportionally by population:

| Breed | Original Bites | + Redistributed | New Total |
|-------|----------------|-----------------|-----------|
| Labrador Retriever | 659 | +1,644 | 2,303 |
| German Shepherd | 852 | +693 | 1,545 |
| Bull Terrier | 61 | +578 | 639 |
| Rottweiler | 404 | +128 | 532 |
| Boxer | 184 | +238 | 422 |
| **Pit Bull** | 6,321 | **−3,793** | **2,528** |

### After Bite Redistribution: New Rankings

| Rank | Original | After Correction |
|------|----------|------------------|
| 1 | Pit Bull (12.96×) | Rottweiler (7.91×) |
| 2 | Rottweiler (6.00×) | Mastiff (7.89×) |
| 3 | Mastiff (5.98×) | Doberman Pinscher (5.19×) |
| 4 | Chow Chow (4.61×) | **Pit Bull (5.18×)** |
| 5 | Akita (4.09×) | Cane Corso (5.06×) |

### Step-by-Step Math Verification

**Original (Cremieux)**
```
Pit Bull Risk = 6,321 / 21,739 = 0.2908
Maltese Risk  = 581 / 25,901 = 0.0224
Relative Risk = 0.2908 / 0.0224 = 12.96×
```

**After Bite Correction (redistribute 3,793 misattributed bites)**
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

> **Where do the misattributed bites come from?** The 3,793 bites misattributed to pit bulls came from visually similar breeds: Boxers, Bulldogs, Mastiffs, Bull Terriers, etc. A 4-7 lb white fluffy Maltese would never be misidentified as a 30-60 lb muscular pit bull, so the Maltese baseline remains valid for this comparison.

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
