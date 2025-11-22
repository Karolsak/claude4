"""
Economical Conductor Cross-Section Calculator using Kelvin's Law
Generates visualizations and saves to PNG files (headless-compatible)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

class EconomicalConductorSolver:
    """Solver for economical conductor cross-section problems"""

    def solve_problem1(self, voltage_kv=110, loads_mw=[20, 5, 6], hours=[6, 12, 10],
                       pf=0.8, fixed_cost=9000, variable_cost=600, interest_rate=10,
                       energy_cost=0.06, resistance_factor=0.176, save_plot=True):
        """
        Solve Problem 1: 3-phase transmission line

        Parameters:
        -----------
        voltage_kv : float
            Line voltage in kV
        loads_mw : list
            Power loads in MW
        hours : list
            Hours for each load
        pf : float
            Power factor (lagging)
        fixed_cost : float
            Fixed cost in Rs/km
        variable_cost : float
            Variable cost in Rs/km/cm²
        interest_rate : float
            Interest and depreciation rate in %
        energy_cost : float
            Energy cost in Rs/kWh
        resistance_factor : float
            Resistance factor (Ω·cm²/km)
        save_plot : bool
            Whether to save visualization
        """

        print("\n" + "="*70)
        print("PROBLEM 1: 3-PHASE TRANSMISSION LINE")
        print("="*70)

        # Convert to base units
        V = voltage_kv * 1000  # V
        P = [mw * 1e6 for mw in loads_mw]  # W

        print("\nINPUT PARAMETERS:")
        print("-" * 70)
        print(f"Voltage:           {voltage_kv} kV (3-phase)")
        print(f"Power Factor:      {pf} lag")
        print(f"\nLoad Cycles (daily):")
        for i, (power, hrs) in enumerate(zip(loads_mw, hours), 1):
            print(f"  Load {i}: {power} MW for {hrs} hours")
        print(f"\nCosts:")
        print(f"  Fixed Cost:      Rs. {fixed_cost}/km")
        print(f"  Variable Cost:   Rs. {variable_cost}/km/cm²")
        print(f"  Interest Rate:   {interest_rate}%")
        print(f"  Energy Cost:     Rs. {energy_cost}/kWh")
        print(f"  Resistance:      {resistance_factor} Ω·cm²/km")

        # Calculate currents for each load (3-phase)
        currents = [p / (np.sqrt(3) * V * pf) for p in P]

        print(f"\nCALCULATED CURRENTS:")
        print("-" * 70)
        for i, (current, hrs) in enumerate(zip(currents, hours), 1):
            print(f"  Load {i}: {current:.2f} A for {hrs} hours")

        # Calculate equivalent RMS current
        I_rms = np.sqrt(sum(I**2 * h for I, h in zip(currents, hours)) / 24)
        print(f"\nRMS Current:       {I_rms:.2f} A")

        # Range of cross-sections to evaluate
        A_range = np.linspace(0.5, 5, 1000)

        # Calculate costs
        capital_costs = []
        energy_costs = []
        total_costs = []

        for A in A_range:
            # Annual capital cost per km
            capital_cost = (fixed_cost + variable_cost * A) * (interest_rate / 100)

            # Resistance per phase per km
            R = resistance_factor / A

            # Annual energy loss (3-phase)
            annual_loss = 3 * I_rms**2 * R * 24 * 365 / 1000  # kWh/km/year

            # Annual energy cost per km
            annual_energy_cost = annual_loss * energy_cost

            # Total annual cost
            total_cost = capital_cost + annual_energy_cost

            capital_costs.append(capital_cost)
            energy_costs.append(annual_energy_cost)
            total_costs.append(total_cost)

        # Find optimal cross-section
        optimal_idx = np.argmin(total_costs)
        optimal_A = A_range[optimal_idx]
        optimal_cost = total_costs[optimal_idx]
        optimal_capital = capital_costs[optimal_idx]
        optimal_energy = energy_costs[optimal_idx]

        # Kelvin's Law formula
        P_factor = 3 * I_rms**2 * 24 * 365 / 1000
        A_kelvin = np.sqrt((P_factor * energy_cost) / (variable_cost * interest_rate / 100))

        # Calculate characteristics at optimal point
        R_optimal = resistance_factor / optimal_A
        annual_loss_optimal = 3 * I_rms**2 * R_optimal * 24 * 365 / 1000

        print(f"\n" + "="*70)
        print("RESULTS:")
        print("="*70)
        print(f"\nOPTIMAL CROSS-SECTION:")
        print(f"  Numerical Optimization: {optimal_A:.4f} cm²")
        print(f"  Kelvin's Law Formula:   {A_kelvin:.4f} cm²")
        print(f"\nANNUAL COSTS (per km):")
        print(f"  Capital Cost:    Rs. {optimal_capital:.2f}")
        print(f"  Energy Cost:     Rs. {optimal_energy:.2f}")
        print(f"  Total Cost:      Rs. {optimal_cost:.2f}")
        print(f"\nSYSTEM CHARACTERISTICS:")
        print(f"  Resistance:      {R_optimal:.4f} Ω/km/phase")
        print(f"  Annual Loss:     {annual_loss_optimal:.2f} kWh/km")
        print(f"  Power Loss:      {3 * I_rms**2 * R_optimal / 1000:.4f} kW/km")

        if save_plot:
            self._plot_problem1(A_range, capital_costs, energy_costs, total_costs,
                              optimal_A, optimal_cost, loads_mw, hours)

        return optimal_A, optimal_cost

    def solve_problem2(self, current=120, voltage=250, energy_cost=0.10,
                       cable_cost=20, length_km=1, interest_rate=8,
                       resistance_factor=0.15, save_plot=True):
        """
        Solve Problem 2: DC feeder system

        Parameters:
        -----------
        current : float
            Current in A
        voltage : float
            Voltage in V
        energy_cost : float
            Energy cost in Rs/kWh
        cable_cost : float
            Cable cost in Rs/m/cm²
        length_km : float
            Length in km
        interest_rate : float
            Interest and depreciation rate in %
        resistance_factor : float
            Resistance in Ω/km/cm²
        save_plot : bool
            Whether to save visualization
        """

        print("\n" + "="*70)
        print("PROBLEM 2: DC FEEDER SYSTEM")
        print("="*70)

        length_m = length_km * 1000  # Convert to meters

        print("\nINPUT PARAMETERS:")
        print("-" * 70)
        print(f"Current:           {current} A")
        print(f"Voltage:           {voltage} V DC")
        print(f"Length:            {length_km} km ({length_m} m)")
        print(f"Cable Cost:        Rs. {cable_cost}/m/cm² (two-core)")
        print(f"Energy Cost:       Rs. {energy_cost}/kWh")
        print(f"Interest Rate:     {interest_rate}%")
        print(f"Resistance:        {resistance_factor} Ω/km/cm²")

        # Range of cross-sections
        A_range = np.linspace(0.5, 10, 1000)

        # Calculate costs
        capital_costs = []
        energy_costs = []
        total_costs = []

        for A in A_range:
            # Total capital cost for two-core cable
            total_capital_cost = cable_cost * A * length_m

            # Annual capital charge
            annual_capital_cost = total_capital_cost * (interest_rate / 100)

            # Total resistance (both cores)
            R_total = 2 * resistance_factor * length_km / A

            # Power loss
            P_loss = current**2 * R_total / 1000  # kW

            # Annual energy loss
            annual_loss = P_loss * 24 * 365  # kWh/year

            # Annual energy cost
            annual_energy_cost = annual_loss * energy_cost

            # Total annual cost
            total_cost = annual_capital_cost + annual_energy_cost

            capital_costs.append(annual_capital_cost)
            energy_costs.append(annual_energy_cost)
            total_costs.append(total_cost)

        # Find optimal cross-section
        optimal_idx = np.argmin(total_costs)
        optimal_A = A_range[optimal_idx]
        optimal_cost = total_costs[optimal_idx]
        optimal_capital = capital_costs[optimal_idx]
        optimal_energy = energy_costs[optimal_idx]

        # Kelvin's Law formula
        numerator = 2 * current**2 * resistance_factor * length_km * 24 * 365 * energy_cost / 1000
        denominator = cable_cost * length_m * (interest_rate / 100)
        A_kelvin = np.sqrt(numerator / denominator)

        # System characteristics at optimal point
        R_optimal = 2 * resistance_factor * length_km / optimal_A
        P_loss_optimal = current**2 * R_optimal / 1000
        voltage_drop = current * R_optimal
        voltage_drop_percent = (voltage_drop / voltage) * 100
        efficiency = (1 - voltage_drop / voltage) * 100
        annual_loss_optimal = P_loss_optimal * 24 * 365

        print(f"\n" + "="*70)
        print("RESULTS:")
        print("="*70)
        print(f"\nOPTIMAL CROSS-SECTION:")
        print(f"  Numerical Optimization: {optimal_A:.4f} cm²")
        print(f"  Kelvin's Law Formula:   {A_kelvin:.4f} cm²")
        print(f"\nANNUAL COSTS:")
        print(f"  Capital Cost:    Rs. {optimal_capital:.2f}")
        print(f"  Energy Cost:     Rs. {optimal_energy:.2f}")
        print(f"  Total Cost:      Rs. {optimal_cost:.2f}")
        print(f"\nSYSTEM CHARACTERISTICS:")
        print(f"  Total Resistance: {R_optimal:.4f} Ω")
        print(f"  Power Loss:       {P_loss_optimal:.4f} kW")
        print(f"  Voltage Drop:     {voltage_drop:.2f} V ({voltage_drop_percent:.2f}%)")
        print(f"  Efficiency:       {efficiency:.2f}%")
        print(f"  Annual Loss:      {annual_loss_optimal:.2f} kWh")

        if save_plot:
            self._plot_problem2(A_range, capital_costs, energy_costs, total_costs,
                              optimal_A, optimal_cost, current, voltage, length_km)

        return optimal_A, optimal_cost

    def _plot_problem1(self, A_range, capital_costs, energy_costs, total_costs,
                      optimal_A, optimal_cost, loads_mw, hours):
        """Create and save plots for Problem 1"""

        # Convert to numpy arrays for boolean indexing
        capital_costs = np.array(capital_costs)
        energy_costs = np.array(energy_costs)
        total_costs = np.array(total_costs)

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Problem 1: 3-Phase Transmission Line - Economical Cross-Section Analysis',
                     fontsize=14, fontweight='bold')

        # Plot 1: Cost breakdown
        ax1 = axes[0, 0]
        ax1.plot(A_range, capital_costs, 'b-', label='Capital Cost', linewidth=2)
        ax1.plot(A_range, energy_costs, 'r-', label='Energy Cost', linewidth=2)
        ax1.plot(A_range, total_costs, 'g-', label='Total Cost', linewidth=2.5)
        ax1.axvline(optimal_A, color='black', linestyle='--', alpha=0.7,
                   label=f'Optimal: {optimal_A:.3f} cm²')
        ax1.set_xlabel('Cross-section (cm²)', fontsize=11)
        ax1.set_ylabel('Annual Cost (Rs/km)', fontsize=11)
        ax1.set_title('Annual Cost vs Cross-section', fontsize=12, fontweight='bold')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)

        # Plot 2: Zoomed view
        ax2 = axes[0, 1]
        zoom_range = (optimal_A - 1 < A_range) & (A_range < optimal_A + 1)
        ax2.plot(A_range[zoom_range], total_costs[zoom_range], 'g-', linewidth=2.5)
        ax2.axvline(optimal_A, color='black', linestyle='--', alpha=0.7)
        ax2.axhline(optimal_cost, color='red', linestyle='--', alpha=0.7)
        ax2.plot(optimal_A, optimal_cost, 'ro', markersize=12,
                label=f'Min: Rs. {optimal_cost:.2f}')
        ax2.set_xlabel('Cross-section (cm²)', fontsize=11)
        ax2.set_ylabel('Total Annual Cost (Rs/km)', fontsize=11)
        ax2.set_title('Zoomed View Around Optimal Point', fontsize=12, fontweight='bold')
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3)

        # Plot 3: Load cycle diagram
        ax3 = axes[1, 0]
        time_points = [0]
        load_points = [loads_mw[0]]
        cumulative_hours = 0
        for load, hrs in zip(loads_mw, hours):
            time_points.append(cumulative_hours)
            time_points.append(cumulative_hours + hrs)
            load_points.append(load)
            load_points.append(load)
            cumulative_hours += hrs

        ax3.plot(time_points[1:], load_points[1:], 'b-', linewidth=2.5)
        ax3.fill_between(time_points[1:], load_points[1:], alpha=0.3)
        ax3.set_xlabel('Time (hours)', fontsize=11)
        ax3.set_ylabel('Load (MW)', fontsize=11)
        ax3.set_title('Daily Load Cycle', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim(0, 24)

        # Plot 4: Cost components pie chart
        ax4 = axes[1, 1]
        costs = [capital_costs[np.argmin(total_costs)],
                energy_costs[np.argmin(total_costs)]]
        labels = [f'Capital Cost\nRs. {costs[0]:.2f}',
                 f'Energy Cost\nRs. {costs[1]:.2f}']
        colors = ['#3498db', '#e74c3c']
        explode = (0.05, 0.05)
        ax4.pie(costs, labels=labels, autopct='%1.1f%%', startangle=90,
               colors=colors, explode=explode, textprops={'fontsize': 10})
        ax4.set_title('Cost Distribution at Optimal Point', fontsize=12, fontweight='bold')

        plt.tight_layout()
        plt.savefig('/home/user/claude4/problem1_analysis.png', dpi=300, bbox_inches='tight')
        print(f"\n✓ Visualization saved: problem1_analysis.png")
        plt.close()

    def _plot_problem2(self, A_range, capital_costs, energy_costs, total_costs,
                      optimal_A, optimal_cost, current, voltage, length):
        """Create and save plots for Problem 2"""

        # Convert to numpy arrays for boolean indexing
        capital_costs = np.array(capital_costs)
        energy_costs = np.array(energy_costs)
        total_costs = np.array(total_costs)

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Problem 2: DC Feeder System - Economical Cross-Section Analysis',
                     fontsize=14, fontweight='bold')

        # Plot 1: Cost breakdown
        ax1 = axes[0, 0]
        ax1.plot(A_range, capital_costs, 'b-', label='Capital Cost', linewidth=2)
        ax1.plot(A_range, energy_costs, 'r-', label='Energy Cost', linewidth=2)
        ax1.plot(A_range, total_costs, 'g-', label='Total Cost', linewidth=2.5)
        ax1.axvline(optimal_A, color='black', linestyle='--', alpha=0.7,
                   label=f'Optimal: {optimal_A:.3f} cm²')
        ax1.set_xlabel('Cross-section (cm²)', fontsize=11)
        ax1.set_ylabel('Annual Cost (Rs)', fontsize=11)
        ax1.set_title('Annual Cost vs Cross-section', fontsize=12, fontweight='bold')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)

        # Plot 2: Zoomed view
        ax2 = axes[0, 1]
        zoom_range = (optimal_A - 2 < A_range) & (A_range < optimal_A + 2)
        ax2.plot(A_range[zoom_range], total_costs[zoom_range], 'g-', linewidth=2.5)
        ax2.axvline(optimal_A, color='black', linestyle='--', alpha=0.7)
        ax2.axhline(optimal_cost, color='red', linestyle='--', alpha=0.7)
        ax2.plot(optimal_A, optimal_cost, 'ro', markersize=12,
                label=f'Min: Rs. {optimal_cost:.2f}')
        ax2.set_xlabel('Cross-section (cm²)', fontsize=11)
        ax2.set_ylabel('Total Annual Cost (Rs)', fontsize=11)
        ax2.set_title('Zoomed View Around Optimal Point', fontsize=12, fontweight='bold')
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3)

        # Plot 3: Voltage drop vs cross-section
        ax3 = axes[1, 0]
        resistance_factor = 0.15
        voltage_drops = [(current * 2 * resistance_factor * length / A) for A in A_range]
        voltage_drop_percent = [(vd / voltage * 100) for vd in voltage_drops]

        ax3_twin = ax3.twinx()
        line1 = ax3.plot(A_range, voltage_drops, 'b-', linewidth=2, label='Voltage Drop (V)')
        line2 = ax3_twin.plot(A_range, voltage_drop_percent, 'r-', linewidth=2,
                             label='Voltage Drop (%)')
        ax3.axvline(optimal_A, color='black', linestyle='--', alpha=0.7)
        ax3.set_xlabel('Cross-section (cm²)', fontsize=11)
        ax3.set_ylabel('Voltage Drop (V)', fontsize=11, color='b')
        ax3_twin.set_ylabel('Voltage Drop (%)', fontsize=11, color='r')
        ax3.set_title('Voltage Drop vs Cross-section', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)

        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax3.legend(lines, labels, loc='upper right', fontsize=9)

        # Plot 4: Cost components pie chart
        ax4 = axes[1, 1]
        costs = [capital_costs[np.argmin(total_costs)],
                energy_costs[np.argmin(total_costs)]]
        labels = [f'Capital Cost\nRs. {costs[0]:.2f}',
                 f'Energy Cost\nRs. {costs[1]:.2f}']
        colors = ['#3498db', '#e74c3c']
        explode = (0.05, 0.05)
        ax4.pie(costs, labels=labels, autopct='%1.1f%%', startangle=90,
               colors=colors, explode=explode, textprops={'fontsize': 10})
        ax4.set_title('Cost Distribution at Optimal Point', fontsize=12, fontweight='bold')

        plt.tight_layout()
        plt.savefig('/home/user/claude4/problem2_analysis.png', dpi=300, bbox_inches='tight')
        print(f"\n✓ Visualization saved: problem2_analysis.png")
        plt.close()


def main():
    """Main function to solve both problems"""

    print("\n" + "="*70)
    print(" ECONOMICAL CONDUCTOR CROSS-SECTION CALCULATOR ")
    print(" Using Kelvin's Law ")
    print("="*70)

    solver = EconomicalConductorSolver()

    # Solve Problem 1
    optimal_A1, optimal_cost1 = solver.solve_problem1()

    print("\n" + "="*70 + "\n")

    # Solve Problem 2
    optimal_A2, optimal_cost2 = solver.solve_problem2()

    print("\n" + "="*70)
    print(" SUMMARY ")
    print("="*70)
    print(f"\nProblem 1 (3-Phase Transmission Line):")
    print(f"  Optimal Cross-section: {optimal_A1:.4f} cm²")
    print(f"  Minimum Annual Cost:   Rs. {optimal_cost1:.2f}/km")

    print(f"\nProblem 2 (DC Feeder System):")
    print(f"  Optimal Cross-section: {optimal_A2:.4f} cm²")
    print(f"  Minimum Annual Cost:   Rs. {optimal_cost2:.2f}")

    print("\n" + "="*70)
    print("\nVisualizations saved as PNG files:")
    print("  - problem1_analysis.png")
    print("  - problem2_analysis.png")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
