
import csv
import io
import math
from collections import Counter, defaultdict

INPUT_CSV = "DOHMH_Dog_Bite_Data_20260103.csv"
OUTPUT_REPORT = "analysis_report.md"

def clean_breed(breed):
    if not breed:
        return "Unknown"
    
    b = breed.strip().upper()
    
    # Handle explicit "Unknown" / "Uncertain"
    if b in ["UNKNOWN", "UNCERTAIN", "NO DOG", ""]:
        return "Unknown"

    # Fix spellings
    if "SCHIPPERKE" in b: # Covers SCHIPPERKE and SCHIPPERKEE
        return "Schipperke"
    if "PHAR" in b and "HOUND" in b: # Covers PHARAOH HOUND variants
        return "Pharaoh Hound"
    
    # Grouping Logic from PDF
    # "Pit Bull Mix", "American Pit Bull Terrier/Pit Bull" etc -> Pit Bull
    if "PIT BULL" in b or "PITBULL" in b or "STAFFORDSHIRE TERRIER" in b or "AM STAFF" in b or "AMERICAN BULLY" in b:
        # The PDF says "Pit Bull Mix" were classed with Pit Bulls.
        # It implies a broad aggregation for "Pit Bull Type".
        # "American Staffordshire Terrier" is often grouped with Pit Bulls in these contexts.
        return "Pit Bull"

    # Schnauzers
    if "SCHNAUZER" in b:
        return "Schnauzer"
    
    # Maltipoos
    if "MALTIPOO" in b or ("MALTI" in b and "POO" in b):
        return "Maltipoo"
        
    # Mastiffs
    if "MASTIFF" in b or "BULLMASTIFF" in b:
        return "Mastiff"
        
    # Vizslas
    if "VIZSLA" in b:
        return "Vizsla"
    
    # Mixed/Crossbreed handling
    # If it says "Mix" or "X" or "Crossbreed" but hasn't been caught by specific rules above (like Pit Bull Mix)
    # The PDF says: "the remaining 'Mixed' category was just for nonspecific mixes."
    # So "Labrador Mix" -> "Labrador Retriever" ?? Or "Mixed"? 
    # The PDF says: "Those classified as 'Pit Bull Mix', 'Afghan Hound Crossbreed', etc., were classed with Pit Bulls, Afghan Hounds, etc."
    # So we should strip "Mix", "Crossbreed", "X" and classify as the base breed.
    
    # specific mixed types that denote Mixed/Other
    if b in ["MIXED", "MIXED BREED", "LARGE MIXED BREED", "MEDIUM MIXED BREED", "SMALL MIXED BREED", "MUTT", "MONGREL", "MIXED/OTHER", "MIXED OTHER"]:
        return "Mixed/Other"

    # Jack Russell
    if "JACK RUSS" in b:
        return "Jack Russell Terrier"
    
    # Mixed/Crossbreed handling
    base_breed = b
    is_mix = False
    
    # Clean up "Mix" indicators 
    # Be careful not to break "MIXED BREED" if we haven't caught it yet, but we tried above.
    # Also handle " / " or "/"
    
    for indicator in [" MIX", " CROSSBREED", " X"]:
        if indicator in base_breed:
            is_mix = True
            base_breed = base_breed.replace(indicator, "")
            
    # Handle "/" separately to avoid "Mixed/Other" becoming "MixedOther" if it wasn't caught
    if "/" in base_breed:
        # If it's like "Labrador/Poodle", pick the first? Or generic Mix?
        # PDF says "Pit Bull Mix" -> Pit Bull.
        # "American Pit Bull Terrier/Pit Bull" -> Pit Bull (handled by top rule)
        # "Shepherd/Pointer X" -> Shepherd?
        # Let's take the first part as primary if we must, or just Leave it?
        # If I split by space and take first?
        # simple cleaning: replace / with space
        base_breed = base_breed.replace("/", " ")

    base_breed = base_breed.strip()
    
    # Re-check generic names after stripping (e.g. "TERRIER MIX" -> "TERRIER")
    # But "LARGE MIXED BREED" -> "LARGEED BREED" issue:
    # "MIXED" contains "MIX". "LARGE MIXED BREED".replace(" MIX", "") -> "LARGEED BREED".
    # We should have caught "LARGE MIXED BREED" at the top.
    # But if input is "LARGE MIXED BREED " (trailing space)? .strip() was done at start.
    
    # Let's add more catch-alls for "ED BREED" if it happens
    if "ED BREED" in base_breed:
        return "Mixed/Other" # Likely a cleaning artifact of "MIXED BREED"

    # If the base breed is generic like "Large Mixed Breed", "Mixed", "Small Mixed Breed"
    if base_breed in ["MIXED", "MIXED BREED", "LARGE MIXED BREED", "MEDIUM MIXED BREED", "SMALL MIXED BREED", "MUTT", "MONGREL", "MIXED OTHER"]:
        return "Mixed/Other"
        
    # If we reduced it to a known breed, return that formatted nicely (Title Case)
    # But we need to handle cases like "Labrador Retriever" which might be "Labrador"
    if "LABRADOR" in base_breed or "LAB " in base_breed:
        return "Labrador Retriever"
    if "GERMAN SHEPHERD" in base_breed or "SHEPERD" in base_breed or "SHEPHERD" in base_breed:
         return "German Shepherd"
    if "ROTTWEILER" in base_breed:
        return "Rottweiler"
    if "CHIHUAHUA" in base_breed:
        return "Chihuahua"
    if "SHIH TZU" in base_breed:
        return "Shih Tzu"
    if "YORKSHIRE TERRIER" in base_breed or "YORKIE" in base_breed:
        return "Yorkshire Terrier"
    if "HUSKY" in base_breed:
        return "Siberian Husky"
    if "MALTESE" in base_breed:
        return "Maltese"
    if "BEAGLE" in base_breed:
        return "Beagle"
    if "BOXER" in base_breed:
        return "Boxer"
    if "GOLDEN RETRIEVER" in base_breed:
        return "Golden Retriever"
    if "POODLE" in base_breed:
        return "Poodle"
    if "CANE CORSO" in base_breed:
        return "Cane Corso"
    if "BULL DOG" in base_breed or "BULLDOG" in base_breed:
        return "Bulldog"
        
    # Return Title Case for others
    return base_breed.title()

def create_bar_chart_svg(data, filename, title):
    # data is list of (label, value)
    if not data:
        return
    
    width = 800
    height = 500
    margin_left = 150
    margin_bottom = 50
    margin_top = 50
    margin_right = 20
    
    chart_width = width - margin_left - margin_right
    chart_height = height - margin_top - margin_bottom
    
    max_val = data[0][1]
    bar_height = chart_height / len(data) * 0.8
    gap = chart_height / len(data) * 0.2
    
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
    svg += f'<rect width="100%" height="100%" fill="white"/>'
    svg += f'<text x="{width/2}" y="{margin_top/2}" text-anchor="middle" font-family="Arial" font-size="20" font-weight="bold">{title}</text>'
    
    # Bars
    for i, (label, value) in enumerate(data):
        y = margin_top + i * (bar_height + gap)
        bar_w = (value / max_val) * chart_width
        
        # Bar
        svg += f'<rect x="{margin_left}" y="{y}" width="{bar_w}" height="{bar_height}" fill="#4285F4"/>'
        
        # Label
        svg += f'<text x="{margin_left - 10}" y="{y + bar_height/2 + 5}" text-anchor="end" font-family="Arial" font-size="12">{label}</text>'
        
        # Value
        svg += f'<text x="{margin_left + bar_w + 5}" y="{y + bar_height/2 + 5}" font-family="Arial" font-size="12">{value}</text>'
        
    svg += '</svg>'
    
    with open(filename, 'w') as f:
        f.write(svg)

def create_log_log_svg(data, filename, title):
    # data is list of values (ranks implicit)
    if not data:
        return
        
    width = 600
    height = 600
    margin = 60
    chart_w = width - 2*margin
    chart_h = height - 2*margin
    
    ranks = range(1, len(data) + 1)
    values = data
    
    min_x, max_x = math.log10(1), math.log10(len(data))
    min_y, max_y = math.log10(min(values)), math.log10(max(values))
    
    # Scale helper
    def get_x(log_rank):
        return margin + (log_rank - min_x) / (max_x - min_x) * chart_w if max_x > min_x else margin
    
    def get_y(log_val):
        return height - margin - (log_val - min_y) / (max_y - min_y) * chart_h if max_y > min_y else height - margin

    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
    svg += f'<rect width="100%" height="100%" fill="white"/>'
    svg += f'<text x="{width/2}" y="{margin/2}" text-anchor="middle" font-family="Arial" font-size="20" font-weight="bold">{title}</text>'
    
    # Axes
    svg += f'<line x1="{margin}" y1="{height-margin}" x2="{width-margin}" y2="{height-margin}" stroke="black"/>' # X
    svg += f'<line x1="{margin}" y1="{height-margin}" x2="{margin}" y2="{margin}" stroke="black"/>' # Y
    
    # Plot points
    points = []
    for r, v in zip(ranks, values):
        lx = math.log10(r)
        ly = math.log10(v)
        px = get_x(lx)
        py = get_y(ly)
        points.append((px, py))
        svg += f'<circle cx="{px}" cy="{py}" r="3" fill="#EA4335" opacity="0.6"/>'
        
    svg += '</svg>'
    
    with open(filename, 'w') as f:
        f.write(svg)

def main():
    # --- 1. Process Bite Data ---
    bite_counts = Counter()
    total_bites = 0
    
    # Cremieux likely accepted data through 2022. limiting to match.
    MAX_YEAR = 2022
    
    print(f"Loading bite data from {INPUT_CSV} (Filtering <= {MAX_YEAR})...")
    with open(INPUT_CSV, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_str = row.get('DateOfBite', '')
            try:
                # Format is "January 01, 2018"
                # Simple parsing: split by space, take last part as year
                if ',' in date_str:
                    year = int(date_str.split(',')[-1].strip())
                    if year > MAX_YEAR:
                        continue
            except ValueError:
                pass 
                # If date parse fails, include.
            
            raw_breed = row.get('Breed', '')
            clean = clean_breed(raw_breed)
            
            # Exclude Unknown/Mixed for breed-specific ranking
            if clean not in ["Unknown", "Mixed/Other"]:
                bite_counts[clean] += 1
                total_bites += 1

    # --- 2. Process Licensing Data (Strict 2022 Population) ---
    LICENSE_CSV = "NYC_Dog_Licensing_Dataset_20260103.csv"
    license_counts = Counter()
    total_licenses = 0
    TARGET_POP_YEAR = 2022

    print(f"Loading licensing data from {LICENSE_CSV} (Active in {TARGET_POP_YEAR})...")
    try:
        with open(LICENSE_CSV, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Column check
                if 'LicenseIssuedDate' not in row or 'LicenseExpiredDate' not in row:
                    continue
                    
                issued_str = row['LicenseIssuedDate']
                expired_str = row['LicenseExpiredDate']
                
                try:
                    # Date Format: "09/12/2014" (MM/DD/YYYY)
                    # We only need the year, or convert to comparable dates
                    # Simple check: valid in target year if Issued <= 2022 and Expired >= 2022
                   
                    # Helper to get year
                    def get_year(d_str):
                        return int(d_str.split('/')[-1])
                        
                    issued_year = get_year(issued_str)
                    expired_year = get_year(expired_str)
                    
                    # Logic: Was it active at any point in 2022?
                    # Active if Issued <= 2022 AND Expired >= 2022
                    if issued_year <= TARGET_POP_YEAR and expired_year >= TARGET_POP_YEAR:
                        raw_breed = row.get('BreedName', '')
                        clean = clean_breed(raw_breed)
                        if clean not in ["Unknown", "Mixed/Other"]:
                            license_counts[clean] += 1
                            total_licenses += 1
                            
                except (ValueError, IndexError):
                    continue

    except FileNotFoundError:
        print(f"Error: {LICENSE_CSV} not found. Skipping risk analysis.")
        return

    # --- 3. Calculate Risk ---
    # Risk = Bites / Licenses
    # Filter for breeds with sufficient population to avoid unstable rates (e.g., > 100 licenses)
    breed_stats = []
    MIN_LICENSES = 100
    
    unique_breeds = set(bite_counts.keys()) | set(license_counts.keys())
    
    for breed in unique_breeds:
        bites = bite_counts[breed]
        licenses = license_counts[breed]
        
        if licenses >= MIN_LICENSES:
            risk = bites / licenses
            breed_stats.append({
                "breed": breed,
                "bites": bites,
                "licenses": licenses,
                "risk": risk
            })
            
    # Sort by Risk
    breed_stats.sort(key=lambda x: x['risk'], reverse=True)
    top_20_risk = breed_stats[:20]

    # --- 4. Risk Visualization ---
    # Convert metric to "Bites per 1000 Licenses" for readability in chart
    chart_data = [(item['breed'], item['risk'] * 1000) for item in top_20_risk]
    create_bar_chart_svg(chart_data, "bite_risk_plot.svg", "Top 20 Breeds by Bite Risk (Bites per 1,000 Licenses)")


    # --- 5. Generate Report ---
    top_20_bites = bite_counts.most_common(20)
    create_bar_chart_svg(top_20_bites, "bite_frequency_plot.svg", "Top 20 Biting Breeds (Absolute Counts)")
    
    # Rank-Frequency Plot
    all_bite_counts = sorted(bite_counts.values(), reverse=True)
    filtered_bite_counts = [c for c in all_bite_counts if c >= 5]
    create_log_log_svg(filtered_bite_counts, "rank_frequency_plot.svg", "Rank-Frequency Distribution (Log-Log)")

    with open(OUTPUT_REPORT, 'w') as f:
        f.write("# Dog Bite Analysis Report\n\n")
        f.write("Analysis recreating findings from 'The Dogs of New York' using both Bite and Licensing data.\n\n")
        
        # --- Relative Risk Calculation (Pit Bull vs Maltese) ---
        pit_stats = next((item for item in breed_stats if item['breed'] == "Pit Bull"), None)
        maltese_stats = next((item for item in breed_stats if item['breed'] == "Maltese"), None)
        
        f.write("## Risk Analysis Findings\n")
        if pit_stats and maltese_stats:
            pit_risk = pit_stats['risk']
            maltese_risk = maltese_stats['risk']
            relative_risk = pit_risk / maltese_risk
            
            f.write(f"### Pit Bull vs. Maltese Relative Risk\n")
            f.write(f"- **Pit Bull Risk**: {pit_risk:.4f} bites per license\n")
            f.write(f"- **Maltese Risk**: {maltese_risk:.4f} bites per license\n")
            f.write(f"- **Relative Risk**: **{relative_risk:.2f}x**\n\n")
            f.write(f"> This calculates how much more likely a Pit Bull is to bite compared to a Maltese, given their registered populations.\n")
            f.write(f"> **Verification**: The original article claims ~12.59x. Our calculated value is {relative_risk:.2f}x.\n\n")
        
        f.write("## Top 20 High-Risk Breeds\n")
        f.write("| Rank | Breed | Risk (Bites/License) | Bites | Licenses |\n")
        f.write("|---|---|---|---|---|\n")
        for i, item in enumerate(top_20_risk, 1):
            f.write(f"| {i} | {item['breed']} | {item['risk']:.4f} | {item['bites']} | {item['licenses']} |\n")
            
        f.write("\n## Top 20 Biting Breeds (Frequency)\n")
        f.write("| Rank | Breed | Bites | % of Total Known |\n")
        f.write("|---|---|---|---|\n")
        for i, (breed, count) in enumerate(top_20_bites, 1):
            pct = count / total_bites * 100
            f.write(f"| {i} | {breed} | {count} | {pct:.1f}% |\n")
        
        f.write("\n## Visualizations\n")
        f.write("### Bite Risk (Bites per 1,000 Licenses)\n")
        f.write("![Bite Risk Plot](bite_risk_plot.svg)\n\n")
        
        f.write("### Bite Frequency (Absolute)\n")
        f.write("### Rank-Frequency Distribution\n")
        f.write("![Rank Frequency Plot](rank_frequency_plot.svg)\n")

if __name__ == "__main__":
    main()
