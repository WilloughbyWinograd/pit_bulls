#!/usr/bin/env python3
"""
Cremieux Analysis Reproduction

This script reproduces the dog bite relative risk analysis from 
"The Dogs of New York" by Cremieux.

Methodology (from the PDF):
- Risk = Number of Bites / Number of Dogs (Population)
- Relative Risk = Risk(Breed X) / Risk(Maltese)
- Population is assumed constant throughout the bite monitoring period.
- Excludes "Unknown", "Mixed", and breeds with <10 bites ("Other").
"""

import csv
from collections import Counter

# --- Configuration ---
BITE_CSV = "DOHMH_Dog_Bite_Data_20260103.csv"
LICENSE_CSV = "NYC_Dog_Licensing_Dataset_20260103.csv"
MIN_BITES_THRESHOLD = 10  # Breeds with fewer bites are grouped as "Other"


def clean_breed(breed: str) -> str:
    """
    Apply Cremieux's "Luxury Classification" rules.
    
    From the PDF:
    - Pit Bull Type: "Pit Bull", "Pit Bull Mix", "American Pit Bull Terrier",
      "Staffordshire Terrier", "American Staffordshire Terrier", etc.
    - Schnauzers: All Schnauzer variants grouped.
    - Mastiffs: All Mastiff variants grouped.
    - Maltipoos: Malti-Poo, Maltipoo variants.
    - Vizslas: Vizsla, Wirehaired Vizsla.
    - Hounds: "Hound Mix", "Hound Crossbreed" -> "Hound".
    - Mixes: "Pit Bull Mix" -> "Pit Bull", "Afghan Hound Crossbreed" -> "Afghan Hound".
    - Misspellings: "Schipperkee" -> "Schipperke", "Pharoh hound" -> "Pharaoh Hound".
    - Generic "Mixed", "Unknown" are excluded.
    """
    if not breed:
        return "Unknown"
    
    b = breed.strip().upper()
    
    # --- Explicit Exclusions ---
    if b in ["UNKNOWN", "UNCERTAIN", "NOT PROVIDED", ""]:
        return "Unknown"
    if b in ["MIXED", "MIXED BREED", "MUTT"]:
        return "Mixed"
    
    # --- Pit Bull Type (Cremieux's explicit definition from footnote) ---
    # From PDF: "American Pit Bull Terrier", "American Pit Bull Mix / Pit Bull Mix",
    # "Staffordshire Bull Terrier" (but this is often separate in data)
    # Test with NARROW definition first (only "PIT BULL" keyword)
    if "PIT BULL" in b or "PITBULL" in b:
        return "Pit Bull"
    
    # Staffordshire Terriers are often considered Pit Bull type
    if "STAFFORDSHIRE" in b:
        return "Pit Bull"
    
    # American Bully is a newer breed, may or may not have been in Cremieux's data
    if "AMERICAN BULLY" in b:
        return "Pit Bull"
    
    # --- Breed Consolidation ---
    if "SCHNAUZER" in b:
        return "Schnauzer"
    if "MALTIPOO" in b or "MALTI-POO" in b or "MALTI POO" in b:
        return "Maltipoo"
    if "MASTIFF" in b or "BULLMASTIFF" in b:
        return "Mastiff"
    if "VIZSLA" in b:
        return "Vizsla"
    
    # --- Hound Consolidation ---
    # "Hound Mix" and "Hound Crossbreed" -> "Hound"
    if b == "HOUND MIX" or b == "HOUND CROSSBREED" or b == "HOUND":
        return "Hound"
    
    # --- Misspelling Corrections ---
    if "SCHIPPERKE" in b or "SCHIPPERKEE" in b:
        return "Schipperke"
    if "PHARAOH" in b or "PHAROH" in b:
        return "Pharaoh Hound"
    
    # --- Mix Handling ---
    # Per Cremieux: "Afghan Hound Crossbreed" -> "Afghan Hound"
    # Strip " Mix", " Crossbreed", " X" and assign to base breed.
    base_breed = b
    for suffix in [" MIX", " CROSSBREED", " X"]:
        if base_breed.endswith(suffix):
            base_breed = base_breed[:-len(suffix)].strip()
            break  # Only strip one suffix
    
    # Handle "Breed / Breed" format (e.g., "American Pit Bull Terrier/Pit Bull")
    if "/" in base_breed:
        parts = base_breed.split("/")
        base_breed = parts[0].strip()  # Take the first part
    
    # --- Common Breed Normalization ---
    if "LABRADOR" in base_breed:
        return "Labrador Retriever"
    if "GERMAN SHEPHERD" in base_breed or "GSD" in base_breed:
        return "German Shepherd"
    if "GOLDEN RETRIEVER" in base_breed:
        return "Golden Retriever"
    if "CHIHUAHUA" in base_breed:
        return "Chihuahua"
    if "SHIH TZU" in base_breed or "SHIHTZU" in base_breed:
        return "Shih Tzu"
    if "YORKSHIRE TERRIER" in base_breed or "YORKIE" in base_breed:
        return "Yorkshire Terrier"
    if "ROTTWEILER" in base_breed:
        return "Rottweiler"
    if "MALTESE" in base_breed:
        return "Maltese"
    if "POODLE" in base_breed:
        return "Poodle"
    if "BEAGLE" in base_breed:
        return "Beagle"
    if "BOXER" in base_breed:
        return "Boxer"
    if "HUSKY" in base_breed:
        return "Siberian Husky"
    if "BULLDOG" in base_breed or "BULL DOG" in base_breed:
        return "Bulldog"
    if "JACK RUSSELL" in base_breed:
        return "Jack Russell Terrier"
    if "COCKER SPANIEL" in base_breed:
        return "Cocker Spaniel"
    if "DACHSHUND" in base_breed:
        return "Dachshund"
    if "DOBERMAN" in base_breed:
        return "Doberman Pinscher"
    if "CHOW" in base_breed:
        return "Chow Chow"
    if "AKITA" in base_breed:
        return "Akita"
    if "GREAT DANE" in base_breed:
        return "Great Dane"
    if "BORDER COLLIE" in base_breed:
        return "Border Collie"
    if "AUSTRALIAN SHEPHERD" in base_breed:
        return "Australian Shepherd"
    if "SHIBA INU" in base_breed or "SHIBA" in base_breed:
        return "Shiba Inu"
    if "POMERANIAN" in base_breed:
        return "Pomeranian"
    if "CANE CORSO" in base_breed:
        return "Cane Corso"
    if "BULL TERRIER" in base_breed and "PIT" not in base_breed:
        return "Bull Terrier"
    
    # Return title-cased base breed
    return base_breed.title()


def main():
    print("=" * 60)
    print("CREMIEUX ANALYSIS REPRODUCTION")
    print("=" * 60)
    
    # --- 1. Load and Count Bites ---
    print(f"\n[1] Loading bite data from: {BITE_CSV}")
    bite_counts = Counter()
    
    with open(BITE_CSV, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_breed = row.get('Breed', '')
            clean = clean_breed(raw_breed)
            bite_counts[clean] += 1
    
    # Remove Unknown and Mixed
    del bite_counts["Unknown"]
    if "Mixed" in bite_counts:
        del bite_counts["Mixed"]
    
    # Apply <10 threshold -> "Other"
    final_bite_counts = Counter()
    for breed, count in bite_counts.items():
        if count >= MIN_BITES_THRESHOLD:
            final_bite_counts[breed] = count
        else:
            final_bite_counts["Other"] += count
    
    # Remove "Other" from final analysis (as per Cremieux)
    if "Other" in final_bite_counts:
        del final_bite_counts["Other"]
    
    total_bites = sum(final_bite_counts.values())
    print(f"    Total bites (after cleaning): {total_bites}")
    print(f"    Unique breeds: {len(final_bite_counts)}")
    
    # --- 2. Load and Count Licenses (ENTIRE dataset, no date filter) ---
    print(f"\n[2] Loading license data from: {LICENSE_CSV}")
    license_counts = Counter()
    
    with open(LICENSE_CSV, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_breed = row.get('BreedName', '')
            clean = clean_breed(raw_breed)
            license_counts[clean] += 1
    
    # Remove Unknown and Mixed
    del license_counts["Unknown"]
    if "Mixed" in license_counts:
        del license_counts["Mixed"]
    
    total_licenses = sum(license_counts.values())
    print(f"    Total licenses (after cleaning): {total_licenses}")
    print(f"    Unique breeds: {len(license_counts)}")
    
    # --- 3. Calculate Risk ---
    print("\n[3] Calculating Risk (Bites / Licenses)...")
    
    # Get Maltese stats for baseline
    maltese_bites = final_bite_counts.get("Maltese", 0)
    maltese_licenses = license_counts.get("Maltese", 0)
    
    if maltese_licenses == 0:
        print("ERROR: No Maltese licenses found. Cannot calculate baseline.")
        return
    
    maltese_risk = maltese_bites / maltese_licenses
    print(f"    Maltese: {maltese_bites} bites / {maltese_licenses} licenses = {maltese_risk:.6f}")
    
    # Get Pit Bull stats
    pitbull_bites = final_bite_counts.get("Pit Bull", 0)
    pitbull_licenses = license_counts.get("Pit Bull", 0)
    
    if pitbull_licenses == 0:
        print("ERROR: No Pit Bull licenses found. Cannot calculate risk.")
        return
    
    pitbull_risk = pitbull_bites / pitbull_licenses
    print(f"    Pit Bull: {pitbull_bites} bites / {pitbull_licenses} licenses = {pitbull_risk:.6f}")
    
    # --- 4. Calculate Relative Risk ---
    relative_risk = pitbull_risk / maltese_risk
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"  Pit Bull Risk:    {pitbull_risk:.6f}")
    print(f"  Maltese Risk:     {maltese_risk:.6f}")
    print(f"  RELATIVE RISK:    {relative_risk:.2f}x")
    print(f"  (Cremieux's claim: 12.59x)")
    print("=" * 60)
    
    # --- 5. Output Top 20 Risk Table ---
    print("\n[4] Top 20 Breeds by Relative Risk:")
    breed_risks = []
    for breed in final_bite_counts:
        bites = final_bite_counts[breed]
        licenses = license_counts.get(breed, 0)
        if licenses > 0:
            risk = bites / licenses
            rr = risk / maltese_risk if maltese_risk > 0 else 0
            breed_risks.append({
                "breed": breed,
                "bites": bites,
                "licenses": licenses,
                "risk": risk,
                "relative_risk": rr
            })
    
    breed_risks.sort(key=lambda x: x["relative_risk"], reverse=True)
    
    print(f"\n{'Rank':<5} {'Breed':<25} {'Bites':<8} {'Licenses':<10} {'Rel. Risk':<10}")
    print("-" * 60)
    for i, item in enumerate(breed_risks[:20], 1):
        print(f"{i:<5} {item['breed']:<25} {item['bites']:<8} {item['licenses']:<10} {item['relative_risk']:.2f}x")


if __name__ == "__main__":
    main()
