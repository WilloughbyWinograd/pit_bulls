# Correcting Cremieux's Pit Bull Risk Analysis

## Executive Summary

Cremieux claims pit bulls have a **12.59× relative risk** of biting compared to Maltese dogs. This analysis shows that when corrected for documented biases in breed identification and population estimates, the true relative risk drops to **1.26× to 2.52×**—a far less dramatic difference that falls within normal breed variation.

---

## Cremieux's Original Claim

| Metric | Value |
|--------|-------|
| Pit Bull Bites | 6,053 |
| Pit Bull Licenses | 21,915 |
| Maltese Bites | 469 |
| Maltese Licenses | 21,363 |
| **Relative Risk** | **12.59×** |

---

## Problem 1: Bite Over-Identification (2.5× Bias)

### The Issue

The NYC Department of Health states explicitly that breed information in the bite data *"has not been verified by DOHMH and is listed only as reported."* The breed is whatever the reporter says—no DNA test, no verification.

Cremieux dismisses this concern, claiming pit bulls are "easy to identify." **He is wrong.**

### The Evidence

A peer-reviewed study ([Olson et al., 2015](https://www.sciencedirect.com/science/article/pii/S109002331500310X)) tested this directly:
- **Trained animal shelter staff** visually identified 120 dogs
- Researchers then verified with **DNA testing**
- Staff identified **52%** as pit bulls
- DNA showed only **21%** actually were

**Result: Professionals over-identified pit bulls by 2.5×**

Bite victims are not trained professionals and are often in adrenaline-charged situations, making them likely **even less accurate** at breed identification.

### Correction Factor

> **Divide reported pit bull bites by 2.5**

---

## Problem 2: Population Under-Counting (2× to 4× Bias)

### The Issue

Cremieux uses licensing data as a proxy for population, testing robustness against only a 5% differential. **That's far too small.**

### The Evidence

1. **Low overall compliance**: Only ~20% of NYC dogs are licensed
2. **Pit bull-specific disincentives**: As Cremieux himself admits, pit bull owners face unique pressures to avoid registration:
   - Housing bans
   - Breed-specific legislation
   - Insurance exclusions
3. **Population mismatch**: 
   - Pit bulls are <5% of NYC licenses (per Cremieux)
   - National estimates indicate pit bulls are **10-20%** of the dog population
   - DNA studies suggest at least **14%**

### Correction Factor

> **Multiply pit bull population by 2× to 4×**

---

## The Corrected Calculations

### Formula

```
Corrected Pit Bull Risk = (Reported Bites ÷ 2.5) ÷ (Reported Population × N)
                        = Reported Risk ÷ (2.5 × N)

Corrected Relative Risk = Original RR ÷ (2.5 × N)
```

Where N = population under-count factor (2, 2.5, or 4)

### Results

| Scenario | Bite Correction | Population Correction | Combined Factor | Corrected Relative Risk |
|----------|-----------------|----------------------|-----------------|------------------------|
| **Original (Cremieux)** | 1× | 1× | 1× | **12.59×** |
| **Conservative** | 2.5× | 2× | 5× | **2.52×** |
| **Evidence-Based** | 2.5× | 4× | 10× | **1.26×** |

---

## Detailed Calculations

### Scenario 1: Conservative (2× population under-count)

```
True Pit Bull Bites = 6,053 ÷ 2.5 = 2,421
True Pit Bull Population = 21,915 × 2 = 43,830
True Pit Bull Risk = 2,421 ÷ 43,830 = 0.0552

Maltese Risk = 469 ÷ 21,363 = 0.0220 (unchanged)

Corrected Relative Risk = 0.0552 ÷ 0.0220 = 2.52×
```

### Scenario 2: Evidence-Based (4× population under-count)

```
True Pit Bull Bites = 6,053 ÷ 2.5 = 2,421
True Pit Bull Population = 21,915 × 4 = 87,660
True Pit Bull Risk = 2,421 ÷ 87,660 = 0.0276

Corrected Relative Risk = 0.0276 ÷ 0.0220 = 1.26×
```

---

## Visualizing the Correction

```
Cremieux's Claim:     ████████████████████████████████████████████████████ 12.59×

Conservative (2×):    ██████████ 2.52×

Evidence-Based (4×):  █████ 1.26×
```

---

## Conclusion

Cremieux's "12.59× relative risk" is based on:
1. **Unverified breed identification** that research shows over-counts pit bulls by 2.5×
2. **Licensing data** that dramatically under-counts pit bull population due to breed-specific registration avoidance

When corrected for these documented biases, the relative risk drops to **1.26× to 2.52×**—a range that:
- Is **5-10× smaller** than claimed
- Falls within normal variation among dog breeds
- Does not support breed-specific legislation

---

## References

1. Olson KR, Levy JK, Norby B, Crandall MM, Broadhurst JE, Jacks S, Barber RC, Griffin KE. (2015). "Inconsistent identification of pit bull-type dogs by shelter staff." *The Veterinary Journal*, 206(2):197-202. [DOI: 10.1016/j.tvjl.2015.07.019](https://www.sciencedirect.com/science/article/pii/S109002331500310X)

2. NYC Department of Health and Mental Hygiene. Dog Bite Data documentation: *"Breed has not been verified by DOHMH and is listed only as reported."*

3. Patronek GJ, Sacks JJ, Delise KM, Cleary DV, Marder AR. (2013). "Co-occurrence of potentially preventable factors in 256 dog bite-related fatalities in the United States (2000-2009)." *Journal of the American Veterinary Medical Association*, 243(12):1726-1736.
