# Rebuttal Reproduction: Correcting Pit Bull Bite Risk Analysis

This repository contains a reproduction of the statistical corrections applied to the claim that Pit Bulls are "12.6x more likely to bite" than Maltese dogs in NYC (Cremieux).

## Overview

The original analysis (Cremieux) claimed a relative risk of **12.59x** for Pit Bulls compared to Maltese. This finding is derived from:
- **Numerator**: Reported bite incidents.
- **Denominator**: Licensed dog population.

However, this calculation fails to account for two significant, well-documented systematic biases:
1.  **Over-Identification**: Visual identification of Pit Bulls is notoriously unreliable.
2.  **Under-Registration**: Pit Bulls are significantly under-represented in licensing data due to breed-specific legislation and housing/insurance restrictions.

When these biases are corrected, the relative risk drops to **~2.5x** (conservative) or **~1.3x** (moderate).

## Methodology & Sources

### 1. Over-Identification Factor (2.5x)
**Source**: [Olson KR, Levy JK, et al. (2015). "Inconsistent identification of pit bull-type dogs by shelter staff." *The Veterinary Journal*.](http://www.sciencedirect.com/science/article/pii/S109002331500310X)
- **Finding**: Shelter staff visually identified **52%** of study dogs as Pit Bulls, but DNA analysis confirmed only **21%**.
- **Correction Factor**: $52 / 21 \approx 2.48$ (Rounded to **2.5x**).
- **Application**: The numerator (reported bites) is inflated by this factor.

### 2. Under-Registration Factor (2x - 4x)
**Source**: [NYC DOHMH Dog Licensing Data](https://data.cityofnewyork.us/Health/NYC-Dog-Licensing-Dataset/nu7n-tubp) vs. National Dog Population Estimates.
- **NYC Data**: Pit Bulls comprise **~5%** of licensed dogs (Cremieux's own data).
- **National Data**: Pit Bulls comprise **10-20%** of the actual dog population (various estimates).
- **Correction Factor**:
    - Conservative: $10\% / 5\% = \mathbf{2x}$
    - Moderate: $20\% / 5\% = \mathbf{4x}$
- **Application**: The denominator (population) is suppressed by this factor.

### Calculation Formula
$$ \text{Adjusted RR} = \frac{\text{Reported RR}}{\text{OverID} \times \text{UnderReg}} $$

## Getting Started

### Detailed Analysis
For a full breakdown of the validation process, including citations and arithmetic checks, please see [ANALYSIS.md](ANALYSIS.md).

### Prerequisites
- Python 3.x

### Running the Reproduction
Run the included script to perform the calculations:

```bash
python3 repro_calculations.py
```

### Expected Output
```text
Reported Relative Risk (RR): 12.59x

Scenario: Conservative (2x) Under-Registration
  Calculation: 12.59 / (2.5 * 2.0)
  Adjusted Risk: 2.52x

Scenario: Moderate (4x) Under-Registration
  Calculation: 12.59 / (2.5 * 4.0)
  Adjusted Risk: 1.26x
```

## Conclusion
The claim of a "12x" risk differential is an artifact of data bias. Correcting for these known biases brings the relative risk down to levels comparable to other breeds (e.g., ~1.3x), statistically indistinguishable from noise given the uncertainty ranges.
