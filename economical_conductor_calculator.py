"""
Economical Conductor Cross-Section Calculator using Kelvin's Law
Two problems with Tkinter visualization and interactive sliders
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class EconomicalConductorCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Economical Conductor Cross-Section Calculator - Kelvin's Law")
        self.root.geometry("1400x900")

        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Create frames for each problem
        self.problem1_frame = ttk.Frame(self.notebook)
        self.problem2_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.problem1_frame, text="Problem 1: 3-Phase Transmission Line")
        self.notebook.add(self.problem2_frame, text="Problem 2: DC Feeder System")

        # Initialize Problem 1
        self.init_problem1()

        # Initialize Problem 2
        self.init_problem2()

    def init_problem1(self):
        """Initialize Problem 1: 3-phase transmission line"""

        # Parameters frame
        params_frame = ttk.LabelFrame(self.problem1_frame, text="Parameters", padding=10)
        params_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Default values
        self.p1_voltage = tk.DoubleVar(value=110)  # kV
        self.p1_load1_mw = tk.DoubleVar(value=20)  # MW
        self.p1_load1_hours = tk.DoubleVar(value=6)  # hours
        self.p1_load2_mw = tk.DoubleVar(value=5)  # MW
        self.p1_load2_hours = tk.DoubleVar(value=12)  # hours
        self.p1_load3_mw = tk.DoubleVar(value=6)  # MW
        self.p1_load3_hours = tk.DoubleVar(value=10)  # hours
        self.p1_pf = tk.DoubleVar(value=0.8)  # power factor
        self.p1_fixed_cost = tk.DoubleVar(value=9000)  # Rs per km
        self.p1_variable_cost = tk.DoubleVar(value=600)  # Rs per km per cm²
        self.p1_interest_rate = tk.DoubleVar(value=10)  # %
        self.p1_energy_cost = tk.DoubleVar(value=0.06)  # Rs per kWh
        self.p1_resistance_factor = tk.DoubleVar(value=0.176)  # ohm-cm² per km

        row = 0
        # Voltage slider
        self.create_slider(params_frame, "Voltage (kV):", self.p1_voltage, 50, 220, row,
                          command=lambda v: self.calculate_problem1())
        row += 1

        # Load 1
        ttk.Label(params_frame, text="Load Cycle 1:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, columnspan=4, sticky='w', pady=(10,5))
        row += 1
        self.create_slider(params_frame, "Power (MW):", self.p1_load1_mw, 1, 50, row,
                          command=lambda v: self.calculate_problem1())
        row += 1
        self.create_slider(params_frame, "Hours:", self.p1_load1_hours, 0, 24, row,
                          command=lambda v: self.calculate_problem1())
        row += 1

        # Load 2
        ttk.Label(params_frame, text="Load Cycle 2:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, columnspan=4, sticky='w', pady=(10,5))
        row += 1
        self.create_slider(params_frame, "Power (MW):", self.p1_load2_mw, 1, 50, row,
                          command=lambda v: self.calculate_problem1())
        row += 1
        self.create_slider(params_frame, "Hours:", self.p1_load2_hours, 0, 24, row,
                          command=lambda v: self.calculate_problem1())
        row += 1

        # Load 3
        ttk.Label(params_frame, text="Load Cycle 3:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, columnspan=4, sticky='w', pady=(10,5))
        row += 1
        self.create_slider(params_frame, "Power (MW):", self.p1_load3_mw, 1, 50, row,
                          command=lambda v: self.calculate_problem1())
        row += 1
        self.create_slider(params_frame, "Hours:", self.p1_load3_hours, 0, 24, row,
                          command=lambda v: self.calculate_problem1())
        row += 1

        # Power factor
        self.create_slider(params_frame, "Power Factor:", self.p1_pf, 0.5, 1.0, row,
                          command=lambda v: self.calculate_problem1())
        row += 1

        # Costs
        self.create_slider(params_frame, "Fixed Cost (Rs/km):", self.p1_fixed_cost, 5000, 15000, row,
                          command=lambda v: self.calculate_problem1())
        row += 1
        self.create_slider(params_frame, "Variable Cost (Rs/km/cm²):", self.p1_variable_cost, 200, 1000, row,
                          command=lambda v: self.calculate_problem1())
        row += 1
        self.create_slider(params_frame, "Interest Rate (%):", self.p1_interest_rate, 5, 20, row,
                          command=lambda v: self.calculate_problem1())
        row += 1
        self.create_slider(params_frame, "Energy Cost (Rs/kWh):", self.p1_energy_cost, 0.02, 0.15, row,
                          command=lambda v: self.calculate_problem1(), resolution=0.01)
        row += 1
        self.create_slider(params_frame, "Resistance Factor (Ω·cm²/km):", self.p1_resistance_factor,
                          0.1, 0.3, row, command=lambda v: self.calculate_problem1(), resolution=0.001)

        # Results frame
        results_frame = ttk.LabelFrame(self.problem1_frame, text="Results", padding=10)
        results_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.p1_result_text = tk.Text(results_frame, height=15, width=50, font=('Courier', 10))
        self.p1_result_text.pack(fill='both', expand=True)

        # Graph frame
        graph_frame = ttk.LabelFrame(self.problem1_frame, text="Cost Analysis", padding=10)
        graph_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky='nsew')

        self.p1_fig = Figure(figsize=(8, 8))
        self.p1_canvas = FigureCanvasTkAgg(self.p1_fig, master=graph_frame)
        self.p1_canvas.get_tk_widget().pack(fill='both', expand=True)

        # Configure grid weights
        self.problem1_frame.columnconfigure(1, weight=1)
        self.problem1_frame.rowconfigure(0, weight=1)

        # Initial calculation
        self.calculate_problem1()

    def init_problem2(self):
        """Initialize Problem 2: DC feeder system"""

        # Parameters frame
        params_frame = ttk.LabelFrame(self.problem2_frame, text="Parameters", padding=10)
        params_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Default values
        self.p2_current = tk.DoubleVar(value=120)  # A
        self.p2_voltage = tk.DoubleVar(value=250)  # V
        self.p2_energy_cost = tk.DoubleVar(value=0.10)  # Rs per kWh
        self.p2_cable_cost = tk.DoubleVar(value=20)  # Rs per metre per cm²
        self.p2_length = tk.DoubleVar(value=1)  # km
        self.p2_interest_rate = tk.DoubleVar(value=8)  # %
        self.p2_resistance_factor = tk.DoubleVar(value=0.15)  # ohm per km per cm²

        row = 0
        # Current slider
        self.create_slider(params_frame, "Current (A):", self.p2_current, 50, 300, row,
                          command=lambda v: self.calculate_problem2())
        row += 1

        # Voltage slider
        self.create_slider(params_frame, "Voltage (V):", self.p2_voltage, 100, 500, row,
                          command=lambda v: self.calculate_problem2())
        row += 1

        # Energy cost
        self.create_slider(params_frame, "Energy Cost (Rs/kWh):", self.p2_energy_cost, 0.05, 0.20, row,
                          command=lambda v: self.calculate_problem2(), resolution=0.01)
        row += 1

        # Cable cost
        self.create_slider(params_frame, "Cable Cost (Rs/m/cm²):", self.p2_cable_cost, 10, 50, row,
                          command=lambda v: self.calculate_problem2())
        row += 1

        # Length
        self.create_slider(params_frame, "Length (km):", self.p2_length, 0.5, 5, row,
                          command=lambda v: self.calculate_problem2(), resolution=0.1)
        row += 1

        # Interest rate
        self.create_slider(params_frame, "Interest Rate (%):", self.p2_interest_rate, 5, 15, row,
                          command=lambda v: self.calculate_problem2())
        row += 1

        # Resistance factor
        self.create_slider(params_frame, "Resistance (Ω/km/cm²):", self.p2_resistance_factor, 0.1, 0.3, row,
                          command=lambda v: self.calculate_problem2(), resolution=0.01)

        # Results frame
        results_frame = ttk.LabelFrame(self.problem2_frame, text="Results", padding=10)
        results_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.p2_result_text = tk.Text(results_frame, height=12, width=50, font=('Courier', 10))
        self.p2_result_text.pack(fill='both', expand=True)

        # Graph frame
        graph_frame = ttk.LabelFrame(self.problem2_frame, text="Cost Analysis", padding=10)
        graph_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky='nsew')

        self.p2_fig = Figure(figsize=(8, 8))
        self.p2_canvas = FigureCanvasTkAgg(self.p2_fig, master=graph_frame)
        self.p2_canvas.get_tk_widget().pack(fill='both', expand=True)

        # Configure grid weights
        self.problem2_frame.columnconfigure(1, weight=1)
        self.problem2_frame.rowconfigure(0, weight=1)

        # Initial calculation
        self.calculate_problem2()

    def create_slider(self, parent, label, variable, from_, to, row, command=None, resolution=1):
        """Create a labeled slider with value display"""
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky='w', padx=5, pady=5)

        slider = ttk.Scale(parent, from_=from_, to=to, variable=variable,
                          orient='horizontal', command=command)
        slider.grid(row=row, column=1, sticky='ew', padx=5, pady=5)

        value_label = ttk.Label(parent, text=f"{variable.get():.2f}")
        value_label.grid(row=row, column=2, sticky='w', padx=5, pady=5)

        # Update value label when slider moves
        def update_label(value):
            value_label.config(text=f"{float(value):.2f}")
            if command:
                command(value)

        slider.config(command=update_label)

        parent.columnconfigure(1, weight=1)

    def calculate_problem1(self):
        """Calculate economical cross-section for Problem 1"""

        # Get parameters
        V = self.p1_voltage.get() * 1000  # Convert to V
        P1 = self.p1_load1_mw.get() * 1e6  # Convert to W
        h1 = self.p1_load1_hours.get()
        P2 = self.p1_load2_mw.get() * 1e6
        h2 = self.p1_load2_hours.get()
        P3 = self.p1_load3_mw.get() * 1e6
        h3 = self.p1_load3_hours.get()
        pf = self.p1_pf.get()
        C1 = self.p1_fixed_cost.get()
        C2 = self.p1_variable_cost.get()
        r_percent = self.p1_interest_rate.get()
        energy_cost = self.p1_energy_cost.get()
        rho = self.p1_resistance_factor.get()

        # Calculate currents for each load (3-phase)
        I1 = P1 / (np.sqrt(3) * V * pf)
        I2 = P2 / (np.sqrt(3) * V * pf)
        I3 = P3 / (np.sqrt(3) * V * pf)

        # Calculate equivalent RMS current (considering daily cycle)
        # I_rms = sqrt((I1²*h1 + I2²*h2 + I3²*h3) / 24)
        I_rms = np.sqrt((I1**2 * h1 + I2**2 * h2 + I3**2 * h3) / 24)

        # Range of cross-sections to evaluate
        A_range = np.linspace(0.5, 5, 500)

        # Calculate costs for each cross-section
        capital_costs = []
        energy_costs = []
        total_costs = []

        for A in A_range:
            # Capital cost per km per year (with interest and depreciation)
            capital_cost_per_km = (C1 + C2 * A) * (r_percent / 100)

            # Resistance per phase per km
            R = rho / A

            # Power loss in 3-phase system (3 * I²R for all three phases)
            # Annual energy loss in kWh
            annual_loss = 3 * I_rms**2 * R * 24 * 365 / 1000  # kWh per km per year

            # Annual energy cost per km
            annual_energy_cost = annual_loss * energy_cost

            # Total annual cost per km
            total_cost = capital_cost_per_km + annual_energy_cost

            capital_costs.append(capital_cost_per_km)
            energy_costs.append(annual_energy_cost)
            total_costs.append(total_cost)

        # Find optimal cross-section
        optimal_idx = np.argmin(total_costs)
        optimal_A = A_range[optimal_idx]
        optimal_cost = total_costs[optimal_idx]
        optimal_capital = capital_costs[optimal_idx]
        optimal_energy = energy_costs[optimal_idx]

        # Calculate using Kelvin's Law formula
        # A_optimal = sqrt((P * ρ * C_e) / (C_c * r/100))
        # Where P = 3 * I_rms² (for annual calculation)
        # C_e = energy cost, C_c = variable cost coefficient, ρ = resistance factor

        P_factor = 3 * I_rms**2 * 24 * 365 / 1000  # Annual kWh loss factor per ohm
        A_kelvin = np.sqrt((P_factor * energy_cost) / (C2 * r_percent / 100))

        # Update results
        self.p1_result_text.delete(1.0, tk.END)
        result = f"""
PROBLEM 1: 3-PHASE TRANSMISSION LINE
=====================================

INPUT PARAMETERS:
-----------------
Voltage: {V/1000:.1f} kV
Power Factor: {pf}

Load Cycles:
  Load 1: {P1/1e6:.1f} MW for {h1:.0f} hours
  Load 2: {P2/1e6:.1f} MW for {h2:.0f} hours
  Load 3: {P3/1e6:.1f} MW for {h3:.0f} hours

Costs:
  Fixed: Rs. {C1:.0f}/km
  Variable: Rs. {C2:.0f}/km/cm²
  Interest Rate: {r_percent:.0f}%
  Energy Cost: Rs. {energy_cost:.2f}/kWh

CALCULATED VALUES:
------------------
Current (Load 1): {I1:.2f} A
Current (Load 2): {I2:.2f} A
Current (Load 3): {I3:.2f} A
RMS Current: {I_rms:.2f} A

OPTIMAL CROSS-SECTION:
---------------------
Numerical Optimization: {optimal_A:.3f} cm²
Kelvin's Law Formula:   {A_kelvin:.3f} cm²

ANNUAL COSTS (per km):
---------------------
Capital Cost:  Rs. {optimal_capital:.2f}
Energy Cost:   Rs. {optimal_energy:.2f}
Total Cost:    Rs. {optimal_cost:.2f}

Resistance:    {rho/optimal_A:.4f} Ω/km
Annual Loss:   {3 * I_rms**2 * (rho/optimal_A) * 24 * 365 / 1000:.2f} kWh/km
"""
        self.p1_result_text.insert(1.0, result)

        # Update graph
        self.p1_fig.clear()

        # Plot 1: Cost breakdown
        ax1 = self.p1_fig.add_subplot(2, 1, 1)
        ax1.plot(A_range, capital_costs, 'b-', label='Capital Cost', linewidth=2)
        ax1.plot(A_range, energy_costs, 'r-', label='Energy Cost', linewidth=2)
        ax1.plot(A_range, total_costs, 'g-', label='Total Cost', linewidth=2)
        ax1.axvline(optimal_A, color='black', linestyle='--', alpha=0.7,
                   label=f'Optimal: {optimal_A:.3f} cm²')
        ax1.set_xlabel('Cross-section (cm²)', fontsize=10)
        ax1.set_ylabel('Annual Cost (Rs/km)', fontsize=10)
        ax1.set_title('Annual Cost vs Cross-section', fontsize=12, fontweight='bold')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)

        # Plot 2: Zoomed view around optimum
        ax2 = self.p1_fig.add_subplot(2, 1, 2)
        zoom_range = (optimal_A - 1 < A_range) & (A_range < optimal_A + 1)
        ax2.plot(A_range[zoom_range], total_costs[zoom_range], 'g-', linewidth=2)
        ax2.axvline(optimal_A, color='black', linestyle='--', alpha=0.7)
        ax2.axhline(optimal_cost, color='red', linestyle='--', alpha=0.7)
        ax2.plot(optimal_A, optimal_cost, 'ro', markersize=10,
                label=f'Minimum: Rs. {optimal_cost:.2f}')
        ax2.set_xlabel('Cross-section (cm²)', fontsize=10)
        ax2.set_ylabel('Total Annual Cost (Rs/km)', fontsize=10)
        ax2.set_title('Zoomed View Around Optimal Point', fontsize=12, fontweight='bold')
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3)

        self.p1_fig.tight_layout()
        self.p1_canvas.draw()

    def calculate_problem2(self):
        """Calculate economical cross-section for Problem 2"""

        # Get parameters
        I = self.p2_current.get()  # A
        V = self.p2_voltage.get()  # V
        energy_cost = self.p2_energy_cost.get()  # Rs/kWh
        cable_cost = self.p2_cable_cost.get()  # Rs/m/cm²
        length_km = self.p2_length.get()  # km
        length_m = length_km * 1000  # m
        r_percent = self.p2_interest_rate.get()  # %
        rho = self.p2_resistance_factor.get()  # ohm/km/cm²

        # Range of cross-sections to evaluate
        A_range = np.linspace(0.5, 10, 500)

        # Calculate costs for each cross-section
        capital_costs = []
        energy_costs = []
        total_costs = []

        for A in A_range:
            # Capital cost for two-core cable (total length in meters)
            total_capital_cost = cable_cost * A * length_m

            # Annual capital charge (interest + depreciation)
            annual_capital_cost = total_capital_cost * (r_percent / 100)

            # Resistance per conductor
            R_per_conductor = rho * length_km / A

            # Total resistance (both cores in series for DC)
            R_total = 2 * R_per_conductor

            # Power loss
            P_loss = I**2 * R_total / 1000  # kW

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

        # Calculate using Kelvin's Law
        # For DC two-core: A = sqrt((2 * I² * ρ * L * C_e) / (C_c * r/100))
        # Where C_c = cable_cost per meter, C_e = energy cost
        # Annual energy loss factor = I² * 24 * 365 / 1000 kWh per ohm

        numerator = 2 * I**2 * rho * length_km * 24 * 365 * energy_cost / 1000
        denominator = cable_cost * length_m * (r_percent / 100)
        A_kelvin = np.sqrt(numerator / denominator)

        # Calculate voltage drop at optimal cross-section
        R_optimal = 2 * rho * length_km / optimal_A
        voltage_drop = I * R_optimal
        voltage_drop_percent = (voltage_drop / V) * 100

        # Update results
        self.p2_result_text.delete(1.0, tk.END)
        result = f"""
PROBLEM 2: DC FEEDER SYSTEM
============================

INPUT PARAMETERS:
-----------------
Current: {I:.1f} A
Voltage: {V:.0f} V
Length: {length_km:.1f} km ({length_m:.0f} m)
Cable Cost: Rs. {cable_cost:.0f}/m/cm²
Energy Cost: Rs. {energy_cost:.2f}/kWh
Interest Rate: {r_percent:.0f}%
Resistance: {rho:.3f} Ω/km/cm²

OPTIMAL CROSS-SECTION:
---------------------
Numerical Optimization: {optimal_A:.3f} cm²
Kelvin's Law Formula:   {A_kelvin:.3f} cm²

ANNUAL COSTS:
-------------
Capital Cost:  Rs. {optimal_capital:.2f}
Energy Cost:   Rs. {optimal_energy:.2f}
Total Cost:    Rs. {optimal_cost:.2f}

SYSTEM CHARACTERISTICS:
----------------------
Total Resistance:  {2 * rho * length_km / optimal_A:.4f} Ω
Power Loss:        {I**2 * 2 * rho * length_km / optimal_A / 1000:.3f} kW
Voltage Drop:      {voltage_drop:.2f} V ({voltage_drop_percent:.2f}%)
Annual Loss:       {I**2 * 2 * rho * length_km / optimal_A * 24 * 365 / 1000:.2f} kWh
Efficiency:        {(1 - voltage_drop/V)*100:.2f}%
"""
        self.p2_result_text.insert(1.0, result)

        # Update graph
        self.p2_fig.clear()

        # Plot 1: Cost breakdown
        ax1 = self.p2_fig.add_subplot(2, 1, 1)
        ax1.plot(A_range, capital_costs, 'b-', label='Capital Cost', linewidth=2)
        ax1.plot(A_range, energy_costs, 'r-', label='Energy Cost', linewidth=2)
        ax1.plot(A_range, total_costs, 'g-', label='Total Cost', linewidth=2)
        ax1.axvline(optimal_A, color='black', linestyle='--', alpha=0.7,
                   label=f'Optimal: {optimal_A:.3f} cm²')
        ax1.set_xlabel('Cross-section (cm²)', fontsize=10)
        ax1.set_ylabel('Annual Cost (Rs)', fontsize=10)
        ax1.set_title('Annual Cost vs Cross-section', fontsize=12, fontweight='bold')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)

        # Plot 2: Zoomed view around optimum
        ax2 = self.p2_fig.add_subplot(2, 1, 2)
        zoom_range = (optimal_A - 2 < A_range) & (A_range < optimal_A + 2)
        ax2.plot(A_range[zoom_range], total_costs[zoom_range], 'g-', linewidth=2)
        ax2.axvline(optimal_A, color='black', linestyle='--', alpha=0.7)
        ax2.axhline(optimal_cost, color='red', linestyle='--', alpha=0.7)
        ax2.plot(optimal_A, optimal_cost, 'ro', markersize=10,
                label=f'Minimum: Rs. {optimal_cost:.2f}')
        ax2.set_xlabel('Cross-section (cm²)', fontsize=10)
        ax2.set_ylabel('Total Annual Cost (Rs)', fontsize=10)
        ax2.set_title('Zoomed View Around Optimal Point', fontsize=12, fontweight='bold')
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3)

        self.p2_fig.tight_layout()
        self.p2_canvas.draw()

def main():
    root = tk.Tk()
    app = EconomicalConductorCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
