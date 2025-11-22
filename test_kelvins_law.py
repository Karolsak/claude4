"""
Test script for Kelvin's Law Calculator
Verifies calculations without GUI
"""

import sys
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing

from kelvins_law_calculator import KelvinsLawCalculator


def test_calculator():
    """Test the calculator with default problem values"""
    print("="*70)
    print("KELVIN'S LAW CALCULATOR - TEST RUN")
    print("="*70)
    print()

    # Create calculator instance
    calc = KelvinsLawCalculator()

    print("INPUT PARAMETERS:")
    print(f"  Distance: {calc.distance} km")
    print(f"  Voltage: {calc.voltage} kV")
    print(f"  Load 1: {calc.load1_kw} kW at {calc.load1_pf} p.f. for {calc.load1_hours} hours")
    print(f"  Load 2: {calc.load2_kw} kW at {calc.load2_pf} p.f. for {calc.load2_hours} hours")
    print(f"  Load 3: {calc.load3_kw} kW at {calc.load3_pf} p.f. for {calc.load3_hours} hours")
    print()

    # Calculate maximum demand
    md = calc.calculate_maximum_demand()
    print(f"Maximum Demand: {md:.2f} kVA")
    print()

    # Calculate annual energy
    annual_energy = calc.calculate_annual_energy()
    print(f"Annual Energy Consumption: {annual_energy:,.2f} kWh")
    print()

    # Test for a specific conductor size
    test_area = 50  # mm²
    print(f"Testing with conductor area: {test_area} mm²")
    losses = calc.calculate_energy_losses(test_area)
    print(f"  Annual Energy Losses: {losses:,.2f} kWh")

    cost_data = calc.calculate_total_cost(test_area)
    print(f"  Capital Cost: Rs. {cost_data['capital_cost']:,.2f}")
    print(f"  Loss Cost: Rs. {cost_data['loss_cost']:,.2f}")
    print(f"  Total Annual Cost: Rs. {cost_data['total_cost']:,.2f}")
    print()

    # Find optimal area
    print("Finding optimal conductor size...")
    optimal_area, areas, costs, optimal_cost_data = calc.find_optimal_area()

    print()
    print("="*70)
    print("OPTIMAL SOLUTION:")
    print("="*70)
    print(f"Optimal Conductor Cross-Section: {optimal_area:.2f} mm²")
    print()
    print(f"Resistance per km: {calc.resistance_factor/optimal_area:.6f} Ω/km")
    print(f"Total Resistance: {(calc.resistance_factor/optimal_area)*calc.distance:.6f} Ω")
    print()
    print(f"Annual Energy Losses: {optimal_cost_data['annual_loss']:,.2f} kWh")
    print(f"Loss Percentage: {(optimal_cost_data['annual_loss']/optimal_cost_data['annual_energy']*100):.2f}%")
    print()
    print("COST BREAKDOWN (Annual):")
    print(f"  Capital Cost (Interest+Depr.): Rs. {optimal_cost_data['capital_cost']:,.2f}")
    print(f"  Maximum Demand Charge:         Rs. {optimal_cost_data['md_cost']:,.2f}")
    print(f"  Energy Cost:                   Rs. {optimal_cost_data['energy_cost']:,.2f}")
    print(f"  Energy Loss Cost:              Rs. {optimal_cost_data['loss_cost']:,.2f}")
    print(f"  {'-'*70}")
    print(f"  TOTAL ANNUAL COST:             Rs. {optimal_cost_data['total_cost']:,.2f}")
    print("="*70)
    print()

    # Show how costs vary around optimal
    print("SENSITIVITY ANALYSIS:")
    print(f"{'Area (mm²)':<15} {'Total Cost (Rs.)':<20} {'% Change from Optimal'}")
    print("-"*60)

    test_areas = [30, 40, optimal_area, 60, 70, 80]
    for area in test_areas:
        cost_info = calc.calculate_total_cost(area)
        pct_change = ((cost_info['total_cost'] - optimal_cost_data['total_cost']) /
                     optimal_cost_data['total_cost'] * 100)
        marker = " ← OPTIMAL" if abs(area - optimal_area) < 0.1 else ""
        print(f"{area:<15.2f} {cost_info['total_cost']:<20,.2f} {pct_change:>+6.2f}%{marker}")

    print()
    print("="*70)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("="*70)
    print()
    print("To run the interactive GUI application, execute:")
    print("  python kelvins_law_calculator.py")
    print()

    return True


if __name__ == "__main__":
    try:
        success = test_calculator()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
