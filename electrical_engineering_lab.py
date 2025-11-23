"""
Comprehensive Electrical Engineering Laboratory
Power Factor Correction, Dynamic Machine Simulation, and Advanced Analysis
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math


class ElectricalEngineeringLab:
    """Main application class for electrical engineering simulations"""

    def __init__(self, root):
        self.root = root
        self.root.title("Electrical Engineering Laboratory - Advanced Simulation Suite")
        self.root.geometry("1400x900")

        # Configure root grid weight for auto-resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Main notebook for different modules
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        # Create tabs
        self.create_problem_50_61_tab()
        self.create_problem_50_62_tab()
        self.create_dynamic_simulation_tab()

        # Bind resize event
        self.root.bind('<Configure>', self.on_window_resize)

    def on_window_resize(self, event):
        """Handle window resize events"""
        # This will be called when window is resized
        pass

    # ==================== PROBLEM 50.61 TAB ====================
    def create_problem_50_61_tab(self):
        """Create tab for Problem 50.61 - Capacitor Power Factor Correction"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Problem 50.61: Capacitor PF Correction")

        # Configure grid weights
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=2)

        # Left panel - inputs
        left_frame = ttk.LabelFrame(tab, text="Input Parameters", padding=10)
        left_frame.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=5, pady=5)

        # Input variables for Problem 50.61
        self.p61_voltage = tk.DoubleVar(value=3000)
        self.p61_frequency = tk.DoubleVar(value=50)
        self.p61_power_kw = tk.DoubleVar(value=447.6)
        self.p61_pf_initial = tk.DoubleVar(value=0.75)
        self.p61_pf_final = tk.DoubleVar(value=0.95)
        self.p61_efficiency = tk.DoubleVar(value=0.93)
        self.p61_capacitor_voltage = tk.DoubleVar(value=600)
        self.p61_num_capacitors = tk.IntVar(value=5)

        # Create input fields with sliders
        row = 0
        self.create_slider_input(left_frame, "Voltage (V):", self.p61_voltage, 1000, 10000, row)
        row += 1
        self.create_slider_input(left_frame, "Frequency (Hz):", self.p61_frequency, 25, 100, row)
        row += 1
        self.create_slider_input(left_frame, "Power Output (kW):", self.p61_power_kw, 100, 1000, row)
        row += 1
        self.create_slider_input(left_frame, "Initial PF:", self.p61_pf_initial, 0.5, 0.99, row, resolution=0.01)
        row += 1
        self.create_slider_input(left_frame, "Final PF:", self.p61_pf_final, 0.5, 1.0, row, resolution=0.01)
        row += 1
        self.create_slider_input(left_frame, "Efficiency:", self.p61_efficiency, 0.7, 0.99, row, resolution=0.01)
        row += 1
        self.create_slider_input(left_frame, "Capacitor Voltage (V):", self.p61_capacitor_voltage, 200, 1000, row)
        row += 1
        self.create_slider_input(left_frame, "Num Capacitors/Unit:", self.p61_num_capacitors, 1, 10, row, resolution=1)
        row += 1

        # Calculate button
        calc_btn = ttk.Button(left_frame, text="Calculate", command=self.calculate_problem_50_61)
        calc_btn.grid(row=row, column=0, columnspan=3, pady=20, sticky='ew')

        # Right panel - results and visualization
        right_frame = ttk.Frame(tab)
        right_frame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=5, pady=5)
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # Results text
        results_frame = ttk.LabelFrame(right_frame, text="Results", padding=10)
        results_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        self.p61_results = tk.Text(results_frame, height=8, wrap=tk.WORD)
        self.p61_results.pack(fill=tk.BOTH, expand=True)

        # Visualization
        viz_frame = ttk.LabelFrame(right_frame, text="Power Triangle Visualization", padding=5)
        viz_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        viz_frame.grid_rowconfigure(0, weight=1)
        viz_frame.grid_columnconfigure(0, weight=1)

        self.p61_fig = Figure(figsize=(8, 6))
        self.p61_canvas = FigureCanvasTkAgg(self.p61_fig, viz_frame)
        self.p61_canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

    def calculate_problem_50_61(self):
        """Calculate capacitor requirements for power factor correction"""
        try:
            # Get input values
            V_line = self.p61_voltage.get()
            f = self.p61_frequency.get()
            P_out = self.p61_power_kw.get() * 1000  # Convert to W
            pf1 = self.p61_pf_initial.get()
            pf2 = self.p61_pf_final.get()
            eta = self.p61_efficiency.get()
            V_cap = self.p61_capacitor_voltage.get()
            n_cap = self.p61_num_capacitors.get()

            # Calculate input power
            P_in = P_out / eta

            # Calculate angles
            phi1 = math.acos(pf1)
            phi2 = math.acos(pf2)

            # Calculate reactive power before and after
            Q1 = P_in * math.tan(phi1)
            Q2 = P_in * math.tan(phi2)

            # Reactive power to be compensated
            Q_c = Q1 - Q2

            # For delta connection, line voltage = phase voltage
            V_phase = V_line

            # Capacitive reactance per phase (delta)
            # Q_c = 3 * V_phase^2 / X_c
            X_c = 3 * V_phase**2 / Q_c

            # Capacitance per phase
            omega = 2 * math.pi * f
            C_phase = 1 / (omega * X_c)

            # Each capacitor unit consists of n capacitors
            # If capacitors are in series: C_total = C_individual / n
            # Voltage rating: n * V_cap should be >= V_phase
            C_individual = C_phase * n_cap

            # Apparent power
            S1 = P_in / pf1
            S2 = P_in / pf2

            # Display results
            results = f"""
PROBLEM 50.61 - CAPACITOR POWER FACTOR CORRECTION
{'='*60}

Input Power: {P_in/1000:.2f} kW
Output Power: {P_out/1000:.2f} kW
Efficiency: {eta*100:.1f}%

Initial Power Factor: {pf1:.3f} (angle: {math.degrees(phi1):.2f}°)
Final Power Factor: {pf2:.3f} (angle: {math.degrees(phi2):.2f}°)

Initial Reactive Power (Q1): {Q1/1000:.2f} kVAR
Final Reactive Power (Q2): {Q2/1000:.2f} kVAR
Reactive Power Compensated (Qc): {Q_c/1000:.2f} kVAR

Initial Apparent Power: {S1/1000:.2f} kVA
Final Apparent Power: {S2/1000:.2f} kVA

Capacitive Reactance/Phase: {X_c:.2f} Ω
Capacitance/Phase (Delta): {C_phase*1e6:.2f} µF
Capacitance/Capacitor: {C_individual*1e6:.2f} µF

Configuration: {n_cap} capacitors in series per phase
Voltage/Capacitor: {V_cap} V
Total Voltage Rating: {n_cap * V_cap} V (Phase Voltage: {V_phase:.0f} V)
"""

            self.p61_results.delete(1.0, tk.END)
            self.p61_results.insert(1.0, results)

            # Visualize power triangle
            self.visualize_power_triangle_50_61(P_in, Q1, Q2, S1, S2, pf1, pf2)

        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")

    def visualize_power_triangle_50_61(self, P, Q1, Q2, S1, S2, pf1, pf2):
        """Visualize power triangles before and after compensation"""
        self.p61_fig.clear()
        ax = self.p61_fig.add_subplot(111)

        # Convert to kW/kVAR/kVA
        P_k = P / 1000
        Q1_k = Q1 / 1000
        Q2_k = Q2 / 1000
        S1_k = S1 / 1000
        S2_k = S2 / 1000
        Q_c = (Q1 - Q2) / 1000

        # Draw initial power triangle (before compensation)
        ax.arrow(0, 0, P_k, 0, head_width=5, head_length=5, fc='blue', ec='blue',
                 linewidth=2, label=f'P = {P_k:.1f} kW')
        ax.arrow(P_k, 0, 0, Q1_k, head_width=5, head_length=5, fc='red', ec='red',
                 linewidth=2, label=f'Q1 = {Q1_k:.1f} kVAR (initial)')
        ax.plot([0, P_k], [0, Q1_k], 'b--', linewidth=2,
                label=f'S1 = {S1_k:.1f} kVA (PF={pf1:.3f})')

        # Draw final power triangle (after compensation)
        ax.arrow(P_k, Q1_k, 0, -Q_c, head_width=5, head_length=5, fc='green', ec='green',
                 linewidth=2, label=f'Qc = {Q_c:.1f} kVAR (capacitor)')
        ax.arrow(P_k, 0, 0, Q2_k, head_width=5, head_length=3, fc='orange', ec='orange',
                 linewidth=2, linestyle='--', label=f'Q2 = {Q2_k:.1f} kVAR (final)')
        ax.plot([0, P_k], [0, Q2_k], 'g-', linewidth=3,
                label=f'S2 = {S2_k:.1f} kVA (PF={pf2:.3f})')

        ax.set_xlabel('Active Power P (kW)', fontsize=10, fontweight='bold')
        ax.set_ylabel('Reactive Power Q (kVAR)', fontsize=10, fontweight='bold')
        ax.set_title('Power Triangle - Power Factor Correction', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right', fontsize=8)
        ax.axis('equal')

        # Add angle annotations
        angle1 = math.degrees(math.atan2(Q1_k, P_k))
        angle2 = math.degrees(math.atan2(Q2_k, P_k))
        ax.annotate(f'φ1={angle1:.1f}°', xy=(P_k/2, Q1_k/2), fontsize=9, color='blue')
        ax.annotate(f'φ2={angle2:.1f}°', xy=(P_k/2, Q2_k/2), fontsize=9, color='green')

        self.p61_fig.tight_layout()
        self.p61_canvas.draw()

    # ==================== PROBLEM 50.62 TAB ====================
    def create_problem_50_62_tab(self):
        """Create tab for Problem 50.62 - Synchronous Motor Compensation"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Problem 50.62: Synchronous Motor")

        # Configure grid weights
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=2)

        # Left panel - inputs
        left_frame = ttk.LabelFrame(tab, text="Input Parameters", padding=10)
        left_frame.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=5, pady=5)

        # Input variables for Problem 50.62
        self.p62_motor_power = tk.DoubleVar(value=50)
        self.p62_load_power = tk.DoubleVar(value=200)
        self.p62_load_pf = tk.DoubleVar(value=0.8)
        self.p62_combined_pf = tk.DoubleVar(value=0.9)

        # Create input fields with sliders
        row = 0
        self.create_slider_input(left_frame, "Sync Motor Power (kW):", self.p62_motor_power, 10, 200, row)
        row += 1
        self.create_slider_input(left_frame, "Load Power (kW):", self.p62_load_power, 50, 500, row)
        row += 1
        self.create_slider_input(left_frame, "Load Power Factor:", self.p62_load_pf, 0.5, 0.99, row, resolution=0.01)
        row += 1
        self.create_slider_input(left_frame, "Combined Power Factor:", self.p62_combined_pf, 0.5, 1.0, row, resolution=0.01)
        row += 1

        # Calculate button
        calc_btn = ttk.Button(left_frame, text="Calculate", command=self.calculate_problem_50_62)
        calc_btn.grid(row=row, column=0, columnspan=3, pady=20, sticky='ew')

        # Right panel - results and visualization
        right_frame = ttk.Frame(tab)
        right_frame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=5, pady=5)
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # Results text
        results_frame = ttk.LabelFrame(right_frame, text="Results", padding=10)
        results_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        self.p62_results = tk.Text(results_frame, height=10, wrap=tk.WORD)
        self.p62_results.pack(fill=tk.BOTH, expand=True)

        # Visualization
        viz_frame = ttk.LabelFrame(right_frame, text="Power Analysis Visualization", padding=5)
        viz_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        viz_frame.grid_rowconfigure(0, weight=1)
        viz_frame.grid_columnconfigure(0, weight=1)

        self.p62_fig = Figure(figsize=(8, 6))
        self.p62_canvas = FigureCanvasTkAgg(self.p62_fig, viz_frame)
        self.p62_canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

    def calculate_problem_50_62(self):
        """Calculate synchronous motor reactive power compensation"""
        try:
            # Get input values
            P_motor = self.p62_motor_power.get()
            P_load = self.p62_load_power.get()
            pf_load = self.p62_load_pf.get()
            pf_combined = self.p62_combined_pf.get()

            # Total active power
            P_total = P_motor + P_load

            # Load reactive power (lagging)
            phi_load = math.acos(pf_load)
            Q_load = P_load * math.tan(phi_load)

            # Combined reactive power (lagging)
            phi_combined = math.acos(pf_combined)
            Q_combined = P_total * math.tan(phi_combined)

            # Motor reactive power (negative means leading)
            Q_motor = Q_combined - Q_load

            # Motor apparent power
            S_motor = math.sqrt(P_motor**2 + Q_motor**2)

            # Motor power factor
            pf_motor = P_motor / S_motor

            # Determine if leading or lagging
            if Q_motor < 0:
                pf_type = "leading"
                Q_motor_abs = abs(Q_motor)
            else:
                pf_type = "lagging"
                Q_motor_abs = Q_motor

            # Load apparent power
            S_load = P_load / pf_load

            # Combined apparent power
            S_combined = P_total / pf_combined

            # Display results
            results = f"""
PROBLEM 50.62 - SYNCHRONOUS MOTOR COMPENSATION
{'='*60}

LOAD ANALYSIS:
  Active Power: {P_load:.2f} kW
  Power Factor: {pf_load:.3f} lagging
  Reactive Power: {Q_load:.2f} kVAR (lagging)
  Apparent Power: {S_load:.2f} kVA

SYNCHRONOUS MOTOR:
  Active Power: {P_motor:.2f} kW
  Reactive Power: {Q_motor_abs:.2f} kVAR ({pf_type})
  Apparent Power: {S_motor:.2f} kVA
  Power Factor: {pf_motor:.4f} {pf_type}

COMBINED SYSTEM:
  Total Active Power: {P_total:.2f} kW
  Total Reactive Power: {Q_combined:.2f} kVAR (lagging)
  Total Apparent Power: {S_combined:.2f} kVA
  Combined Power Factor: {pf_combined:.3f} lagging

The synchronous motor supplies {Q_motor_abs:.2f} kVAR of leading
reactive power to improve the overall power factor from
{pf_load:.3f} to {pf_combined:.3f}.
"""

            self.p62_results.delete(1.0, tk.END)
            self.p62_results.insert(1.0, results)

            # Visualize power analysis
            self.visualize_power_analysis_50_62(P_load, Q_load, P_motor, Q_motor,
                                                P_total, Q_combined, pf_load, pf_combined)

        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")

    def visualize_power_analysis_50_62(self, P_load, Q_load, P_motor, Q_motor,
                                       P_total, Q_combined, pf_load, pf_combined):
        """Visualize power analysis for synchronous motor compensation"""
        self.p62_fig.clear()

        # Create two subplots
        ax1 = self.p62_fig.add_subplot(121)
        ax2 = self.p62_fig.add_subplot(122)

        # Plot 1: Phasor diagram
        ax1.arrow(0, 0, P_load, 0, head_width=3, head_length=5, fc='blue', ec='blue',
                  linewidth=2, label=f'Load P={P_load:.0f}kW')
        ax1.arrow(P_load, 0, 0, Q_load, head_width=3, head_length=5, fc='red', ec='red',
                  linewidth=2, label=f'Load Q={Q_load:.0f}kVAR')

        ax1.arrow(P_load, Q_load, P_motor, 0, head_width=3, head_length=5, fc='green', ec='green',
                  linewidth=2, label=f'Motor P={P_motor:.0f}kW')
        ax1.arrow(P_load+P_motor, Q_load, 0, Q_motor, head_width=3, head_length=5,
                  fc='purple', ec='purple', linewidth=2,
                  label=f'Motor Q={abs(Q_motor):.0f}kVAR ({"leading" if Q_motor < 0 else "lagging"})')

        # Combined power
        ax1.plot([0, P_total], [0, Q_combined], 'k-', linewidth=3,
                 label=f'Combined (PF={pf_combined:.3f})')

        ax1.set_xlabel('Active Power (kW)', fontweight='bold')
        ax1.set_ylabel('Reactive Power (kVAR)', fontweight='bold')
        ax1.set_title('Power Phasor Diagram', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=8, loc='best')
        ax1.axhline(y=0, color='k', linewidth=0.5)
        ax1.axvline(x=0, color='k', linewidth=0.5)

        # Plot 2: Bar chart comparison
        categories = ['Active\nPower', 'Reactive\nPower', 'Apparent\nPower']
        load_values = [P_load, Q_load, P_load/pf_load]
        motor_values = [P_motor, abs(Q_motor), math.sqrt(P_motor**2 + Q_motor**2)]
        combined_values = [P_total, Q_combined, P_total/pf_combined]

        x = np.arange(len(categories))
        width = 0.25

        ax2.bar(x - width, load_values, width, label='Load', color='blue', alpha=0.7)
        ax2.bar(x, motor_values, width, label='Motor', color='green', alpha=0.7)
        ax2.bar(x + width, combined_values, width, label='Combined', color='red', alpha=0.7)

        ax2.set_ylabel('Power (kW/kVAR/kVA)', fontweight='bold')
        ax2.set_title('Power Comparison', fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(categories)
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')

        # Add value labels on bars
        for i, (l, m, c) in enumerate(zip(load_values, motor_values, combined_values)):
            ax2.text(i - width, l + 2, f'{l:.0f}', ha='center', fontsize=8)
            ax2.text(i, m + 2, f'{m:.0f}', ha='center', fontsize=8)
            ax2.text(i + width, c + 2, f'{c:.0f}', ha='center', fontsize=8)

        self.p62_fig.tight_layout()
        self.p62_canvas.draw()

    # ==================== DYNAMIC SIMULATION TAB ====================
    def create_dynamic_simulation_tab(self):
        """Create tab for dynamic electrical machine simulation"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Dynamic Machine Simulation")

        # Configure grid weights
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=2)

        # Left panel - controls
        left_frame = ttk.LabelFrame(tab, text="Simulation Controls", padding=10)
        left_frame.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=5, pady=5)

        # Machine type selection
        ttk.Label(left_frame, text="Machine Type:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.machine_type = tk.StringVar(value="Induction Motor")
        machine_combo = ttk.Combobox(left_frame, textvariable=self.machine_type,
                                     values=["Induction Motor", "Synchronous Generator", "DC Motor"],
                                     state='readonly')
        machine_combo.grid(row=0, column=1, columnspan=2, sticky='ew', pady=5)

        # ODE Solver selection
        ttk.Label(left_frame, text="ODE Solver:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        self.ode_solver = tk.StringVar(value="RK45")
        solver_combo = ttk.Combobox(left_frame, textvariable=self.ode_solver,
                                    values=["RK45", "Euler"], state='readonly')
        solver_combo.grid(row=1, column=1, columnspan=2, sticky='ew', pady=5)

        # Simulation parameters
        self.sim_time = tk.DoubleVar(value=5.0)
        self.sim_steps = tk.IntVar(value=1000)
        self.voltage_input = tk.DoubleVar(value=400)
        self.frequency = tk.DoubleVar(value=50)
        self.load_torque = tk.DoubleVar(value=100)
        self.inertia = tk.DoubleVar(value=0.5)
        self.resistance = tk.DoubleVar(value=1.0)
        self.inductance = tk.DoubleVar(value=0.1)

        row = 2
        self.create_slider_input(left_frame, "Simulation Time (s):", self.sim_time, 0.1, 10, row, resolution=0.1)
        row += 1
        self.create_slider_input(left_frame, "Voltage (V):", self.voltage_input, 100, 1000, row)
        row += 1
        self.create_slider_input(left_frame, "Frequency (Hz):", self.frequency, 25, 100, row)
        row += 1
        self.create_slider_input(left_frame, "Load Torque (Nm):", self.load_torque, 0, 500, row)
        row += 1
        self.create_slider_input(left_frame, "Inertia (kg⋅m²):", self.inertia, 0.1, 5, row, resolution=0.1)
        row += 1
        self.create_slider_input(left_frame, "Resistance (Ω):", self.resistance, 0.1, 10, row, resolution=0.1)
        row += 1
        self.create_slider_input(left_frame, "Inductance (H):", self.inductance, 0.01, 1, row, resolution=0.01)
        row += 1

        # Control buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=row, column=0, columnspan=3, pady=20, sticky='ew')

        self.start_btn = ttk.Button(btn_frame, text="Start", command=self.start_simulation)
        self.start_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self.stop_simulation, state='disabled')
        self.stop_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        self.reset_btn = ttk.Button(btn_frame, text="Reset", command=self.reset_simulation)
        self.reset_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # Right panel - visualization
        right_frame = ttk.Frame(tab)
        right_frame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=5, pady=5)
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        viz_frame = ttk.LabelFrame(right_frame, text="Dynamic Response", padding=5)
        viz_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        viz_frame.grid_rowconfigure(0, weight=1)
        viz_frame.grid_columnconfigure(0, weight=1)

        self.sim_fig = Figure(figsize=(10, 8))
        self.sim_canvas = FigureCanvasTkAgg(self.sim_fig, viz_frame)
        self.sim_canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        # Simulation state
        self.simulation_running = False
        self.simulation_data = None

    def start_simulation(self):
        """Start dynamic simulation"""
        self.simulation_running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')

        # Run simulation based on machine type
        machine = self.machine_type.get()
        solver = self.ode_solver.get()

        if machine == "Induction Motor":
            self.simulate_induction_motor(solver)
        elif machine == "Synchronous Generator":
            self.simulate_synchronous_generator(solver)
        elif machine == "DC Motor":
            self.simulate_dc_motor(solver)

        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.simulation_running = False

    def stop_simulation(self):
        """Stop simulation"""
        self.simulation_running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')

    def reset_simulation(self):
        """Reset simulation"""
        self.simulation_running = False
        self.simulation_data = None
        self.sim_fig.clear()
        self.sim_canvas.draw()

    def simulate_induction_motor(self, solver):
        """Simulate induction motor dynamics"""
        # Get parameters
        V = self.voltage_input.get()
        f = self.frequency.get()
        T_load = self.load_torque.get()
        J = self.inertia.get()
        R = self.resistance.get()
        L = self.inductance.get()
        t_max = self.sim_time.get()

        # Synchronous speed
        omega_sync = 2 * math.pi * f

        # Define differential equation: dω/dt = (T_motor - T_load) / J
        # Simplified model: T_motor = K * (omega_sync - omega)
        K_motor = 2.0  # Motor constant

        def motor_dynamics(t, state):
            omega = state[0]
            current = state[1]

            # Motor torque (simplified slip-dependent model)
            slip = (omega_sync - omega) / omega_sync
            T_motor = K_motor * omega_sync * slip if slip > 0 else 0

            # Current dynamics (RL circuit)
            V_eff = V * math.sqrt(2/3)  # Effective voltage
            di_dt = (V_eff - R * current) / L

            # Speed dynamics
            domega_dt = (T_motor - T_load) / J

            return [domega_dt, di_dt]

        # Initial conditions: [omega, current]
        y0 = [0.0, 0.0]

        # Solve ODE
        if solver == "RK45":
            t, y = self.solve_ode_rk45(motor_dynamics, y0, 0, t_max, 1000)
        else:  # Euler
            t, y = self.solve_ode_euler(motor_dynamics, y0, 0, t_max, 1000)

        omega = y[:, 0]
        current = y[:, 1]

        # Calculate other quantities
        speed_rpm = omega * 60 / (2 * math.pi)
        sync_speed_rpm = omega_sync * 60 / (2 * math.pi)
        slip = (omega_sync - omega) / omega_sync * 100
        torque = K_motor * omega_sync * (omega_sync - omega) / omega_sync

        # Visualize results
        self.visualize_motor_dynamics(t, speed_rpm, current, torque, slip, sync_speed_rpm)

    def simulate_synchronous_generator(self, solver):
        """Simulate synchronous generator dynamics"""
        V = self.voltage_input.get()
        f = self.frequency.get()
        P_load = self.load_torque.get() * 100  # Convert to watts
        J = self.inertia.get()
        t_max = self.sim_time.get()

        # Synchronous speed
        omega_sync = 2 * math.pi * f

        def generator_dynamics(t, state):
            delta = state[0]  # Load angle
            omega = state[1]   # Speed

            # Electrical torque (simplified)
            T_elec = (P_load / omega) if omega > 0.1 else 0
            T_mech = self.load_torque.get()  # Mechanical torque from prime mover

            # Dynamics
            ddelta_dt = omega - omega_sync
            domega_dt = (T_mech - T_elec) / J

            return [ddelta_dt, domega_dt]

        # Initial conditions: [delta, omega]
        y0 = [0.0, omega_sync]

        # Solve ODE
        if solver == "RK45":
            t, y = self.solve_ode_rk45(generator_dynamics, y0, 0, t_max, 1000)
        else:
            t, y = self.solve_ode_euler(generator_dynamics, y0, 0, t_max, 1000)

        delta = y[:, 0]
        omega = y[:, 1]

        # Calculate power and frequency
        speed_rpm = omega * 60 / (2 * math.pi)
        power = P_load * np.ones_like(t)
        frequency = omega / (2 * math.pi)

        # Visualize
        self.visualize_generator_dynamics(t, speed_rpm, delta, power, frequency)

    def simulate_dc_motor(self, solver):
        """Simulate DC motor dynamics"""
        V = self.voltage_input.get()
        T_load = self.load_torque.get()
        J = self.inertia.get()
        R = self.resistance.get()
        L = self.inductance.get()
        t_max = self.sim_time.get()

        # Motor constants
        K_motor = 1.0  # Torque constant
        K_back_emf = 1.0  # Back EMF constant

        def dc_motor_dynamics(t, state):
            omega = state[0]
            current = state[1]

            # Back EMF
            E = K_back_emf * omega

            # Current dynamics
            di_dt = (V - E - R * current) / L

            # Torque
            T_motor = K_motor * current

            # Speed dynamics
            domega_dt = (T_motor - T_load) / J

            return [domega_dt, di_dt]

        # Initial conditions
        y0 = [0.0, 0.0]

        # Solve ODE
        if solver == "RK45":
            t, y = self.solve_ode_rk45(dc_motor_dynamics, y0, 0, t_max, 1000)
        else:
            t, y = self.solve_ode_euler(dc_motor_dynamics, y0, 0, t_max, 1000)

        omega = y[:, 0]
        current = y[:, 1]

        # Calculate other quantities
        speed_rpm = omega * 60 / (2 * math.pi)
        torque = K_motor * current
        power = torque * omega

        # Visualize
        self.visualize_dc_motor_dynamics(t, speed_rpm, current, torque, power)

    def solve_ode_rk45(self, f, y0, t0, tf, n_points):
        """Solve ODE using RK45 method"""
        t = np.linspace(t0, tf, n_points)
        y = np.zeros((n_points, len(y0)))
        y[0] = y0

        for i in range(n_points - 1):
            h = t[i+1] - t[i]
            k1 = np.array(f(t[i], y[i]))
            k2 = np.array(f(t[i] + h/2, y[i] + h*k1/2))
            k3 = np.array(f(t[i] + h/2, y[i] + h*k2/2))
            k4 = np.array(f(t[i] + h, y[i] + h*k3))
            y[i+1] = y[i] + h * (k1 + 2*k2 + 2*k3 + k4) / 6

        return t, y

    def solve_ode_euler(self, f, y0, t0, tf, n_points):
        """Solve ODE using Euler method"""
        t = np.linspace(t0, tf, n_points)
        y = np.zeros((n_points, len(y0)))
        y[0] = y0

        for i in range(n_points - 1):
            h = t[i+1] - t[i]
            y[i+1] = y[i] + h * np.array(f(t[i], y[i]))

        return t, y

    def visualize_motor_dynamics(self, t, speed, current, torque, slip, sync_speed):
        """Visualize induction motor dynamics"""
        self.sim_fig.clear()

        # Create 4 subplots
        ax1 = self.sim_fig.add_subplot(221)
        ax2 = self.sim_fig.add_subplot(222)
        ax3 = self.sim_fig.add_subplot(223)
        ax4 = self.sim_fig.add_subplot(224)

        # Speed vs time
        ax1.plot(t, speed, 'b-', linewidth=2, label='Rotor Speed')
        ax1.axhline(y=sync_speed, color='r', linestyle='--', label='Sync Speed')
        ax1.set_xlabel('Time (s)', fontweight='bold')
        ax1.set_ylabel('Speed (RPM)', fontweight='bold')
        ax1.set_title('Speed Response', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Current vs time
        ax2.plot(t, current, 'g-', linewidth=2)
        ax2.set_xlabel('Time (s)', fontweight='bold')
        ax2.set_ylabel('Current (A)', fontweight='bold')
        ax2.set_title('Current Response', fontweight='bold')
        ax2.grid(True, alpha=0.3)

        # Torque vs time
        ax3.plot(t, torque, 'r-', linewidth=2)
        ax3.set_xlabel('Time (s)', fontweight='bold')
        ax3.set_ylabel('Torque (Nm)', fontweight='bold')
        ax3.set_title('Torque Response', fontweight='bold')
        ax3.grid(True, alpha=0.3)

        # Slip vs time
        ax4.plot(t, slip, 'm-', linewidth=2)
        ax4.set_xlabel('Time (s)', fontweight='bold')
        ax4.set_ylabel('Slip (%)', fontweight='bold')
        ax4.set_title('Slip Response', fontweight='bold')
        ax4.grid(True, alpha=0.3)

        self.sim_fig.suptitle(f'Induction Motor Dynamic Simulation ({self.ode_solver.get()} Method)',
                              fontsize=14, fontweight='bold')
        self.sim_fig.tight_layout()
        self.sim_canvas.draw()

    def visualize_generator_dynamics(self, t, speed, delta, power, frequency):
        """Visualize synchronous generator dynamics"""
        self.sim_fig.clear()

        ax1 = self.sim_fig.add_subplot(221)
        ax2 = self.sim_fig.add_subplot(222)
        ax3 = self.sim_fig.add_subplot(223)
        ax4 = self.sim_fig.add_subplot(224)

        # Speed
        ax1.plot(t, speed, 'b-', linewidth=2)
        ax1.set_xlabel('Time (s)', fontweight='bold')
        ax1.set_ylabel('Speed (RPM)', fontweight='bold')
        ax1.set_title('Speed Response', fontweight='bold')
        ax1.grid(True, alpha=0.3)

        # Load angle
        ax2.plot(t, np.degrees(delta), 'g-', linewidth=2)
        ax2.set_xlabel('Time (s)', fontweight='bold')
        ax2.set_ylabel('Load Angle (deg)', fontweight='bold')
        ax2.set_title('Load Angle', fontweight='bold')
        ax2.grid(True, alpha=0.3)

        # Power
        ax3.plot(t, power/1000, 'r-', linewidth=2)
        ax3.set_xlabel('Time (s)', fontweight='bold')
        ax3.set_ylabel('Power (kW)', fontweight='bold')
        ax3.set_title('Output Power', fontweight='bold')
        ax3.grid(True, alpha=0.3)

        # Frequency
        ax4.plot(t, frequency, 'm-', linewidth=2)
        ax4.set_xlabel('Time (s)', fontweight='bold')
        ax4.set_ylabel('Frequency (Hz)', fontweight='bold')
        ax4.set_title('Frequency', fontweight='bold')
        ax4.grid(True, alpha=0.3)

        self.sim_fig.suptitle(f'Synchronous Generator Dynamic Simulation ({self.ode_solver.get()} Method)',
                              fontsize=14, fontweight='bold')
        self.sim_fig.tight_layout()
        self.sim_canvas.draw()

    def visualize_dc_motor_dynamics(self, t, speed, current, torque, power):
        """Visualize DC motor dynamics"""
        self.sim_fig.clear()

        ax1 = self.sim_fig.add_subplot(221)
        ax2 = self.sim_fig.add_subplot(222)
        ax3 = self.sim_fig.add_subplot(223)
        ax4 = self.sim_fig.add_subplot(224)

        # Speed
        ax1.plot(t, speed, 'b-', linewidth=2)
        ax1.set_xlabel('Time (s)', fontweight='bold')
        ax1.set_ylabel('Speed (RPM)', fontweight='bold')
        ax1.set_title('Speed Response', fontweight='bold')
        ax1.grid(True, alpha=0.3)

        # Current
        ax2.plot(t, current, 'g-', linewidth=2)
        ax2.set_xlabel('Time (s)', fontweight='bold')
        ax2.set_ylabel('Current (A)', fontweight='bold')
        ax2.set_title('Armature Current', fontweight='bold')
        ax2.grid(True, alpha=0.3)

        # Torque
        ax3.plot(t, torque, 'r-', linewidth=2)
        ax3.set_xlabel('Time (s)', fontweight='bold')
        ax3.set_ylabel('Torque (Nm)', fontweight='bold')
        ax3.set_title('Motor Torque', fontweight='bold')
        ax3.grid(True, alpha=0.3)

        # Power
        ax4.plot(t, power, 'm-', linewidth=2)
        ax4.set_xlabel('Time (s)', fontweight='bold')
        ax4.set_ylabel('Power (W)', fontweight='bold')
        ax4.set_title('Output Power', fontweight='bold')
        ax4.grid(True, alpha=0.3)

        self.sim_fig.suptitle(f'DC Motor Dynamic Simulation ({self.ode_solver.get()} Method)',
                              fontsize=14, fontweight='bold')
        self.sim_fig.tight_layout()
        self.sim_canvas.draw()

    # ==================== HELPER METHODS ====================
    def create_slider_input(self, parent, label, variable, min_val, max_val, row, resolution=1):
        """Create a labeled input field with slider"""
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky='w', pady=2)

        entry = ttk.Entry(parent, textvariable=variable, width=10)
        entry.grid(row=row, column=1, padx=5, pady=2)

        slider = ttk.Scale(parent, from_=min_val, to=max_val, variable=variable,
                          orient=tk.HORIZONTAL, length=200)
        slider.grid(row=row, column=2, sticky='ew', pady=2)

        # Configure column weights for slider expansion
        parent.grid_columnconfigure(2, weight=1)


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = ElectricalEngineeringLab(root)
    root.mainloop()


if __name__ == "__main__":
    main()
