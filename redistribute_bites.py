#!/usr/bin/env python3
"""
Redistribute Misattributed Pit Bull Bites

This script:
1. Uses Cremieux's exact values (12.59x baseline)
2. Redistributes misattributed pit bull bites to "big dogs" 
   proportionally based on their % of population
3. Shows rankings before and after correction
"""

import csv
from collections import Counter

# --- Configuration ---
BITE_CSV = "DOHMH_Dog_Bite_Data_20260103.csv"
LICENSE_CSV = "NYC_Dog_Licensing_Dataset_20260103.csv"

# Date filtering (Cremieux's ranges)
MIN_BITE_YEAR = 2015
MAX_BITE_YEAR = 2022
MIN_LICENSE_YEAR = 2014
MAX_LICENSE_YEAR = 2023
MAX_LICENSE_MONTH = 11

# Pit bull over-identification factor (from Olson et al. 2015)
OVERCOUNT_FACTOR = 2.5

# Cremieux's EXACT Pit Bull breed strings (from his footnotes)
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

# Cremieux's Maltese definition (matches his back-classification)
CREMIEUX_MALTESE = {'Maltese', 'Maltese Crossbreed'}

# Big dogs that could be visually confused with pit bulls
BIG_DOG_BREEDS = {
    'Boxer', 'American Bulldog', 'Bulldog', 'Mastiff', 'Bull Terrier',
    'Cane Corso', 'Rottweiler', 'Doberman Pinscher', 'Great Dane',
    'German Shepherd', 'Labrador Retriever', 'American Bully',
    'Rhodesian Ridgeback', 'Weimaraner', 'Vizsla', 'Pointer',
    'Belgian Malinois'
}

def normalize_breed_for_license(breed):
    """Match a license breed to our normalized categories using Cremieux's exact strings."""
    b = breed.strip()
    
    # Cremieux's exact Pit Bull strings
    if b in CREMIEUX_PIT_BULLS:
        return 'Pit Bull'
    
    # Cremieux's exact Maltese strings
    if b in CREMIEUX_MALTESE:
        return 'Maltese'
    
    # Other big dog breeds (normalized)
    b_upper = b.upper()
    if 'LABRADOR' in b_upper:
        return 'Labrador Retriever'
    if 'GERMAN SHEPHERD' in b_upper:
        return 'German Shepherd'
    if 'BOXER' in b_upper:
        return 'Boxer'
    if 'ROTTWEILER' in b_upper:
        return 'Rottweiler'
    if 'BULLDOG' in b_upper and 'FRENCH' not in b_upper:
        return 'Bulldog'
    if 'DOBERMAN' in b_upper:
        return 'Doberman Pinscher'
    if 'GREAT DANE' in b_upper:
        return 'Great Dane'
    if 'MASTIFF' in b_upper:
        return 'Mastiff'
    if 'CANE CORSO' in b_upper:
        return 'Cane Corso'
    if 'BULL TERRIER' in b_upper:
        return 'Bull Terrier'
    if 'BELGIAN MALINOIS' in b_upper:
        return 'Belgian Malinois'
    if 'RHODESIAN' in b_upper:
        return 'Rhodesian Ridgeback'
    if 'WEIMARANER' in b_upper:
        return 'Weimaraner'
    if 'POINTER' in b_upper:
        return 'Pointer'
    if 'AMERICAN BULLY' in b_upper:
        return 'American Bully'
    if 'CHIHUAHUA' in b_upper:
        return 'Chihuahua'
    if 'SIBERIAN HUSKY' in b_upper or 'HUSKY' in b_upper:
        return 'Siberian Husky'
    if 'CHOW' in b_upper:
        return 'Chow Chow'
    if 'AKITA' in b_upper:
        return 'Akita'
    if 'BEAGLE' in b_upper:
        return 'Beagle'
    if 'GOLDEN RETRIEVER' in b_upper:
        return 'Golden Retriever'
    if 'POODLE' in b_upper:
        return 'Poodle'
    if 'YORKSHIRE' in b_upper:
        return 'Yorkshire Terrier'
    if 'SHIH TZU' in b_upper:
        return 'Shih Tzu'
    if 'COCKER SPANIEL' in b_upper:
        return 'Cocker Spaniel'
    if 'DACHSHUND' in b_upper:
        return 'Dachshund'
    
    return None


def normalize_breed_for_bite(breed):
    """Match a bite breed to our normalized categories."""
    b = breed.strip().upper()
    
    if not b or b in ['UNKNOWN', 'MIXED', 'OTHER']:
        return None
    
    # Pit Bull - match keyword pattern (bite data is less granular)
    if 'PIT BULL' in b or 'PITBULL' in b or 'STAFFORDSHIRE' in b:
        return 'Pit Bull'
    if 'AMERICAN BULLY' in b:
        return 'American Bully'
    
    # Match same as license normalization
    if 'MALTESE' in b:
        return 'Maltese'
    if 'LABRADOR' in b:
        return 'Labrador Retriever'
    if 'GERMAN SHEPHERD' in b:
        return 'German Shepherd'
    if 'BOXER' in b:
        return 'Boxer'
    if 'ROTTWEILER' in b:
        return 'Rottweiler'
    if 'BULLDOG' in b and 'FRENCH' not in b:
        return 'Bulldog'
    if 'DOBERMAN' in b:
        return 'Doberman Pinscher'
    if 'GREAT DANE' in b:
        return 'Great Dane'
    if 'MASTIFF' in b:
        return 'Mastiff'
    if 'CANE CORSO' in b:
        return 'Cane Corso'
    if 'BULL TERRIER' in b:
        return 'Bull Terrier'
    if 'BELGIAN MALINOIS' in b:
        return 'Belgian Malinois'
    if 'RHODESIAN' in b:
        return 'Rhodesian Ridgeback'
    if 'WEIMARANER' in b:
        return 'Weimaraner'
    if 'POINTER' in b:
        return 'Pointer'
    if 'CHIHUAHUA' in b:
        return 'Chihuahua'
    if 'HUSKY' in b:
        return 'Siberian Husky'
    if 'CHOW' in b:
        return 'Chow Chow'
    if 'AKITA' in b:
        return 'Akita'
    if 'BEAGLE' in b:
        return 'Beagle'
    if 'GOLDEN RETRIEVER' in b:
        return 'Golden Retriever'
    if 'POODLE' in b:
        return 'Poodle'
    if 'YORKSHIRE' in b or 'YORKIE' in b:
        return 'Yorkshire Terrier'
    if 'SHIH TZU' in b:
        return 'Shih Tzu'
    if 'COCKER SPANIEL' in b:
        return 'Cocker Spaniel'
    if 'DACHSHUND' in b:
        return 'Dachshund'
    
    return None


def main():
    print("=" * 70)
    print("REDISTRIBUTING MISATTRIBUTED PIT BULL BITES")
    print("=" * 70)
    
    # --- Load Bites ---
    print("\n[1] Loading bite data...")
    bite_counts = Counter()
    
    with open(BITE_CSV, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_str = row.get('DateOfBite', '')
            try:
                if ',' in date_str:
                    year = int(date_str.split(',')[-1].strip())
                    if year < MIN_BITE_YEAR or year > MAX_BITE_YEAR:
                        continue
            except ValueError:
                continue
            
            breed = normalize_breed_for_bite(row.get('Breed', ''))
            if breed:
                bite_counts[breed] += 1
    
    print(f"    Loaded {sum(bite_counts.values())} bites across {len(bite_counts)} breeds")
    
    # --- Load Licenses ---
    print("\n[2] Loading license data...")
    license_counts = Counter()
    
    with open(LICENSE_CSV, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            issued_str = row.get('LicenseIssuedDate', '').strip().strip('"')
            try:
                parts = issued_str.split('/')
                if len(parts) == 3:
                    month = int(parts[0])
                    year = int(parts[2])
                    if year < MIN_LICENSE_YEAR or year > MAX_LICENSE_YEAR:
                        continue
                    if year == MIN_LICENSE_YEAR and month < 9:
                        continue
                    if year == MAX_LICENSE_YEAR and month > MAX_LICENSE_MONTH:
                        continue
            except (ValueError, IndexError):
                continue
            
            breed = normalize_breed_for_license(row.get('BreedName', ''))
            if breed:
                license_counts[breed] += 1
    
    print(f"    Loaded {sum(license_counts.values())} licenses across {len(license_counts)} breeds")
    
    # --- Get Maltese baseline ---
    maltese_bites = bite_counts.get('Maltese', 0)
    maltese_licenses = license_counts.get('Maltese', 0)
    maltese_risk = maltese_bites / maltese_licenses if maltese_licenses > 0 else 0
    
    print(f"\n    Maltese: {maltese_bites} bites / {maltese_licenses} licenses")
    print(f"    Maltese risk: {maltese_risk:.6f}")
    
    # --- Pit Bull original ---
    pb_bites = bite_counts.get('Pit Bull', 0)
    pb_licenses = license_counts.get('Pit Bull', 0)
    pb_risk = pb_bites / pb_licenses if pb_licenses > 0 else 0
    pb_rr = pb_risk / maltese_risk if maltese_risk > 0 else 0
    
    print(f"\n    Pit Bull: {pb_bites} bites / {pb_licenses} licenses")
    print(f"    Pit Bull risk: {pb_risk:.6f}")
    print(f"    Pit Bull relative risk: {pb_rr:.2f}x (Cremieux: 12.59x)")
    
    # --- Calculate ORIGINAL relative risk for all breeds ---
    print("\n[3] Calculating ORIGINAL relative risk for all breeds...")
    original_risks = {}
    for breed in set(bite_counts.keys()) | set(license_counts.keys()):
        if breed in license_counts and license_counts[breed] >= 100:
            bites = bite_counts.get(breed, 0)
            licenses = license_counts[breed]
            risk = bites / licenses
            rr = risk / maltese_risk if maltese_risk > 0 else 0
            original_risks[breed] = {
                'bites': bites,
                'licenses': licenses,
                'risk': risk,
                'rr': rr
            }
    
    # --- Calculate misattributed bites ---
    pb_true_bites = pb_bites / OVERCOUNT_FACTOR
    misattributed_bites = pb_bites - pb_true_bites
    
    print(f"\n[4] Bite correction (Olson et al. over-identification factor: {OVERCOUNT_FACTOR}x)")
    print(f"    Reported Pit Bull bites: {pb_bites}")
    print(f"    True Pit Bull bites: {pb_true_bites:.0f}")
    print(f"    Misattributed bites: {misattributed_bites:.0f}")
    
    # --- Calculate redistribution pool (big dogs + Unknown) based on BITES ---
    # We need to track Unknown bites separately
    unknown_bites = 0
    with open(BITE_CSV, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_str = row.get('DateOfBite', '')
            try:
                if ',' in date_str:
                    year = int(date_str.split(',')[-1].strip())
                    if year < MIN_BITE_YEAR or year > MAX_BITE_YEAR:
                        continue
            except ValueError:
                continue
            breed = row.get('Breed', '').strip().upper()
            if not breed or 'UNKNOWN' in breed or breed == 'MIXED':
                unknown_bites += 1
    
    # Calculate big dog bites total (from bite_counts, excluding pit bull)
    big_dog_bites = sum(bite_counts.get(b, 0) for b in BIG_DOG_BREEDS)
    
    # Total redistribution pool = big dogs + unknown
    redistribution_pool_bites = big_dog_bites + unknown_bites
    
    print(f"\n[5] Redistributing to big dogs + Unknown (proportional to BITES)")
    print(f"    Big dog bites: {big_dog_bites}")
    print(f"    Unknown bites: {unknown_bites}")
    print(f"    Total redistribution pool: {redistribution_pool_bites}")
    
    # --- Redistribute misattributed bites proportional to original bites ---
    corrected_bites = dict(bite_counts)
    corrected_bites['Pit Bull'] = pb_true_bites
    corrected_bites['Unknown'] = unknown_bites  # Add Unknown to our tracking
    
    print("\n    Redistribution by bite proportion:")
    for breed in sorted(BIG_DOG_BREEDS):
        if breed in bite_counts and bite_counts[breed] > 0:
            proportion = bite_counts[breed] / redistribution_pool_bites
            additional_bites = misattributed_bites * proportion
            corrected_bites[breed] = corrected_bites.get(breed, 0) + additional_bites
            print(f"      {breed}: {bite_counts[breed]} bites ({proportion*100:.1f}%) → +{additional_bites:.0f}")
    
    # Unknown gets its share too
    unknown_proportion = unknown_bites / redistribution_pool_bites
    unknown_additional = misattributed_bites * unknown_proportion
    corrected_bites['Unknown'] = unknown_bites + unknown_additional
    print(f"      Unknown: {unknown_bites} bites ({unknown_proportion*100:.1f}%) → +{unknown_additional:.0f}")
    
    # --- Calculate CORRECTED relative risk ---
    print("\n[6] Calculating CORRECTED relative risk...")
    corrected_risks = {}
    for breed in set(corrected_bites.keys()) | set(license_counts.keys()):
        if breed in license_counts and license_counts[breed] >= 100:
            bites = corrected_bites.get(breed, 0)
            licenses = license_counts[breed]
            risk = bites / licenses
            rr = risk / maltese_risk if maltese_risk > 0 else 0
            corrected_risks[breed] = {
                'bites': bites,
                'licenses': licenses,
                'risk': risk,
                'rr': rr
            }
    
    # --- Print comparison ---
    print("\n" + "=" * 70)
    print("RESULTS: TOP 20 BREEDS BY RELATIVE RISK (vs Maltese)")
    print("=" * 70)
    
    sorted_original = sorted(original_risks.items(), key=lambda x: x[1]['rr'], reverse=True)
    sorted_corrected = sorted(corrected_risks.items(), key=lambda x: x[1]['rr'], reverse=True)
    
    print("\n--- ORIGINAL ---")
    print(f"{'Rank':<5} {'Breed':<25} {'Bites':<8} {'Pop':<10} {'RR':<10}")
    print("-" * 65)
    for i, (breed, data) in enumerate(sorted_original[:20], 1):
        print(f"{i:<5} {breed:<25} {data['bites']:<8} {data['licenses']:<10} {data['rr']:.2f}x")
    
    print("\n--- CORRECTED (bite misattribution redistributed to big dogs) ---")
    print(f"{'Rank':<5} {'Breed':<25} {'Bites':<8} {'Pop':<10} {'RR':<10}")
    print("-" * 65)
    for i, (breed, data) in enumerate(sorted_corrected[:20], 1):
        bites_disp = f"{data['bites']:.0f}" if isinstance(data['bites'], float) else str(data['bites'])
        print(f"{i:<5} {breed:<25} {bites_disp:<8} {data['licenses']:<10} {data['rr']:.2f}x")
    
    # --- Summary ---
    print("\n" + "=" * 70)
    print("PIT BULL SUMMARY")
    print("=" * 70)
    orig_rank = [b for b, _ in sorted_original].index('Pit Bull') + 1 if 'Pit Bull' in original_risks else 'N/A'
    corr_rank = [b for b, _ in sorted_corrected].index('Pit Bull') + 1 if 'Pit Bull' in corrected_risks else 'N/A'
    print(f"Original:  Rank #{orig_rank}, RR = {original_risks.get('Pit Bull', {}).get('rr', 0):.2f}x")
    print(f"After bite correction: Rank #{corr_rank}, RR = {corrected_risks.get('Pit Bull', {}).get('rr', 0):.2f}x")
    
    # --- ALSO apply population under-count correction ---
    print("\n" + "=" * 70)
    print("FULL CORRECTION: Bite Misattribution + Population Under-Count")
    print("=" * 70)
    
    pb_corrected_rr = corrected_risks.get('Pit Bull', {}).get('rr', 0)
    
    print("\nPit Bull population is under-counted in licensing data due to:")
    print("  - Only ~20% of NYC dogs are licensed overall")
    print("  - Pit bull owners face unique disincentives (housing bans, BSL, insurance)")
    print("  - Pit bulls are <5% of licenses but 10-20% of national dog population")
    
    print("\n--- SCENARIO: 2x Population Under-Count (Conservative) ---")
    # If pit bull population is 2x what licenses show, divide RR by 2
    rr_2x = pb_corrected_rr / 2
    print(f"  True Pit Bull Pop = {pb_licenses} × 2 = {pb_licenses * 2}")
    print(f"  Corrected RR = {pb_corrected_rr:.2f}x / 2 = {rr_2x:.2f}x")
    
    print("\n--- SCENARIO: 4x Population Under-Count (Evidence-Based) ---")
    rr_4x = pb_corrected_rr / 4
    print(f"  True Pit Bull Pop = {pb_licenses} × 4 = {pb_licenses * 4}")
    print(f"  Corrected RR = {pb_corrected_rr:.2f}x / 4 = {rr_4x:.2f}x")
    
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    orig_rr = original_risks.get('Pit Bull', {}).get('rr', 0)
    print(f"{'Scenario':<45} {'Pit Bull RR':<15}")
    print("-" * 60)
    print(f"{'Cremieux Original':<45} {orig_rr:.2f}x")
    print(f"{'+ Bite Misattribution Correction (2.5x)':<45} {pb_corrected_rr:.2f}x")
    print(f"{'+ Pop Under-Count 2x (Conservative)':<45} {rr_2x:.2f}x")
    print(f"{'+ Pop Under-Count 4x (Evidence-Based)':<45} {rr_4x:.2f}x")


if __name__ == "__main__":
    main()
