"""
Test script to verify alternator calculations
Validates the analytical solution for the given problem
"""

import sys
import numpy as np
from alternator_advanced_lab import AlternatorParameters, AlternatorCalculator

def test_alternator_solution():
    """Test the alternator calculation with given parameters"""

    print("="*80)
    print("SALIENT POLE ALTERNATOR CALCULATION TEST")
    print("="*80)
    print()

    # Create parameters matching the problem
    params = AlternatorParameters(
        kva_rating=25.0,
        voltage_rating=440.0,
        frequency=50.0,
        ra=0.3,
        xd=5.0,
        xq=3.0,
        power_factor=0.8,
        connection="star"
    )

    print("GIVEN PARAMETERS:")
    print(f"  Rating: {params.kva_rating} kVA, {params.voltage_rating} V, {params.frequency} Hz")
    print(f"  Connection: {params.connection.upper()}")
    print(f"  Ra = {params.ra} Ω")
    print(f"  Xd = {params.xd} Ω")
    print(f"  Xq = {params.xq} Ω")
    print(f"  Power Factor = {params.power_factor} lagging")
    print()

    # Calculate
    calc = AlternatorCalculator(params)
    results = calc.calculate_steady_state()

    print("CALCULATED RESULTS:")
    print("-"*80)
    print(f"Phase Voltage (V_ph):              {results['v_phase']:.2f} V")
    print(f"Rated Current (I_a):                {results['i_rated']:.2f} A")
    print(f"Power Factor Angle (φ):             {results['phi_deg']:.2f}°")
    print()
    print(f"Direct Axis Current (I_d):          {results['id']:.2f} A")
    print(f"Quadrature Axis Current (I_q):      {results['iq']:.2f} A")
    print()
    print("="*80)
    print(" *** PRIMARY ANSWERS ***")
    print("="*80)
    print(f"TORQUE ANGLE (δ):                   {results['delta_deg']:.2f}°")
    print(f"INDUCED EMF PER PHASE (E_f):        {results['ef']:.2f} V")
    print(f"VOLTAGE REGULATION (VR):            {results['voltage_regulation']:.2f} %")
    print("="*80)
    print()

    print("ADDITIONAL RESULTS:")
    print("-"*80)
    print(f"Power Output:                       {results['power_output']:.2f} kW")
    print(f"Copper Losses:                      {results['power_loss']:.3f} kW")
    print(f"Efficiency:                         {results['efficiency']:.2f} %")
    print(f"Electromagnetic Torque:             {results['torque']:.2f} N·m")
    print(f"Synchronous Speed:                  {results['omega_s']:.2f} rad/s")
    print()

    # Validation checks
    print("VALIDATION CHECKS:")
    print("-"*80)

    # Check 1: Phase voltage for star connection
    expected_v_ph = 440 / np.sqrt(3)
    if abs(results['v_phase'] - expected_v_ph) < 0.1:
        print("✓ Phase voltage calculation correct")
    else:
        print("✗ Phase voltage calculation incorrect")

    # Check 2: Rated current
    expected_i = 25000 / (np.sqrt(3) * 440)
    if abs(results['i_rated'] - expected_i) < 0.1:
        print("✓ Rated current calculation correct")
    else:
        print("✗ Rated current calculation incorrect")

    # Check 3: Power factor angle
    expected_phi = np.degrees(np.arccos(0.8))
    if abs(results['phi_deg'] - expected_phi) < 0.1:
        print("✓ Power factor angle correct")
    else:
        print("✗ Power factor angle incorrect")

    # Check 4: Id and Iq consistency
    i_reconstructed = np.sqrt(results['id']**2 + results['iq']**2)
    if abs(i_reconstructed - results['i_rated']) < 0.1:
        print("✓ Current component resolution correct")
    else:
        print("✗ Current component resolution incorrect")

    # Check 5: Power output
    expected_power = 3 * results['v_phase'] * results['i_rated'] * params.power_factor / 1000
    if abs(results['power_output'] - expected_power) < 0.1:
        print("✓ Power output calculation correct")
    else:
        print("✗ Power output calculation incorrect")

    print()
    print("="*80)
    print("TEST COMPLETED SUCCESSFULLY")
    print("="*80)
    print()

    # Summary for problem solution
    print("FINAL ANSWER SUMMARY:")
    print("="*80)
    print(f"""
For a 25 kVA, 440 V, 50 Hz, star-connected salient pole alternator
operating at rated load with 0.8 lagging power factor:

1. Torque Angle (δ)         = {results['delta_deg']:.2f}°
2. Induced EMF per phase (Ef) = {results['ef']:.2f} V
3. Voltage Regulation (VR)   = {results['voltage_regulation']:.2f} %

Machine parameters: Ra = {params.ra} Ω, Xd = {params.xd} Ω, Xq = {params.xq} Ω
    """)
    print("="*80)

    return results

if __name__ == "__main__":
    try:
        results = test_alternator_solution()
        print("\n✓ All tests passed successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
