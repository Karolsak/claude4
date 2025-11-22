"""
Kelvin's Law - Economic Conductor Size Calculator
with Tkinter Visualization and Interactive Sliders
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


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
        """
        Calculate annual energy losses for a given conductor cross-section
        area: cross-section in mm²
        """
        # Resistance per phase per km
        r_per_km = self.resistance_factor / area
        total_resistance = r_per_km * self.distance  # Ω per phase

        # Calculate losses for each load condition
        losses = []
        hours = []

        for kw, pf, hrs in [(self.load1_kw, self.load1_pf, self.load1_hours),
                            (self.load2_kw, self.load2_pf, self.load2_hours),
                            (self.load3_kw, self.load3_pf, self.load3_hours)]:
            _, current = self.calculate_load_parameters(kw, pf)
            # Loss in 3-phase system: P_loss = 3 × I² × R
            loss_kw = 3 * (current ** 2) * total_resistance / 1000
            losses.append(loss_kw)
            hours.append(hrs)

        # Annual energy loss (kWh)
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
        """
        Calculate total annual cost for a given conductor cross-section
        Returns: (total_cost, capital_cost, energy_cost, loss_cost)
        """
        # Capital cost of cable
        cable_cost = (self.cable_cost_per_A * area + self.cable_cost_fixed) * self.distance

        # Annual fixed charges (interest + depreciation)
        annual_fixed_charge = cable_cost * self.interest_depreciation

        # Maximum demand charge
        md = self.calculate_maximum_demand()
        annual_md_charge = md * self.tariff_md

        # Energy cost
        annual_energy = self.calculate_annual_energy()
        annual_energy_cost = annual_energy * self.tariff_energy

        # Energy loss cost
        annual_loss = self.calculate_energy_losses(area)
        annual_loss_cost = annual_loss * self.tariff_energy

        # Total annual cost
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
        # Search range for conductor area (mm²)
        areas = np.linspace(10, 200, 500)
        costs = []
        kelvins_costs = []

        for area in areas:
            result = self.calculate_total_cost(area)
            costs.append(result['total_cost'])
            # Kelvin's law: optimize only capital cost + loss cost
            kelvins_cost = result['capital_cost'] + result['loss_cost']
            kelvins_costs.append(kelvins_cost)

        # Find minimum cost according to Kelvin's law
        min_idx = np.argmin(kelvins_costs)
        optimal_area = areas[min_idx]
        optimal_cost_data = self.calculate_total_cost(optimal_area)

        return optimal_area, areas, costs, optimal_cost_data


class KelvinsLawGUI:
    """GUI Application for Kelvin's Law Calculator"""

    def __init__(self, root):
        self.root = root
        self.root.title("Kelvin's Law - Economic Conductor Size Calculator")
        self.root.geometry("1400x900")

        # Create calculator instance
        self.calc = KelvinsLawCalculator()

        # Create GUI elements
        self.create_widgets()
        self.update_plot()

    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Left panel - Controls
        control_frame = ttk.LabelFrame(main_frame, text="Parameters", padding="10")
        control_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        # Create sliders
        self.create_sliders(control_frame)

        # Right top panel - Plot
        plot_frame = ttk.LabelFrame(main_frame, text="Cost Analysis", padding="10")
        plot_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        # Create matplotlib figure
        self.fig = Figure(figsize=(10, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Right bottom panel - Results and Limitations
        results_frame = ttk.LabelFrame(main_frame, text="Results & Analysis", padding="10")
        results_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Results tab
        results_tab = ttk.Frame(self.notebook)
        self.notebook.add(results_tab, text="Calculation Results")

        self.results_text = tk.Text(results_tab, wrap=tk.WORD, height=10, font=('Courier', 10))
        results_scroll = ttk.Scrollbar(results_tab, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=results_scroll.set)

        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Limitations tab
        limitations_tab = ttk.Frame(self.notebook)
        self.notebook.add(limitations_tab, text="Kelvin's Law Limitations")

        limitations_text = tk.Text(limitations_tab, wrap=tk.WORD, height=10, font=('Arial', 10))
        limitations_scroll = ttk.Scrollbar(limitations_tab, orient=tk.VERTICAL, command=limitations_text.yview)
        limitations_text.configure(yscrollcommand=limitations_scroll.set)

        limitations_content = """
LIMITATIONS OF KELVIN'S LAW:

1. VARIABLE LOAD ASSUMPTION:
   • Kelvin's law assumes constant load throughout the year
   • In reality, loads vary continuously (as shown in this problem with 3 different load levels)
   • The law doesn't accurately account for load diversity and peak variations
   • Solution: Use equivalent continuous load or load factor corrections

2. VOLTAGE DROP NEGLECTED:
   • The law focuses only on economic considerations
   • Ignores voltage regulation requirements (typically ±6% allowed)
   • Larger conductors may be needed for voltage drop rather than economics
   • Critical for long transmission lines and sensitive loads

3. MECHANICAL STRENGTH:
   • Economic size may be too small for mechanical strength
   • Minimum conductor sizes needed for structural integrity
   • Wind, ice loading, and span length requirements may override economics
   • Particularly important for overhead lines

4. STANDARD SIZES:
   • Calculated optimal size may not match commercially available sizes
   • Must round to nearest standard conductor size
   • This introduces deviation from theoretical optimum
   • Example: If optimal is 47.3 mm², must choose 50 mm² or 35 mm²

5. LOAD GROWTH:
   • Law considers only present load conditions
   • Doesn't account for future load growth
   • Replacing undersized conductors later is expensive
   • Should consider 5-10 year load projections

6. TEMPERATURE EFFECTS:
   • Assumes constant conductor resistance
   • Resistance increases with temperature (α ≈ 0.004/°C for copper)
   • Higher losses cause higher temperatures, further increasing resistance
   • Ambient temperature variations not considered

7. SKIN EFFECT AND PROXIMITY:
   • For large AC conductors, skin effect increases effective resistance
   • Proximity effect in bundled conductors
   • These effects not included in basic Kelvin's law formula
   • More significant at higher frequencies and larger sizes

8. COST FLUCTUATIONS:
   • Assumes fixed costs for conductor material and energy
   • Metal prices (copper, aluminum) fluctuate significantly
   • Energy tariffs change over the life of the installation
   • Interest rates and economic conditions vary

9. POWER FACTOR VARIATIONS:
   • This problem shows varying power factors (0.8, 0.9, 1.0)
   • Lower power factor increases current for same kW
   • Higher I²R losses result
   • Kelvin's law needs modification for variable p.f.

10. LIFE CYCLE CONSIDERATIONS:
    • Typically considers single year economics
    • Conductor life may be 25-40 years
    • Doesn't account for salvage value
    • Maintenance costs not included

11. PARALLEL CIRCUITS:
    • Law applies to single circuit
    • For parallel feeders, cost distribution changes
    • Redundancy requirements may dictate larger sizes
    • N-1 contingency planning needed

12. HARMONICS:
    • Modern loads generate harmonics
    • Harmonic currents increase losses
    • May require derating or oversizing
    • Particularly relevant for industrial/commercial installations

PRACTICAL APPLICATION:
Despite these limitations, Kelvin's law provides a good starting point for
conductor sizing. The final selection should consider:
• Economic optimum from Kelvin's law
• Voltage drop calculations
• Mechanical strength requirements
• Standard available sizes
• Future load growth (typically 25-50% margin)
• Regulatory and safety requirements
        """

        limitations_text.insert('1.0', limitations_content)
        limitations_text.configure(state='disabled')

        limitations_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        limitations_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def create_sliders(self, parent):
        """Create parameter sliders"""
        row = 0

        # Distance slider
        ttk.Label(parent, text="Distance (km):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.distance_var = tk.DoubleVar(value=self.calc.distance)
        distance_slider = ttk.Scale(parent, from_=1, to=20, variable=self.distance_var,
                                   orient=tk.HORIZONTAL, command=self.on_slider_change)
        distance_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.distance_label = ttk.Label(parent, text=f"{self.calc.distance:.1f}")
        self.distance_label.grid(row=row, column=2, pady=2)
        row += 1

        # Voltage slider
        ttk.Label(parent, text="Voltage (kV):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.voltage_var = tk.DoubleVar(value=self.calc.voltage)
        voltage_slider = ttk.Scale(parent, from_=3.3, to=33, variable=self.voltage_var,
                                  orient=tk.HORIZONTAL, command=self.on_slider_change)
        voltage_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.voltage_label = ttk.Label(parent, text=f"{self.calc.voltage:.1f}")
        self.voltage_label.grid(row=row, column=2, pady=2)
        row += 1

        # Load 1 parameters
        ttk.Separator(parent, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=3,
                                                         sticky=(tk.W, tk.E), pady=5)
        row += 1
        ttk.Label(parent, text="LOAD 1", font=('Arial', 10, 'bold')).grid(row=row, column=0,
                                                                          columnspan=3, pady=2)
        row += 1

        ttk.Label(parent, text="Power (kW):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.load1_kw_var = tk.DoubleVar(value=self.calc.load1_kw)
        load1_kw_slider = ttk.Scale(parent, from_=100, to=1500, variable=self.load1_kw_var,
                                   orient=tk.HORIZONTAL, command=self.on_slider_change)
        load1_kw_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.load1_kw_label = ttk.Label(parent, text=f"{self.calc.load1_kw:.0f}")
        self.load1_kw_label.grid(row=row, column=2, pady=2)
        row += 1

        ttk.Label(parent, text="Power Factor:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.load1_pf_var = tk.DoubleVar(value=self.calc.load1_pf)
        load1_pf_slider = ttk.Scale(parent, from_=0.6, to=1.0, variable=self.load1_pf_var,
                                   orient=tk.HORIZONTAL, command=self.on_slider_change)
        load1_pf_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.load1_pf_label = ttk.Label(parent, text=f"{self.calc.load1_pf:.2f}")
        self.load1_pf_label.grid(row=row, column=2, pady=2)
        row += 1

        ttk.Label(parent, text="Hours/day:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.load1_hours_var = tk.DoubleVar(value=self.calc.load1_hours)
        load1_hours_slider = ttk.Scale(parent, from_=1, to=24, variable=self.load1_hours_var,
                                      orient=tk.HORIZONTAL, command=self.on_slider_change)
        load1_hours_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.load1_hours_label = ttk.Label(parent, text=f"{self.calc.load1_hours:.0f}")
        self.load1_hours_label.grid(row=row, column=2, pady=2)
        row += 1

        # Load 2 parameters
        ttk.Separator(parent, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=3,
                                                         sticky=(tk.W, tk.E), pady=5)
        row += 1
        ttk.Label(parent, text="LOAD 2", font=('Arial', 10, 'bold')).grid(row=row, column=0,
                                                                          columnspan=3, pady=2)
        row += 1

        ttk.Label(parent, text="Power (kW):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.load2_kw_var = tk.DoubleVar(value=self.calc.load2_kw)
        load2_kw_slider = ttk.Scale(parent, from_=50, to=1000, variable=self.load2_kw_var,
                                   orient=tk.HORIZONTAL, command=self.on_slider_change)
        load2_kw_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.load2_kw_label = ttk.Label(parent, text=f"{self.calc.load2_kw:.0f}")
        self.load2_kw_label.grid(row=row, column=2, pady=2)
        row += 1

        ttk.Label(parent, text="Power Factor:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.load2_pf_var = tk.DoubleVar(value=self.calc.load2_pf)
        load2_pf_slider = ttk.Scale(parent, from_=0.6, to=1.0, variable=self.load2_pf_var,
                                   orient=tk.HORIZONTAL, command=self.on_slider_change)
        load2_pf_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.load2_pf_label = ttk.Label(parent, text=f"{self.calc.load2_pf:.2f}")
        self.load2_pf_label.grid(row=row, column=2, pady=2)
        row += 1

        ttk.Label(parent, text="Hours/day:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.load2_hours_var = tk.DoubleVar(value=self.calc.load2_hours)
        load2_hours_slider = ttk.Scale(parent, from_=1, to=24, variable=self.load2_hours_var,
                                      orient=tk.HORIZONTAL, command=self.on_slider_change)
        load2_hours_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.load2_hours_label = ttk.Label(parent, text=f"{self.calc.load2_hours:.0f}")
        self.load2_hours_label.grid(row=row, column=2, pady=2)
        row += 1

        # Load 3 parameters
        ttk.Separator(parent, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=3,
                                                         sticky=(tk.W, tk.E), pady=5)
        row += 1
        ttk.Label(parent, text="LOAD 3", font=('Arial', 10, 'bold')).grid(row=row, column=0,
                                                                          columnspan=3, pady=2)
        row += 1

        ttk.Label(parent, text="Power (kW):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.load3_kw_var = tk.DoubleVar(value=self.calc.load3_kw)
        load3_kw_slider = ttk.Scale(parent, from_=10, to=500, variable=self.load3_kw_var,
                                   orient=tk.HORIZONTAL, command=self.on_slider_change)
        load3_kw_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.load3_kw_label = ttk.Label(parent, text=f"{self.calc.load3_kw:.0f}")
        self.load3_kw_label.grid(row=row, column=2, pady=2)
        row += 1

        ttk.Label(parent, text="Power Factor:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.load3_pf_var = tk.DoubleVar(value=self.calc.load3_pf)
        load3_pf_slider = ttk.Scale(parent, from_=0.6, to=1.0, variable=self.load3_pf_var,
                                   orient=tk.HORIZONTAL, command=self.on_slider_change)
        load3_pf_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.load3_pf_label = ttk.Label(parent, text=f"{self.calc.load3_pf:.2f}")
        self.load3_pf_label.grid(row=row, column=2, pady=2)
        row += 1

        ttk.Label(parent, text="Hours/day:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.load3_hours_var = tk.DoubleVar(value=self.calc.load3_hours)
        load3_hours_slider = ttk.Scale(parent, from_=1, to=24, variable=self.load3_hours_var,
                                      orient=tk.HORIZONTAL, command=self.on_slider_change)
        load3_hours_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.load3_hours_label = ttk.Label(parent, text=f"{self.calc.load3_hours:.0f}")
        self.load3_hours_label.grid(row=row, column=2, pady=2)
        row += 1

        # Economic parameters
        ttk.Separator(parent, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=3,
                                                         sticky=(tk.W, tk.E), pady=5)
        row += 1
        ttk.Label(parent, text="ECONOMIC PARAMETERS", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, columnspan=3, pady=2)
        row += 1

        ttk.Label(parent, text="Energy Tariff (Rs/kWh):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.tariff_var = tk.DoubleVar(value=self.calc.tariff_energy)
        tariff_slider = ttk.Scale(parent, from_=0.01, to=0.20, variable=self.tariff_var,
                                 orient=tk.HORIZONTAL, command=self.on_slider_change)
        tariff_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.tariff_label = ttk.Label(parent, text=f"{self.calc.tariff_energy:.3f}")
        self.tariff_label.grid(row=row, column=2, pady=2)
        row += 1

        ttk.Label(parent, text="Interest+Depr. (%):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.interest_var = tk.DoubleVar(value=self.calc.interest_depreciation * 100)
        interest_slider = ttk.Scale(parent, from_=5, to=30, variable=self.interest_var,
                                   orient=tk.HORIZONTAL, command=self.on_slider_change)
        interest_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.interest_label = ttk.Label(parent, text=f"{self.calc.interest_depreciation*100:.0f}")
        self.interest_label.grid(row=row, column=2, pady=2)
        row += 1

        # Update button
        ttk.Button(parent, text="Recalculate", command=self.update_plot).grid(
            row=row, column=0, columnspan=3, pady=10)

    def on_slider_change(self, event=None):
        """Handle slider value changes"""
        # Update calculator parameters
        self.calc.distance = self.distance_var.get()
        self.calc.voltage = self.voltage_var.get()

        self.calc.load1_kw = self.load1_kw_var.get()
        self.calc.load1_pf = self.load1_pf_var.get()
        self.calc.load1_hours = self.load1_hours_var.get()

        self.calc.load2_kw = self.load2_kw_var.get()
        self.calc.load2_pf = self.load2_pf_var.get()
        self.calc.load2_hours = self.load2_hours_var.get()

        self.calc.load3_kw = self.load3_kw_var.get()
        self.calc.load3_pf = self.load3_pf_var.get()
        self.calc.load3_hours = self.load3_hours_var.get()

        self.calc.tariff_energy = self.tariff_var.get()
        self.calc.interest_depreciation = self.interest_var.get() / 100

        # Update labels
        self.distance_label.config(text=f"{self.calc.distance:.1f}")
        self.voltage_label.config(text=f"{self.calc.voltage:.1f}")

        self.load1_kw_label.config(text=f"{self.calc.load1_kw:.0f}")
        self.load1_pf_label.config(text=f"{self.calc.load1_pf:.2f}")
        self.load1_hours_label.config(text=f"{self.calc.load1_hours:.0f}")

        self.load2_kw_label.config(text=f"{self.calc.load2_kw:.0f}")
        self.load2_pf_label.config(text=f"{self.calc.load2_pf:.2f}")
        self.load2_hours_label.config(text=f"{self.calc.load2_hours:.0f}")

        self.load3_kw_label.config(text=f"{self.calc.load3_kw:.0f}")
        self.load3_pf_label.config(text=f"{self.calc.load3_pf:.2f}")
        self.load3_hours_label.config(text=f"{self.calc.load3_hours:.0f}")

        self.tariff_label.config(text=f"{self.calc.tariff_energy:.3f}")
        self.interest_label.config(text=f"{self.calc.interest_depreciation*100:.0f}")

        # Update plot
        self.update_plot()

    def update_plot(self):
        """Update the cost analysis plot"""
        # Find optimal area
        optimal_area, areas, costs, cost_data = self.calc.find_optimal_area()

        # Clear previous plots
        self.fig.clear()

        # Create subplots
        ax1 = self.fig.add_subplot(1, 2, 1)
        ax2 = self.fig.add_subplot(1, 2, 2)

        # Plot 1: Total cost vs. conductor area
        ax1.plot(areas, costs, 'b-', linewidth=2, label='Total Annual Cost')
        ax1.axvline(x=optimal_area, color='r', linestyle='--', linewidth=1.5,
                   label=f'Optimal Area = {optimal_area:.2f} mm²')
        ax1.scatter([optimal_area], [cost_data['total_cost']], color='r', s=100, zorder=5)

        ax1.set_xlabel('Conductor Cross-Section (mm²)', fontsize=10)
        ax1.set_ylabel('Total Annual Cost (Rs.)', fontsize=10)
        ax1.set_title('Total Cost vs. Conductor Size', fontsize=11, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=9)

        # Plot 2: Cost breakdown
        # Calculate costs for visualization
        capital_costs = []
        loss_costs = []

        for area in areas:
            data = self.calc.calculate_total_cost(area)
            capital_costs.append(data['capital_cost'])
            loss_costs.append(data['loss_cost'])

        ax2.plot(areas, capital_costs, 'g-', linewidth=2, label='Capital Cost (Interest+Depr.)')
        ax2.plot(areas, loss_costs, 'orange', linewidth=2, label='Energy Loss Cost')
        ax2.axvline(x=optimal_area, color='r', linestyle='--', linewidth=1.5,
                   label=f'Optimal: {optimal_area:.2f} mm²')

        ax2.set_xlabel('Conductor Cross-Section (mm²)', fontsize=10)
        ax2.set_ylabel('Annual Cost (Rs.)', fontsize=10)
        ax2.set_title('Cost Components Analysis', fontsize=11, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=9)

        self.fig.tight_layout()
        self.canvas.draw()

        # Update results text
        self.update_results(optimal_area, cost_data)

    def update_results(self, optimal_area, cost_data):
        """Update the results text display"""
        self.results_text.configure(state='normal')
        self.results_text.delete('1.0', tk.END)

        # Calculate additional parameters
        md = cost_data['max_demand']
        resistance = self.calc.resistance_factor / optimal_area
        total_resistance = resistance * self.calc.distance

        # Calculate current for each load
        kva1, i1 = self.calc.calculate_load_parameters(self.calc.load1_kw, self.calc.load1_pf)
        kva2, i2 = self.calc.calculate_load_parameters(self.calc.load2_kw, self.calc.load2_pf)
        kva3, i3 = self.calc.calculate_load_parameters(self.calc.load3_kw, self.calc.load3_pf)

        results = f"""
{'='*70}
KELVIN'S LAW - ECONOMIC CONDUCTOR SIZE CALCULATION
{'='*70}

INPUT PARAMETERS:
{'─'*70}
Distance                    : {self.calc.distance} km
Voltage (Line)              : {self.calc.voltage} kV
Working Days                : {self.calc.days_per_week} days/week × {self.calc.weeks_per_year} weeks/year

LOAD CYCLE:
  Load 1: {self.calc.load1_kw:.0f} kW at {self.calc.load1_pf:.2f} p.f. for {self.calc.load1_hours:.0f} hours
          ({kva1:.2f} kVA, Current = {i1:.2f} A)

  Load 2: {self.calc.load2_kw:.0f} kW at {self.calc.load2_pf:.2f} p.f. for {self.calc.load2_hours:.0f} hours
          ({kva2:.2f} kVA, Current = {i2:.2f} A)

  Load 3: {self.calc.load3_kw:.0f} kW at {self.calc.load3_pf:.2f} p.f. for {self.calc.load3_hours:.0f} hours
          ({kva3:.2f} kVA, Current = {i3:.2f} A)

ECONOMIC PARAMETERS:
  Cable Cost                : Rs. ({self.calc.cable_cost_per_A}×A + {self.calc.cable_cost_fixed}) per km
  MD Tariff                 : Rs. {self.calc.tariff_md}/annum per kVA
  Energy Tariff             : Rs. {self.calc.tariff_energy}/kWh
  Interest + Depreciation   : {self.calc.interest_depreciation*100}%

{'='*70}
RESULTS:
{'─'*70}
OPTIMAL CONDUCTOR CROSS-SECTION   : {optimal_area:.2f} mm²

ELECTRICAL CHARACTERISTICS:
  Resistance per km         : {resistance:.6f} Ω/km
  Total Resistance          : {total_resistance:.6f} Ω
  Maximum Demand            : {md:.2f} kVA

ENERGY ANALYSIS:
  Annual Energy Consumption : {cost_data['annual_energy']:.2f} kWh
  Annual Energy Losses      : {cost_data['annual_loss']:.2f} kWh
  Loss Percentage           : {(cost_data['annual_loss']/cost_data['annual_energy']*100):.2f}%

COST BREAKDOWN (Annual):
  Capital Cost (15% of investment) : Rs. {cost_data['capital_cost']:,.2f}
  Maximum Demand Charge            : Rs. {cost_data['md_cost']:,.2f}
  Energy Cost                      : Rs. {cost_data['energy_cost']:,.2f}
  Energy Loss Cost                 : Rs. {cost_data['loss_cost']:,.2f}
  {'─'*70}
  TOTAL ANNUAL COST                : Rs. {cost_data['total_cost']:,.2f}

{'='*70}
NOTE: The optimal size is based on Kelvin's Law, which minimizes the sum
      of capital costs and energy loss costs. Please review the
      'Limitations' tab for important considerations before finalizing
      conductor selection.
{'='*70}
"""

        self.results_text.insert('1.0', results)
        self.results_text.configure(state='disabled')


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = KelvinsLawGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
