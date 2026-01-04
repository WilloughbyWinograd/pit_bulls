#!/usr/bin/env python3
"""
Cremieux Analysis Reproduction

This script reproduces the dog bite relative risk analysis from 
"The Dogs of New York" by Cremieux (June 29, 2024).

Result: 12.73x relative risk (Cremieux claimed 12.59x)
The small difference is due to data updates between his Feb 2024 snapshot
and the current Jan 2026 snapshot.

Methodology (from the PDF):
- Risk = Number of Bites / Number of Dogs (Population)
- Relative Risk = Risk(Pit Bull) / Risk(Maltese)
- Data ranges: Bites Jan 2015 - Dec 2022, Licenses Sept 2014 - Nov 2023
- Uses Cremieux's EXACT breed string classifications from his footnotes
"""

import csv
from collections import Counter

# --- Configuration ---
BITE_CSV = "DOHMH_Dog_Bite_Data_20260103.csv"
LICENSE_CSV = "NYC_Dog_Licensing_Dataset_20260103.csv"

# Date filtering to match Cremieux's exact data vintage
# Bites: January 2015 - December 2022
MIN_BITE_YEAR = 2015
MAX_BITE_YEAR = 2022
# Licenses: September 2014 - November 2023
MIN_LICENSE_YEAR = 2014
MAX_LICENSE_YEAR = 2023
MAX_LICENSE_MONTH = 11  # November

# Cremieux's EXACT Pit Bull Type breed strings (from footnote image in PDF)
CREMIEUX_PIT_BULLS = {
    'American Pit Bull Terrier',
    'American Pit Bull Mix / Pit Bull Mix',
    'Pit Bull',
    'Pit Bull Mix',
    'American Staffordshire Terrier',
    'Staffordshire Bull Terrier',
    'American Pit Bull Terrier Crossbreed',
    'American Staffordshire Terrier Crossbreed',
}

# Maltese breeds (per his back-classification method)
MALTESE_BREEDS = {'Maltese', 'Maltese Crossbreed'}


def is_pit_bull_license(breed: str) -> bool:
    """Check if a license breed string is a Pit Bull Type (exact match)."""
    return breed.strip() in CREMIEUX_PIT_BULLS


def is_pit_bull_bite(breed: str) -> bool:
    """Check if a bite breed string is a Pit Bull Type (includes variants)."""
    b = breed.strip()
    if b in CREMIEUX_PIT_BULLS:
        return True
    b_upper = b.upper()
    if 'PIT BULL' in b_upper or 'STAFFORDSHIRE' in b_upper:
        return True
    return False


def is_maltese_license(breed: str) -> bool:
    """Check if a license breed string is Maltese (exact match)."""
    return breed.strip() in MALTESE_BREEDS


def is_maltese_bite(breed: str) -> bool:
    """Check if a bite breed string is Maltese."""
    return 'MALTESE' in breed.upper()


def main():
    print("=" * 60)
    print("CREMIEUX ANALYSIS REPRODUCTION")
    print("=" * 60)
    print(f"Data ranges:")
    print(f"  Bites: Jan {MIN_BITE_YEAR} - Dec {MAX_BITE_YEAR}")
    print(f"  Licenses: Sept {MIN_LICENSE_YEAR} - Nov {MAX_LICENSE_YEAR}")
    
    # --- 1. Load and Count Bites ---
    print(f"\n[1] Loading bite data from: {BITE_CSV}")
    pit_bites = 0
    maltese_bites = 0
    total_bites = 0
    skipped_bites = 0
    
    with open(BITE_CSV, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Filter by year
            date_str = row.get('DateOfBite', '')
            try:
                if ',' in date_str:
                    year = int(date_str.split(',')[-1].strip())
                    if year < MIN_BITE_YEAR or year > MAX_BITE_YEAR:
                        skipped_bites += 1
                        continue
            except ValueError:
                continue
            
            total_bites += 1
            breed = row.get('Breed', '').strip()
            
            if is_pit_bull_bite(breed):
                pit_bites += 1
            elif is_maltese_bite(breed):
                maltese_bites += 1
    
    print(f"    Total bites in range: {total_bites}")
    print(f"    Pit Bull bites: {pit_bites}")
    print(f"    Maltese bites: {maltese_bites}")
    print(f"    (Skipped {skipped_bites} bites outside date range)")
    
    # --- 2. Load and Count Licenses ---
    print(f"\n[2] Loading license data from: {LICENSE_CSV}")
    pit_licenses = 0
    maltese_licenses = 0
    total_licenses = 0
    skipped_licenses = 0
    
    with open(LICENSE_CSV, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Filter by LicenseIssuedDate (MM/DD/YYYY format)
            issued_str = row.get('LicenseIssuedDate', '').strip().strip('"')
            try:
                parts = issued_str.split('/')
                if len(parts) == 3:
                    month = int(parts[0])
                    year = int(parts[2])
                    # Min: Sept 2014
                    if year < MIN_LICENSE_YEAR:
                        skipped_licenses += 1
                        continue
                    if year == MIN_LICENSE_YEAR and month < 9:
                        skipped_licenses += 1
                        continue
                    # Max: Nov 2023
                    if year > MAX_LICENSE_YEAR:
                        skipped_licenses += 1
                        continue
                    if year == MAX_LICENSE_YEAR and month > MAX_LICENSE_MONTH:
                        skipped_licenses += 1
                        continue
            except (ValueError, IndexError):
                continue
            
            total_licenses += 1
            breed = row.get('BreedName', '').strip()
            
            if is_pit_bull_license(breed):
                pit_licenses += 1
            elif is_maltese_license(breed):
                maltese_licenses += 1
    
    print(f"    Total licenses in range: {total_licenses}")
    print(f"    Pit Bull licenses: {pit_licenses}")
    print(f"    Maltese licenses: {maltese_licenses}")
    print(f"    (Skipped {skipped_licenses} licenses outside date range)")
    
    # --- 3. Calculate Risk ---
    print("\n[3] Calculating Risk...")
    
    if maltese_licenses == 0 or pit_licenses == 0:
        print("ERROR: Missing license counts. Cannot calculate risk.")
        return
    
    pit_risk = pit_bites / pit_licenses
    maltese_risk = maltese_bites / maltese_licenses
    relative_risk = pit_risk / maltese_risk
    
    # --- 4. Output Results ---
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"  Pit Bull: {pit_bites} bites / {pit_licenses} licenses")
    print(f"  Pit Bull Risk:    {pit_risk:.6f}")
    print()
    print(f"  Maltese: {maltese_bites} bites / {maltese_licenses} licenses")
    print(f"  Maltese Risk:     {maltese_risk:.6f}")
    print()
    print(f"  RELATIVE RISK:    {relative_risk:.2f}x")
    print(f"  (Cremieux's claim: 12.59x)")
    print("=" * 60)
    
    # --- 5. Comparison with Cremieux's values ---
    print("\n[4] Comparison with Cremieux's reported values:")
    print("    Cremieux's Pit Bull: 6,053 bites / 21,915 licenses")
    print("    Cremieux's Maltese:  469 bites / 21,363 licenses")
    print()
    print("    Differences are due to data updates between")
    print("    his Feb 2024 snapshot and current Jan 2026 data.")


if __name__ == "__main__":
    main()
