# Dog Bite Analysis Report

Analysis recreating findings from 'The Dogs of New York' using both Bite and Licensing data.

## Risk Analysis Findings
### Pit Bull vs. Maltese Relative Risk
- **Pit Bull Risk**: 0.7389 bites per license
- **Maltese Risk**: 0.0820 bites per license
- **Relative Risk**: **9.01x**

> This calculates how much more likely a Pit Bull is to bite compared to a Maltese, given their registered populations.
> **Verification**: The original article claims ~12.59x. Our calculated value is 9.01x.

## Top 20 High-Risk Breeds
| Rank | Breed | Risk (Bites/License) | Bites | Licenses |
|---|---|---|---|---|
| 1 | Pit Bull | 0.7389 | 6329 | 8565 |
| 2 | Mastiff | 0.5907 | 140 | 237 |
| 3 | Rottweiler | 0.5647 | 406 | 719 |
| 4 | Akita | 0.3636 | 72 | 198 |
| 5 | Chow Chow | 0.3381 | 95 | 281 |
| 6 | Collie, Border | 0.3083 | 41 | 133 |
| 7 | Cane Corso | 0.2801 | 79 | 282 |
| 8 | Doberman Pinscher | 0.2716 | 88 | 324 |
| 9 | Belgian Malinois | 0.1979 | 38 | 192 |
| 10 | Bull Terrier | 0.1950 | 55 | 282 |
| 11 | Siberian Husky | 0.1868 | 500 | 2676 |
| 12 | Great Dane | 0.1780 | 47 | 264 |
| 13 | Dalmatian | 0.1734 | 30 | 173 |
| 14 | West High White Terrier | 0.1477 | 44 | 298 |
| 15 | German Shepherd | 0.1433 | 1149 | 8019 |
| 16 | Dachshund Smooth Coat | 0.1392 | 70 | 503 |
| 17 | Bulldog | 0.1313 | 646 | 4919 |
| 18 | Weimaraner | 0.1277 | 24 | 188 |
| 19 | Wheaton Terrier | 0.1225 | 43 | 351 |
| 20 | Newfoundland | 0.1200 | 12 | 100 |

## Top 20 Biting Breeds (Frequency)
| Rank | Breed | Bites | % of Total Known |
|---|---|---|---|
| 1 | Pit Bull | 6329 | 34.0% |
| 2 | German Shepherd | 1149 | 6.2% |
| 3 | Shih Tzu | 1017 | 5.5% |
| 4 | Chihuahua | 963 | 5.2% |
| 5 | Labrador Retriever | 678 | 3.6% |
| 6 | Yorkshire Terrier | 662 | 3.6% |
| 7 | Bulldog | 646 | 3.5% |
| 8 | Poodle | 593 | 3.2% |
| 9 | Maltese | 514 | 2.8% |
| 10 | Siberian Husky | 500 | 2.7% |
| 11 | Rottweiler | 406 | 2.2% |
| 12 | Terrier | 306 | 1.6% |
| 13 | Jack Russell Terrier | 280 | 1.5% |
| 14 | Beagle | 273 | 1.5% |
| 15 | Cocker Spaniel | 198 | 1.1% |
| 16 | Boxer | 174 | 0.9% |
| 17 | Golden Retriever | 170 | 0.9% |
| 18 | Shiba Inu | 146 | 0.8% |
| 19 | Pomeranian | 143 | 0.8% |
| 20 | Mastiff | 140 | 0.8% |

## Visualizations
### Bite Risk (Bites per 1,000 Licenses)
![Bite Risk Plot](bite_risk_plot.svg)

### Bite Frequency (Absolute)
### Rank-Frequency Distribution
![Rank Frequency Plot](rank_frequency_plot.svg)
