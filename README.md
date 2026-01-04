# Pit Bull Data Analysis

This repository contains data analysis scripts and reports investigating dog bite statistics in New York City, specifically addressing the claims made in "The Dogs of New York".

## Contents

### 1. Risk Analysis Replication (`/`)
Recreation of the original analysis using NYC DOHMH data.
- **Script**: `analyze_dog_bites.py` - Parses bite and licensing data to calculate breed-specific risk.
- **Report**: `analysis_report.md` - Findings from the replication, including the relative risk calculation.
- **Visualizations**: Generated SVG plots for bite frequency and risk distributions.

### 2. Rebuttal Validation (`/rebuttal_reproduction/`)
A focused analysis validation of the rebuttal to the "12.6x risk" claim.
- **Analysis**: `ANALYSIS.md` - Detailed validation of the statistical corrections for over-identification and under-registration.
- **Reproduction**: `repro_calculations.py` - Script to programmatically verify the corrected risk factors.
- **Context**: `README.md` - Overview of the rebuttal methodology.

## Getting Started

### Prerequisites
- Python 3.x

### Running the Analysis
To run the main risk analysis:
```bash
python3 analyze_dog_bites.py
```

To run the rebuttal reproduction:
```bash
cd rebuttal_reproduction
python3 repro_calculations.py
```

## Data Sources
- **Bites**: `DOHMH_Dog_Bite_Data_20260103.csv`
- **Licensing**: `NYC_Dog_Licensing_Dataset_20260103.csv`
*(Note: Large data files may not be included in the repo if they exceed size limits)*
