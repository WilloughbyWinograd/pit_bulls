#!/usr/bin/env python3
"""
Reproduction script for "Cremieux Is Wrong About Pit Bulls" rebuttal calculations.

This script demonstrates how correcting for systematic biases in:
1. Bite Identification (Over-identification of Pit Bulls)
2. Population Registration (Under-registration of Pit Bulls)
Reduces the reported Relative Risk (RR) from ~12.6x to ~1.3x - 2.5x.
"""

def calculate_adjusted_risk(reported_rr, over_id_factor, under_reg_factor):
    """
    Calculates the adjusted relative risk.
    
    Formula:
        Adjusted RR = Reported RR / (Over_ID_Factor * Under_Reg_Factor)
        
    Args:
        reported_rr (float): The relative risk reported in the original analysis (12.59)
        over_id_factor (float): Factor by which Pit Bulls are over-identified (2.5)
        under_reg_factor (float): Factor by which Pit Bulls are under-registered (2.0 - 4.0)
        
    Returns:
        float: The corrected relative risk.
    """
    return reported_rr / (over_id_factor * under_reg_factor)

def main():
    # --- Input Parameters ---
    
    # 1. Reported Relative Risk
    # Source: Cremieux Analysis of NYC Data
    REPORTED_RR = 12.59
    
    # 2. Over-Identification Factor
    # Source: Olson KR, et al. (2015). "Inconsistent identification of pit bull-type dogs by shelter staff."
    # Finding: 52% visual ID vs 21% DNA confirmed.
    # Calculation: 52 / 21 = 2.476 -> ~2.5x
    OVER_ID_FACTOR = 2.5
    
    # 3. Under-Registration Factor
    # Source: NYC DOHMH Data (~5% reported) vs National Estimates (~10-20% actual)
    # Conservative Estimate (10% actual / 5% reported) = 2x
    # Moderate Estimate (20% actual / 5% reported) = 4x
    UNDER_REG_FACTORS = {
        "Conservative (2x)": 2.0,
        "Moderate (4x)": 4.0
    }
    
    # --- Reproduction Output ---
    
    print(f"{'-'*40}")
    print(f"Rebuttal Calculation Reproduction")
    print(f"{'-'*40}")
    print(f"Reported Relative Risk (RR): {REPORTED_RR}x\n")
    
    print(f"Correction Factors:")
    print(f"  - Over-Identification Bias: {OVER_ID_FACTOR}x (Source: Olson et al., 2015)")
    print(f"  - Under-Registration Bias:  2.0x - 4.0x (Source: NYC vs National Data)\n")
    
    print(f"{'-'*40}")
    print(f"Results:")
    print(f"{'-'*40}")
    
    for label, factor in UNDER_REG_FACTORS.items():
        adjusted_rr = calculate_adjusted_risk(REPORTED_RR, OVER_ID_FACTOR, factor)
        print(f"Scenario: {label} Under-Registration")
        print(f"  Calculation: {REPORTED_RR} / ({OVER_ID_FACTOR} * {factor})")
        print(f"  Adjusted Risk: {adjusted_rr:.2f}x")
        print("")

if __name__ == "__main__":
    main()
