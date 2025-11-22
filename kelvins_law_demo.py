"""
Comprehensive Kelvin's Law Demonstration
Shows calculations, optimal size, and practical limitations
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from kelvins_law_matplotlib import KelvinsLawCalculator


def kelvin_law_demonstration():
    """Complete demonstration of Kelvin's Law with limitations"""

    print("\n" + "="*85)
    print(" "*20 + "KELVIN'S LAW - ECONOMIC CONDUCTOR SIZE CALCULATOR")
    print("="*85)
    print()

    calc = KelvinsLawCalculator()

    # Problem statement
    print("PROBLEM STATEMENT:")
    print("-" * 85)
    print(f"An industrial load is supplied by a 3-phase cable from a sub-station.")
    print(f"Distance: {calc.distance} km")
    print(f"Voltage: {calc.voltage} kV (line-to-line)")
    print(f"\nDaily load cycle (6 days/week for entire year):")
    print(f"  • {calc.load1_kw} kW at {calc.load1_pf} p.f. for {calc.load1_hours} hours")
    print(f"  • {calc.load2_kw} kW at {calc.load2_pf} p.f. for {calc.load2_hours} hours")
    print(f"  • {calc.load3_kw} kW at unity p.f. for {calc.load3_hours} hours")
    print(f"\nCable cost: Rs. ({calc.cable_cost_per_A}A + {calc.cable_cost_fixed}) per km")
    print(f"Tariff: Rs. {calc.tariff_md}/annum per kVA of M.D. + {calc.tariff_energy} Rs/kWh")
    print(f"Interest + Depreciation: {calc.interest_depreciation*100}%")
    print(f"Resistance: {calc.resistance_factor}/A Ω-km (A in mm²)")
    print()

    # Load analysis
    print("="*85)
    print("STEP 1: LOAD ANALYSIS")
    print("="*85)
    print(f"\n{'Load':<8} {'Power':<12} {'p.f.':<8} {'kVA':<12} {'Current (A)':<15}")
    print("-" * 60)

    loads_data = []
    for i, (kw, pf, hrs) in enumerate([
        (calc.load1_kw, calc.load1_pf, calc.load1_hours),
        (calc.load2_kw, calc.load2_pf, calc.load2_hours),
        (calc.load3_kw, calc.load3_pf, calc.load3_hours)
    ], 1):
        kva, current = calc.calculate_load_parameters(kw, pf)
        loads_data.append((kw, pf, hrs, kva, current))
        print(f"Load {i}   {kw:<12.0f} {pf:<8.2f} {kva:<12.2f} {current:<15.2f}")

    md = calc.calculate_maximum_demand()
    max_current = max(ld[4] for ld in loads_data)
    print(f"\nMaximum Demand (MD): {md:.2f} kVA")
    print(f"Maximum Current: {max_current:.2f} A")
    print()

    # Energy consumption
    print("="*85)
    print("STEP 2: ANNUAL ENERGY CONSUMPTION")
    print("="*85)
    print()

    working_days = calc.days_per_week * calc.weeks_per_year
    total_energy = 0

    for i, (kw, pf, hrs, kva, current) in enumerate(loads_data, 1):
        daily = kw * hrs
        annual = daily * working_days
        total_energy += annual
        print(f"Load {i}: {kw:.0f} kW × {hrs} hrs/day × {working_days} days/year = {annual:,.0f} kWh")

    print(f"\nTotal Annual Energy Consumption: {total_energy:,.0f} kWh/year")
    print()

    # Kelvin's Law Optimization
    print("="*85)
    print("STEP 3: KELVIN'S LAW OPTIMIZATION")
    print("="*85)
    print()
    print("Kelvin's Law states that the most economical conductor size is achieved when:")
    print("  Annual cost of energy losses = Annual fixed charges on capital")
    print()
    print("We minimize: Total Cost = Capital Cost (annual) + Energy Loss Cost (annual)")
    print()

    # Calculate for various sizes
    print(f"{'Area':<8} {'Resistance':<12} {'Annual':<12} {'Capital':<14} {'Loss':<12} {'Relevant':<14}")
    print(f"{'(mm²)':<8} {'R_total (Ω)':<12} {'Loss(kWh)':<12} {'Cost (Rs.)':<14} {'Cost(Rs.)':<12} {'Total (Rs.)':<14}")
    print("-" * 85)

    test_areas = [10, 20, 30, 40, 50, 60, 70, 80, 100, 120, 150]
    min_kelvin_cost = float('inf')
    optimal_area_approx = 10

    for area in test_areas:
        r_total = (calc.resistance_factor / area) * calc.distance
        annual_loss = calc.calculate_energy_losses(area)
        cost_data = calc.calculate_total_cost(area)

        # Kelvin's law: only capital + loss
        kelvin_cost = cost_data['capital_cost'] + cost_data['loss_cost']

        marker = ""
        if kelvin_cost < min_kelvin_cost:
            min_kelvin_cost = kelvin_cost
            optimal_area_approx = area
            marker = " ←"

        print(f"{area:<8.0f} {r_total:<12.6f} {annual_loss:<12.0f} {cost_data['capital_cost']:<14,.0f} " +
              f"{cost_data['loss_cost']:<12.2f} {kelvin_cost:<14,.2f}{marker}")

    print()

    # Fine search
    areas_fine = np.linspace(5, 150, 1000)
    kelvin_costs = []
    capital_costs_arr = []
    loss_costs_arr = []

    for area in areas_fine:
        cost_data = calc.calculate_total_cost(area)
        kelvin_cost = cost_data['capital_cost'] + cost_data['loss_cost']
        kelvin_costs.append(kelvin_cost)
        capital_costs_arr.append(cost_data['capital_cost'])
        loss_costs_arr.append(cost_data['loss_cost'])

    min_idx = np.argmin(kelvin_costs)
    optimal_area = areas_fine[min_idx]
    optimal_data = calc.calculate_total_cost(optimal_area)

    print("="*85)
    print("OPTIMAL SOLUTION (According to Kelvin's Law)")
    print("="*85)
    print(f"\n✓ Optimal Conductor Cross-Section: {optimal_area:.2f} mm²")
    print()

    r_opt = calc.resistance_factor / optimal_area
    r_total_opt = r_opt * calc.distance

    print("Electrical Characteristics:")
    print(f"  Resistance per km:     {r_opt:.6f} Ω/km")
    print(f"  Total Resistance:      {r_total_opt:.6f} Ω")
    print(f"  Maximum Current:       {max_current:.2f} A")
    vdrop_volts = np.sqrt(3) * max_current * r_total_opt
    vdrop_pct_opt = vdrop_volts / (calc.voltage * 1000) * 100
    print(f"  Voltage Drop at max load: {vdrop_volts:.3f} V " +
          f"({vdrop_pct_opt:.2f}%)")
    print()

    print("Annual Energy:")
    print(f"  Energy Consumption:    {optimal_data['annual_energy']:,.0f} kWh")
    print(f"  Energy Losses:         {optimal_data['annual_loss']:,.0f} kWh")
    print(f"  Loss Percentage:       {optimal_data['annual_loss']/optimal_data['annual_energy']*100:.3f}%")
    print()

    cable_cost = (calc.cable_cost_per_A * optimal_area + calc.cable_cost_fixed) * calc.distance

    print("Cost Breakdown (Annual):")
    print(f"  Cable Cost:            Rs. {cable_cost:,.2f} (one-time)")
    print(f"  Capital Charge (15%):  Rs. {optimal_data['capital_cost']:,.2f}")
    print(f"  Energy Loss Cost:      Rs. {optimal_data['loss_cost']:,.2f}")
    print(f"  {'─' * 50}")
    print(f"  Kelvin's Cost:         Rs. {optimal_data['capital_cost'] + optimal_data['loss_cost']:,.2f}")
    print()
    print("Additional Fixed Costs (not part of Kelvin's optimization):")
    print(f"  MD Charge:             Rs. {optimal_data['md_cost']:,.2f}")
    print(f"  Energy Cost:           Rs. {optimal_data['energy_cost']:,.2f}")
    print(f"  {'─' * 50}")
    print(f"  Total Annual Cost:     Rs. {optimal_data['total_cost']:,.2f}")
    print()

    # Verify Kelvin's Law
    ratio = optimal_data['loss_cost'] / optimal_data['capital_cost']
    print("Kelvin's Law Verification:")
    print(f"  Capital Cost / Loss Cost Ratio: {1/ratio:.2f}")
    if ratio < 0.1:
        print(f"  ⚠  Loss cost is much smaller than capital cost ({ratio:.4f})")
        print(f"     This indicates energy tariff is very low relative to capital costs.")
    print()

    # Practical considerations
    print("="*85)
    print("PRACTICAL CONSIDERATIONS & LIMITATIONS")
    print("="*85)
    print()

    # Check current density
    area_mm2 = optimal_area
    current_density = max_current / area_mm2  # A/mm²

    print(f"1. CURRENT CARRYING CAPACITY:")
    print(f"   Calculated optimal area: {optimal_area:.2f} mm²")
    print(f"   Maximum current: {max_current:.2f} A")
    print(f"   Current density: {current_density:.2f} A/mm²")
    print(f"   Typical safe limit for copper: 2-4 A/mm²")
    if current_density > 4:
        print(f"   ⚠  WARNING: Current density too high! Risk of overheating.")
        suggested_area_current = max_current / 3  # Using 3 A/mm²
        print(f"   → Suggested minimum for current: {suggested_area_current:.0f} mm²")
    else:
        print(f"   ✓ Current density is acceptable.")
    print()

    # Check voltage drop
    vdrop_volts = np.sqrt(3) * max_current * r_total_opt
    vdrop_pct = vdrop_volts / (calc.voltage * 1000) * 100
    print(f"2. VOLTAGE DROP:")
    print(f"   Voltage drop at maximum load: {vdrop_volts:.2f} V ({vdrop_pct:.2f}%)")
    print(f"   Typical acceptable limit: 3-6%")
    if vdrop_pct > 6:
        print(f"   ⚠  WARNING: Voltage drop exceeds limits!")
        # For 5% drop: V_drop = √3 × I × R, so R = V_drop / (√3 × I)
        # R = (0.05 × V) / (√3 × I), A = ρ × L / R
        max_r_for_5pct = (0.05 * calc.voltage * 1000) / (np.sqrt(3) * max_current)
        suggested_area_vdrop = (calc.resistance_factor * calc.distance) / max_r_for_5pct
        print(f"   → Suggested minimum for 5% drop: {suggested_area_vdrop:.0f} mm²")
    else:
        print(f"   ✓ Voltage drop is acceptable.")
    print()

    # Standard sizes
    print(f"3. STANDARD CONDUCTOR SIZES:")
    standard_sizes = [10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240]
    print(f"   Calculated optimal: {optimal_area:.2f} mm²")
    print(f"   Available standard sizes (mm²): {standard_sizes}")

    # Find nearest standard sizes
    larger_standard = [s for s in standard_sizes if s >= optimal_area]
    smaller_standard = [s for s in standard_sizes if s <= optimal_area]

    if larger_standard:
        print(f"   → Nearest larger standard: {larger_standard[0]} mm²")
    if smaller_standard:
        print(f"   → Nearest smaller standard: {smaller_standard[-1]} mm²")
    print()

    # Recommendation
    print(f"4. FINAL RECOMMENDATION:")
    print(f"   Considering all factors:")

    # Determine practical minimum
    practical_min = optimal_area
    reasons = []

    if current_density > 4:
        practical_min = max(practical_min, max_current / 3)
        reasons.append("current capacity")

    if vdrop_pct > 5:
        max_r_for_5pct = (0.05 * calc.voltage * 1000) / (np.sqrt(3) * max_current)
        suggested_area_vdrop = (calc.resistance_factor * calc.distance) / max_r_for_5pct
        practical_min = max(practical_min, suggested_area_vdrop)
        reasons.append("voltage drop")

    # Add safety margin for future load growth (25%)
    practical_min_with_margin = practical_min * 1.25
    reasons.append("25% future growth margin")

    # Round to nearest standard size
    final_standard = min([s for s in standard_sizes if s >= practical_min_with_margin],
                        default=standard_sizes[-1])

    print(f"   • Kelvin's law optimal: {optimal_area:.0f} mm²")
    print(f"   • Practical minimum (considering {', '.join(reasons)}): {practical_min_with_margin:.0f} mm²")
    print(f"   • Recommended standard size: {final_standard} mm²")
    print()

    # Compare costs
    final_data = calc.calculate_total_cost(final_standard)
    cost_increase = final_data['total_cost'] - optimal_data['total_cost']
    pct_increase = cost_increase / optimal_data['total_cost'] * 100

    print(f"   Cost comparison:")
    print(f"   • At {optimal_area:.0f} mm² (Kelvin's optimal): Rs. {optimal_data['total_cost']:,.2f}/year")
    print(f"   • At {final_standard} mm² (Recommended):  Rs. {final_data['total_cost']:,.2f}/year")
    print(f"   • Increase: Rs. {cost_increase:,.2f}/year ({pct_increase:.2f}%)")
    print()

    # Create visualization
    create_visualization(areas_fine, capital_costs_arr, loss_costs_arr, kelvin_costs,
                        optimal_area, final_standard, calc)

    print("="*85)
    print("KEY LIMITATIONS OF KELVIN'S LAW DEMONSTRATED:")
    print("="*85)
    print()
    print("1. ⚠  IGNORES VOLTAGE DROP - Can result in unacceptable voltage regulation")
    print("2. ⚠  IGNORES CURRENT CAPACITY - May select conductors that overheat")
    print("3. ⚠  LOW ENERGY COSTS - When tariffs are low, pushes toward minimum size")
    print("4. ⚠  STANDARD SIZES - Calculated size may not be commercially available")
    print("5. ⚠  NO FUTURE GROWTH - Doesn't account for load increases")
    print("6. ⚠  ASSUMES CONSTANT LOAD - Real loads vary; uses equivalent calculations")
    print("7. ⚠  MECHANICAL STRENGTH - Doesn't consider structural requirements")
    print()
    print("CONCLUSION:")
    print("Kelvin's Law provides an economic starting point, but practical conductor")
    print("selection must also consider voltage drop, current capacity, standard sizes,")
    print("and future load growth. The final selection often differs significantly from")
    print("the pure economic optimum.")
    print("="*85)
    print()


def create_visualization(areas, capital_costs, loss_costs, kelvin_costs,
                        optimal_area, recommended_area, calc):
    """Create and save visualization plots"""

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Kelvin's Law - Economic Conductor Size Analysis",
                fontsize=16, fontweight='bold')

    # Plot 1: Kelvin's cost components
    ax1 = axes[0, 0]
    ax1.plot(areas, capital_costs, 'g-', linewidth=2.5, label='Capital Cost (Annual)')
    ax1.plot(areas, loss_costs, 'orange', linewidth=2.5, label='Energy Loss Cost')
    ax1.plot(areas, kelvin_costs, 'b--', linewidth=2, label='Total (Kelvin\'s Law)', alpha=0.7)
    ax1.axvline(x=optimal_area, color='r', linestyle='--', linewidth=1.5,
               label=f'Optimal (Kelvin): {optimal_area:.0f} mm²', alpha=0.7)
    ax1.axvline(x=recommended_area, color='purple', linestyle='--', linewidth=1.5,
               label=f'Recommended: {recommended_area} mm²', alpha=0.7)
    ax1.set_xlabel('Conductor Cross-Section (mm²)', fontsize=12)
    ax1.set_ylabel('Annual Cost (Rs.)', fontsize=12)
    ax1.set_title('Kelvin\'s Law Cost Components', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)
    ax1.set_xlim(5, 150)

    # Plot 2: Voltage drop
    ax2 = axes[0, 1]
    max_current = 45.93  # From Load 1
    voltage_drops = []
    for area in areas:
        r_total = (calc.resistance_factor / area) * calc.distance
        vdrop_pct = np.sqrt(3) * max_current * r_total / calc.voltage * 100
        voltage_drops.append(vdrop_pct)

    ax2.plot(areas, voltage_drops, 'b-', linewidth=2.5)
    ax2.axhline(y=5, color='orange', linestyle='--', linewidth=1.5,
               label='Typical Limit (5%)', alpha=0.7)
    ax2.axhline(y=6, color='r', linestyle='--', linewidth=1.5,
               label='Maximum Limit (6%)', alpha=0.7)
    ax2.axvline(x=optimal_area, color='r', linestyle=':', linewidth=1.5,
               label=f'Kelvin Optimal: {optimal_area:.0f} mm²', alpha=0.7)
    ax2.axvline(x=recommended_area, color='purple', linestyle='--', linewidth=1.5,
               label=f'Recommended: {recommended_area} mm²', alpha=0.7)
    ax2.set_xlabel('Conductor Cross-Section (mm²)', fontsize=12)
    ax2.set_ylabel('Voltage Drop (%)', fontsize=12)
    ax2.set_title('Voltage Drop vs. Conductor Size', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=9)
    ax2.set_xlim(5, 150)

    # Plot 3: Current density
    ax3 = axes[1, 0]
    current_densities = [max_current / area for area in areas]

    ax3.plot(areas, current_densities, 'b-', linewidth=2.5)
    ax3.axhspan(2, 4, color='green', alpha=0.2, label='Safe Range (2-4 A/mm²)')
    ax3.axhline(y=4, color='orange', linestyle='--', linewidth=1.5, alpha=0.7)
    ax3.axhline(y=2, color='green', linestyle='--', linewidth=1.5, alpha=0.7)
    ax3.axvline(x=optimal_area, color='r', linestyle=':', linewidth=1.5,
               label=f'Kelvin Optimal: {optimal_area:.0f} mm²', alpha=0.7)
    ax3.axvline(x=recommended_area, color='purple', linestyle='--', linewidth=1.5,
               label=f'Recommended: {recommended_area} mm²', alpha=0.7)
    ax3.set_xlabel('Conductor Cross-Section (mm²)', fontsize=12)
    ax3.set_ylabel('Current Density (A/mm²)', fontsize=12)
    ax3.set_title('Current Density vs. Conductor Size', fontsize=13, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.legend(fontsize=9)
    ax3.set_xlim(5, 150)
    ax3.set_ylim(0, min(10, max(current_densities)))

    # Plot 4: Total annual cost
    ax4 = axes[1, 1]
    total_costs = []
    for area in areas:
        cost_data = calc.calculate_total_cost(area)
        total_costs.append(cost_data['total_cost'])

    ax4.plot(areas, total_costs, 'b-', linewidth=2.5, label='Total Annual Cost')
    ax4.axvline(x=optimal_area, color='r', linestyle='--', linewidth=1.5,
               label=f'Kelvin Optimal: {optimal_area:.0f} mm²', alpha=0.7)
    ax4.axvline(x=recommended_area, color='purple', linestyle='--', linewidth=1.5,
               label=f'Recommended: {recommended_area} mm²', alpha=0.7)
    ax4.set_xlabel('Conductor Cross-Section (mm²)', fontsize=12)
    ax4.set_ylabel('Total Annual Cost (Rs.)', fontsize=12)
    ax4.set_title('Total Annual Cost (including MD and Energy)', fontsize=13, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    ax4.legend(fontsize=10)
    ax4.set_xlim(5, 150)

    plt.tight_layout()
    plt.savefig('kelvins_law_complete_analysis.png', dpi=150, bbox_inches='tight')
    print("\n✓ Complete analysis saved as 'kelvins_law_complete_analysis.png'\n")


if __name__ == "__main__":
    kelvin_law_demonstration()
