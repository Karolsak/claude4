"""
Kelvin's Law - Economic Conductor Size Calculator
Interactive Matplotlib Version (No Tkinter Required)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.gridspec import GridSpec


class KelvinsLawCalculator:
    """
    Calculator for finding the most economical conductor cross-section
    using Kelvin's Law
    """

    def __init__(self):
        # Default parameters (from the problem)
        self.distance = 6  # km
        self.voltage = 11  # kV (line voltage)

        # Load cycle parameters
        self.load1_kw = 700
        self.load1_pf = 0.8
        self.load1_hours = 7

        self.load2_kw = 400
        self.load2_pf = 0.9
        self.load2_hours = 3

        self.load3_kw = 88
        self.load3_pf = 1.0
        self.load3_hours = 14

        # Working days
        self.days_per_week = 6
        self.weeks_per_year = 52

        # Economic parameters
        self.cable_cost_per_A = 5000  # Rs. per km per mm²
        self.cable_cost_fixed = 1500  # Rs. per km
        self.tariff_md = 150  # Rs. per annum per kVA
        self.tariff_energy = 0.05  # Rs. per unit (kWh)
        self.interest_depreciation = 0.15  # 15%
        self.resistance_factor = 0.173  # ohm-km per mm²

    def calculate_load_parameters(self, kw, pf):
        """Calculate kVA and current for a given load"""
        kva = kw / pf
        # For 3-phase: I = kVA / (√3 × V_L)
        current = (kva * 1000) / (np.sqrt(3) * self.voltage * 1000)
        return kva, current

    def calculate_energy_losses(self, area):
        """Calculate annual energy losses for a given conductor cross-section"""
        r_per_km = self.resistance_factor / area
        total_resistance = r_per_km * self.distance

        losses = []
        hours = []

        for kw, pf, hrs in [(self.load1_kw, self.load1_pf, self.load1_hours),
                            (self.load2_kw, self.load2_pf, self.load2_hours),
                            (self.load3_kw, self.load3_pf, self.load3_hours)]:
            _, current = self.calculate_load_parameters(kw, pf)
            loss_kw = 3 * (current ** 2) * total_resistance / 1000
            losses.append(loss_kw)
            hours.append(hrs)

        annual_loss = 0
        for loss, hrs in zip(losses, hours):
            annual_loss += loss * hrs * self.days_per_week * self.weeks_per_year

        return annual_loss

    def calculate_maximum_demand(self):
        """Calculate maximum demand in kVA"""
        kva1, _ = self.calculate_load_parameters(self.load1_kw, self.load1_pf)
        kva2, _ = self.calculate_load_parameters(self.load2_kw, self.load2_pf)
        kva3, _ = self.calculate_load_parameters(self.load3_kw, self.load3_pf)
        return max(kva1, kva2, kva3)

    def calculate_annual_energy(self):
        """Calculate total annual energy consumption in kWh"""
        total = 0
        for kw, hrs in [(self.load1_kw, self.load1_hours),
                        (self.load2_kw, self.load2_hours),
                        (self.load3_kw, self.load3_hours)]:
            total += kw * hrs * self.days_per_week * self.weeks_per_year
        return total

    def calculate_total_cost(self, area):
        """Calculate total annual cost for a given conductor cross-section"""
        cable_cost = (self.cable_cost_per_A * area + self.cable_cost_fixed) * self.distance
        annual_fixed_charge = cable_cost * self.interest_depreciation

        md = self.calculate_maximum_demand()
        annual_md_charge = md * self.tariff_md

        annual_energy = self.calculate_annual_energy()
        annual_energy_cost = annual_energy * self.tariff_energy

        annual_loss = self.calculate_energy_losses(area)
        annual_loss_cost = annual_loss * self.tariff_energy

        total_cost = annual_fixed_charge + annual_md_charge + annual_energy_cost + annual_loss_cost

        return {
            'total_cost': total_cost,
            'capital_cost': annual_fixed_charge,
            'md_cost': annual_md_charge,
            'energy_cost': annual_energy_cost,
            'loss_cost': annual_loss_cost,
            'annual_energy': annual_energy,
            'annual_loss': annual_loss,
            'max_demand': md
        }

    def find_optimal_area(self):
        """Find the optimal conductor cross-section using Kelvin's Law"""
        areas = np.linspace(10, 200, 500)
        costs = []
        kelvins_costs = []  # Only capital + loss cost for Kelvin's law

        for area in areas:
            result = self.calculate_total_cost(area)
            costs.append(result['total_cost'])
            # Kelvin's law: optimize only capital cost + loss cost
            kelvins_cost = result['capital_cost'] + result['loss_cost']
            kelvins_costs.append(kelvins_cost)

        min_idx = np.argmin(kelvins_costs)
        optimal_area = areas[min_idx]
        optimal_cost_data = self.calculate_total_cost(optimal_area)

        return optimal_area, areas, costs, optimal_cost_data


class InteractiveKelvinsLaw:
    """Interactive visualization using Matplotlib"""

    def __init__(self):
        self.calc = KelvinsLawCalculator()
        self.setup_figure()
        self.create_sliders()
        self.update_plots()

    def setup_figure(self):
        """Setup the figure and axes"""
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.suptitle('Kelvin\'s Law - Economic Conductor Size Calculator',
                         fontsize=16, fontweight='bold')

        # Create grid layout
        gs = GridSpec(4, 3, figure=self.fig, hspace=0.4, wspace=0.3,
                     left=0.05, right=0.98, top=0.94, bottom=0.05)

        # Main plots
        self.ax_cost = self.fig.add_subplot(gs[0:2, 0:2])
        self.ax_breakdown = self.fig.add_subplot(gs[2:4, 0:2])

        # Text area for results
        self.ax_text = self.fig.add_subplot(gs[0:2, 2])
        self.ax_text.axis('off')

        # Limitations text
        self.ax_limits = self.fig.add_subplot(gs[2:4, 2])
        self.ax_limits.axis('off')

        # Slider axes (will be created in create_sliders)
        self.slider_axes = []
        self.sliders = []

    def create_sliders(self):
        """Create interactive sliders"""
        # Slider positions and parameters
        slider_configs = [
            ('Distance (km)', 1, 20, self.calc.distance),
            ('Voltage (kV)', 3.3, 33, self.calc.voltage),
            ('Load1 kW', 100, 1500, self.calc.load1_kw),
            ('Load1 PF', 0.6, 1.0, self.calc.load1_pf),
            ('Load1 hrs', 1, 24, self.calc.load1_hours),
            ('Load2 kW', 50, 1000, self.calc.load2_kw),
            ('Load2 PF', 0.6, 1.0, self.calc.load2_pf),
            ('Load2 hrs', 1, 24, self.calc.load2_hours),
            ('Load3 kW', 10, 500, self.calc.load3_kw),
            ('Load3 PF', 0.6, 1.0, self.calc.load3_pf),
            ('Load3 hrs', 1, 24, self.calc.load3_hours),
            ('Tariff (Rs/kWh)', 0.01, 0.20, self.calc.tariff_energy),
            ('Int+Depr (%)', 5, 30, self.calc.interest_depreciation * 100),
        ]

        # Position sliders at the bottom
        num_sliders = len(slider_configs)
        bottom_space = 0.02
        slider_height = 0.015
        slider_spacing = 0.025

        for i, (label, vmin, vmax, vinit) in enumerate(slider_configs):
            ax_pos = [0.15, bottom_space + i * slider_spacing, 0.7, slider_height]
            ax = self.fig.add_axes(ax_pos)
            slider = Slider(ax, label, vmin, vmax, valinit=vinit, valstep=(vmax-vmin)/1000)
            slider.on_changed(self.on_slider_change)
            self.slider_axes.append(ax)
            self.sliders.append(slider)

        # Adjust main plot positions to make room for sliders
        slider_bottom = bottom_space + num_sliders * slider_spacing + 0.02

    def on_slider_change(self, val):
        """Handle slider changes"""
        # Update calculator parameters
        self.calc.distance = self.sliders[0].val
        self.calc.voltage = self.sliders[1].val
        self.calc.load1_kw = self.sliders[2].val
        self.calc.load1_pf = self.sliders[3].val
        self.calc.load1_hours = self.sliders[4].val
        self.calc.load2_kw = self.sliders[5].val
        self.calc.load2_pf = self.sliders[6].val
        self.calc.load2_hours = self.sliders[7].val
        self.calc.load3_kw = self.sliders[8].val
        self.calc.load3_pf = self.sliders[9].val
        self.calc.load3_hours = self.sliders[10].val
        self.calc.tariff_energy = self.sliders[11].val
        self.calc.interest_depreciation = self.sliders[12].val / 100

        self.update_plots()

    def update_plots(self):
        """Update all plots and text"""
        # Find optimal area
        optimal_area, areas, costs, cost_data = self.calc.find_optimal_area()

        # Clear previous plots
        self.ax_cost.clear()
        self.ax_breakdown.clear()

        # Plot 1: Total cost vs. conductor area
        self.ax_cost.plot(areas, costs, 'b-', linewidth=2, label='Total Annual Cost')
        self.ax_cost.axvline(x=optimal_area, color='r', linestyle='--', linewidth=2,
                           label=f'Optimal: {optimal_area:.2f} mm²')
        self.ax_cost.scatter([optimal_area], [cost_data['total_cost']],
                           color='r', s=100, zorder=5)
        self.ax_cost.set_xlabel('Conductor Cross-Section (mm²)', fontsize=11)
        self.ax_cost.set_ylabel('Total Annual Cost (Rs.)', fontsize=11)
        self.ax_cost.set_title('Total Cost vs. Conductor Size', fontsize=12, fontweight='bold')
        self.ax_cost.grid(True, alpha=0.3)
        self.ax_cost.legend(fontsize=10)

        # Plot 2: Cost breakdown
        capital_costs = []
        loss_costs = []

        for area in areas:
            data = self.calc.calculate_total_cost(area)
            capital_costs.append(data['capital_cost'])
            loss_costs.append(data['loss_cost'])

        self.ax_breakdown.plot(areas, capital_costs, 'g-', linewidth=2,
                              label='Capital Cost (Interest+Depr.)')
        self.ax_breakdown.plot(areas, loss_costs, 'orange', linewidth=2,
                              label='Energy Loss Cost')
        self.ax_breakdown.axvline(x=optimal_area, color='r', linestyle='--', linewidth=2,
                                 label=f'Optimal: {optimal_area:.2f} mm²')
        self.ax_breakdown.set_xlabel('Conductor Cross-Section (mm²)', fontsize=11)
        self.ax_breakdown.set_ylabel('Annual Cost (Rs.)', fontsize=11)
        self.ax_breakdown.set_title('Cost Components Analysis (Kelvin\'s Law Intersection)',
                                   fontsize=12, fontweight='bold')
        self.ax_breakdown.grid(True, alpha=0.3)
        self.ax_breakdown.legend(fontsize=10)

        # Update results text
        self.update_results_text(optimal_area, cost_data)

        # Update limitations text
        self.update_limitations_text()

        self.fig.canvas.draw_idle()

    def update_results_text(self, optimal_area, cost_data):
        """Update the results text display"""
        self.ax_text.clear()
        self.ax_text.axis('off')

        # Calculate additional parameters
        resistance = self.calc.resistance_factor / optimal_area
        total_resistance = resistance * self.calc.distance

        results = f"""OPTIMAL SOLUTION
{'='*30}

Optimal Area: {optimal_area:.2f} mm²

Resistance: {resistance:.6f} Ω/km
Total R: {total_resistance:.6f} Ω

Max Demand: {cost_data['max_demand']:.2f} kVA

Energy: {cost_data['annual_energy']:,.0f} kWh
Losses: {cost_data['annual_loss']:,.0f} kWh
Loss %: {(cost_data['annual_loss']/cost_data['annual_energy']*100):.2f}%

ANNUAL COSTS (Rs.):
{'─'*30}
Capital: {cost_data['capital_cost']:,.0f}
MD Charge: {cost_data['md_cost']:,.0f}
Energy: {cost_data['energy_cost']:,.0f}
Losses: {cost_data['loss_cost']:,.0f}
{'─'*30}
TOTAL: {cost_data['total_cost']:,.0f}
"""

        self.ax_text.text(0.05, 0.95, results, transform=self.ax_text.transAxes,
                         fontsize=9, verticalalignment='top', fontfamily='monospace',
                         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    def update_limitations_text(self):
        """Update the limitations text display"""
        self.ax_limits.clear()
        self.ax_limits.axis('off')

        limitations = """KELVIN'S LAW LIMITATIONS

1. Variable Load: Assumes constant
   load; real loads vary continuously

2. Voltage Drop: Only economics
   considered, not regulation

3. Mechanical Strength: May be
   too small structurally

4. Standard Sizes: Calculated size
   may not be available

5. Load Growth: Doesn't account
   for future expansion

6. Temperature: Assumes constant
   resistance

7. Power Factor: Complex with
   varying p.f.

8. Cost Changes: Metal & energy
   prices fluctuate

9. Skin Effect: Not included for
   large conductors

10. Life Cycle: Single year focus

See documentation for details.
"""

        self.ax_limits.text(0.05, 0.95, limitations, transform=self.ax_limits.transAxes,
                           fontsize=8, verticalalignment='top', fontfamily='sans-serif',
                           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

    def show(self):
        """Display the interactive plot"""
        plt.show()


def print_detailed_limitations():
    """Print detailed discussion of Kelvin's Law limitations"""
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                  KELVIN'S LAW - DETAILED LIMITATIONS                      ║
╚═══════════════════════════════════════════════════════════════════════════╝

1. VARIABLE LOAD ASSUMPTION:
   • Kelvin's law assumes constant load throughout operation
   • Real loads vary continuously (as shown: 3 different load levels)
   • Doesn't accurately account for load diversity and peak variations
   • Solution: Use equivalent continuous load or load factor corrections

2. VOLTAGE DROP NEGLECTED:
   • Focuses only on economic considerations
   • Ignores voltage regulation requirements (typically ±6% allowed)
   • Larger conductors may be needed for voltage drop rather than economics
   • Critical for long transmission lines and sensitive loads

3. MECHANICAL STRENGTH:
   • Economic size may be too small for mechanical strength
   • Minimum conductor sizes needed for structural integrity
   • Wind, ice loading, and span length requirements may override economics

4. STANDARD SIZES:
   • Calculated optimal size may not match commercially available sizes
   • Must round to nearest standard conductor size
   • Example: If optimal is 47.3 mm², choose 50 mm² or 35 mm²

5. LOAD GROWTH:
   • Considers only present load conditions
   • Doesn't account for future load growth
   • Should consider 5-10 year load projections

6. TEMPERATURE EFFECTS:
   • Assumes constant conductor resistance
   • Resistance increases with temperature (α ≈ 0.004/°C for copper)
   • Higher losses → higher temperatures → higher resistance

7. SKIN EFFECT AND PROXIMITY:
   • For large AC conductors, skin effect increases effective resistance
   • Proximity effect in bundled conductors
   • More significant at higher frequencies and larger sizes

8. COST FLUCTUATIONS:
   • Assumes fixed costs for conductor material and energy
   • Metal prices (copper, aluminum) fluctuate significantly
   • Energy tariffs change over installation life

9. POWER FACTOR VARIATIONS:
   • This problem shows varying power factors (0.8, 0.9, 1.0)
   • Lower power factor increases current for same kW
   • Higher I²R losses result

10. LIFE CYCLE CONSIDERATIONS:
    • Typically considers single year economics
    • Conductor life may be 25-40 years
    • Doesn't account for salvage value
    • Maintenance costs not included

╔═══════════════════════════════════════════════════════════════════════════╗
║                       PRACTICAL RECOMMENDATIONS                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

Despite limitations, Kelvin's law provides a good starting point.
Final selection should consider:

✓ Economic optimum from Kelvin's law
✓ Voltage drop calculations (±6% typical limit)
✓ Mechanical strength requirements
✓ Standard available sizes
✓ Future load growth (25-50% margin typical)
✓ Regulatory and safety requirements
✓ Short circuit capacity
✓ Temperature derating factors

═══════════════════════════════════════════════════════════════════════════
""")


def main():
    """Main function"""
    print("\n" + "="*70)
    print("KELVIN'S LAW - ECONOMIC CONDUCTOR SIZE CALCULATOR")
    print("Interactive Matplotlib Version")
    print("="*70)
    print("\nThis application calculates the most economical conductor cross-section")
    print("for a 3-phase power distribution system using Kelvin's Law.")
    print("\nProblem: Industrial load, 6 km distance, 11 kV, variable load cycle")
    print("\nUSAGE:")
    print("  • Use the sliders at the bottom to adjust parameters")
    print("  • Observe real-time updates in cost curves")
    print("  • Top plot: Total cost vs. conductor size")
    print("  • Middle plot: Cost breakdown (Capital vs. Losses)")
    print("  • Right panels: Results and limitations")
    print("\n" + "="*70 + "\n")

    # Print detailed limitations
    print_detailed_limitations()

    print("\nLaunching interactive visualization...")
    print("Close the plot window to exit.\n")

    # Create and show interactive plot
    app = InteractiveKelvinsLaw()
    app.show()


if __name__ == "__main__":
    main()
