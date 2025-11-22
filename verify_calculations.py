"""
Verification script for Kelvin's Law calculations
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

from kelvins_law_matplotlib import KelvinsLawCalculator


def verify_calculations():
    """Verify all calculations step by step"""
    print("="*80)
    print("KELVIN'S LAW CALCULATOR - DETAILED VERIFICATION")
    print("="*80)
    print()

    calc = KelvinsLawCalculator()

    # Display input parameters
    print("INPUT PARAMETERS:")
    print(f"  Distance: {calc.distance} km")
    print(f"  Voltage: {calc.voltage} kV (line-to-line)")
    print(f"  Working days: {calc.days_per_week} days/week × {calc.weeks_per_year} weeks/year " +
          f"= {calc.days_per_week * calc.weeks_per_year} days/year")
    print()

    print("LOAD CYCLE:")
    print(f"  Load 1: {calc.load1_kw} kW at {calc.load1_pf} p.f. for {calc.load1_hours} hours/day")
    print(f"  Load 2: {calc.load2_kw} kW at {calc.load2_pf} p.f. for {calc.load2_hours} hours/day")
    print(f"  Load 3: {calc.load3_kw} kW at {calc.load3_pf} p.f. for {calc.load3_hours} hours/day")
    print()

    # Verify load calculations
    print("LOAD ANALYSIS:")
    print(f"{'Load':<10} {'kW':<10} {'p.f.':<10} {'kVA':<12} {'Current (A)':<15}")
    print("-"*60)

    for i, (kw, pf, hrs) in enumerate([
        (calc.load1_kw, calc.load1_pf, calc.load1_hours),
        (calc.load2_kw, calc.load2_pf, calc.load2_hours),
        (calc.load3_kw, calc.load3_pf, calc.load3_hours)
    ], 1):
        kva, current = calc.calculate_load_parameters(kw, pf)
        print(f"Load {i:<5} {kw:<10.0f} {pf:<10.2f} {kva:<12.2f} {current:<15.2f}")

    md = calc.calculate_maximum_demand()
    print()
    print(f"Maximum Demand: {md:.2f} kVA")
    print()

    # Annual energy
    annual_energy = calc.calculate_annual_energy()
    print(f"Annual Energy Consumption:")
    for i, (kw, hrs) in enumerate([
        (calc.load1_kw, calc.load1_hours),
        (calc.load2_kw, calc.load2_hours),
        (calc.load3_kw, calc.load3_hours)
    ], 1):
        daily = kw * hrs
        annual = daily * calc.days_per_week * calc.weeks_per_year
        print(f"  Load {i}: {kw} kW × {hrs} hrs × {calc.days_per_week*calc.weeks_per_year} days = {annual:,.0f} kWh")

    print(f"  TOTAL: {annual_energy:,.0f} kWh/year")
    print()

    # Test different conductor sizes
    print("COST ANALYSIS FOR DIFFERENT CONDUCTOR SIZES:")
    print("="*80)
    print(f"{'Area':<8} {'R/km':<10} {'Total R':<10} {'Losses':<12} {'Cap.Cost':<12} {'Loss Cost':<12} {'Total Cost':<12}")
    print(f"{'(mm²)':<8} {'(Ω)':<10} {'(Ω)':<10} {'(kWh)':<12} {'(Rs.)':<12} {'(Rs.)':<12} {'(Rs.)':<12}")
    print("-"*95)

    test_areas = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150]

    min_cost = float('inf')
    optimal_from_test = 10

    for area in test_areas:
        r_per_km = calc.resistance_factor / area
        total_r = r_per_km * calc.distance
        losses = calc.calculate_energy_losses(area)
        cost_data = calc.calculate_total_cost(area)

        print(f"{area:<8.0f} {r_per_km:<10.6f} {total_r:<10.6f} {losses:<12.0f} " +
              f"{cost_data['capital_cost']:<12.0f} {cost_data['loss_cost']:<12.0f} " +
              f"{cost_data['total_cost']:<12.0f}")

        if cost_data['total_cost'] < min_cost:
            min_cost = cost_data['total_cost']
            optimal_from_test = area

    print()
    print(f"Approximate optimal from table: {optimal_from_test} mm²")
    print()

    # Fine-grained search around the optimal
    print("FINE-GRAINED SEARCH:")
    print("="*80)

    # Search in a wider range with finer resolution
    areas_fine = np.linspace(5, 150, 1000)
    costs = []

    for area in areas_fine:
        result = calc.calculate_total_cost(area)
        costs.append(result['total_cost'])

    min_idx = np.argmin(costs)
    optimal_area = areas_fine[min_idx]
    optimal_cost_data = calc.calculate_total_cost(optimal_area)

    print(f"Optimal Conductor Cross-Section: {optimal_area:.2f} mm²")
    print()

    # Show detailed breakdown for optimal size
    r_per_km = calc.resistance_factor / optimal_area
    total_r = r_per_km * calc.distance

    print("OPTIMAL SOLUTION DETAILS:")
    print("-"*80)
    print(f"Conductor Area: {optimal_area:.2f} mm²")
    print(f"Resistance per km: {r_per_km:.6f} Ω/km")
    print(f"Total Resistance: {total_r:.6f} Ω")
    print()

    print("Cable Cost Calculation:")
    cable_cost_total = (calc.cable_cost_per_A * optimal_area + calc.cable_cost_fixed) * calc.distance
    print(f"  Cost per km: Rs. ({calc.cable_cost_per_A} × {optimal_area:.2f} + {calc.cable_cost_fixed})")
    print(f"              = Rs. {calc.cable_cost_per_A * optimal_area + calc.cable_cost_fixed:,.2f} per km")
    print(f"  Total cable cost (6 km): Rs. {cable_cost_total:,.2f}")
    print(f"  Annual charge ({calc.interest_depreciation*100}%): Rs. {optimal_cost_data['capital_cost']:,.2f}")
    print()

    print(f"Annual Energy Losses: {optimal_cost_data['annual_loss']:,.2f} kWh")
    print(f"Loss Percentage: {(optimal_cost_data['annual_loss']/optimal_cost_data['annual_energy']*100):.2f}%")
    print()

    print("ANNUAL COST BREAKDOWN:")
    print(f"  Capital Cost (Interest + Depreciation): Rs. {optimal_cost_data['capital_cost']:>12,.2f}")
    print(f"  Maximum Demand Charge:                  Rs. {optimal_cost_data['md_cost']:>12,.2f}")
    print(f"  Energy Cost:                            Rs. {optimal_cost_data['energy_cost']:>12,.2f}")
    print(f"  Energy Loss Cost:                       Rs. {optimal_cost_data['loss_cost']:>12,.2f}")
    print(f"  {'-'*60}")
    print(f"  TOTAL ANNUAL COST:                      Rs. {optimal_cost_data['total_cost']:>12,.2f}")
    print()

    # Verify Kelvin's Law principle
    print("KELVIN'S LAW VERIFICATION:")
    print("-"*80)
    print("At economic optimum, the annual cost of losses should approximately equal")
    print("the annual fixed charges on the capital cost.")
    print()
    print(f"Capital Cost (annual):     Rs. {optimal_cost_data['capital_cost']:,.2f}")
    print(f"Energy Loss Cost (annual): Rs. {optimal_cost_data['loss_cost']:,.2f}")
    print(f"Ratio: {optimal_cost_data['loss_cost'] / optimal_cost_data['capital_cost']:.3f}")
    print()
    if abs(optimal_cost_data['loss_cost'] / optimal_cost_data['capital_cost'] - 1.0) < 0.3:
        print("✓ Kelvin's Law principle is approximately satisfied!")
    else:
        print("⚠ Note: MD and energy costs dominate, shifting optimum from pure Kelvin's Law")

    print()
    print("="*80)
    print("VERIFICATION COMPLETE")
    print("="*80)

    # Also save a plot
    try:
        import matplotlib.pyplot as plt

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Plot 1: Total cost
        ax1.plot(areas_fine, costs, 'b-', linewidth=2)
        ax1.axvline(x=optimal_area, color='r', linestyle='--', linewidth=2,
                   label=f'Optimal: {optimal_area:.2f} mm²')
        ax1.scatter([optimal_area], [optimal_cost_data['total_cost']],
                   color='r', s=100, zorder=5)
        ax1.set_xlabel('Conductor Cross-Section (mm²)', fontsize=11)
        ax1.set_ylabel('Total Annual Cost (Rs.)', fontsize=11)
        ax1.set_title('Total Cost vs. Conductor Size', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Plot 2: Cost breakdown
        capital_costs = []
        loss_costs = []

        for area in areas_fine:
            data = calc.calculate_total_cost(area)
            capital_costs.append(data['capital_cost'])
            loss_costs.append(data['loss_cost'])

        ax2.plot(areas_fine, capital_costs, 'g-', linewidth=2, label='Capital Cost')
        ax2.plot(areas_fine, loss_costs, 'orange', linewidth=2, label='Loss Cost')
        ax2.axvline(x=optimal_area, color='r', linestyle='--', linewidth=2,
                   label=f'Optimal: {optimal_area:.2f} mm²')
        ax2.set_xlabel('Conductor Cross-Section (mm²)', fontsize=11)
        ax2.set_ylabel('Annual Cost (Rs.)', fontsize=11)
        ax2.set_title('Cost Components (Kelvin\'s Law)', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        plt.tight_layout()
        plt.savefig('kelvins_law_analysis.png', dpi=150, bbox_inches='tight')
        print("\n✓ Analysis plot saved as 'kelvins_law_analysis.png'")

    except Exception as e:
        print(f"\n⚠ Could not save plot: {e}")

    return optimal_area, optimal_cost_data


if __name__ == "__main__":
    verify_calculations()
