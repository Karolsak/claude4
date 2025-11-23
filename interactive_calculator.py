"""
Interactive Economical Conductor Calculator with Matplotlib Sliders
For environments without Tkinter support
"""

import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Try TkAgg backend for interactivity
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.gridspec import GridSpec

class InteractiveConductorCalculator:
    def __init__(self):
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.suptitle('Economical Conductor Cross-Section Calculator - Kelvin\'s Law',
                         fontsize=14, fontweight='bold')

        # Create grid layout
        gs = GridSpec(3, 3, figure=self.fig, hspace=0.4, wspace=0.3,
                     left=0.05, right=0.95, top=0.93, bottom=0.05)

        # Problem selector
        self.ax_radio = self.fig.add_subplot(gs[0, 0])
        self.radio = RadioButtons(self.ax_radio, ('Problem 1: 3-Phase', 'Problem 2: DC Feeder'))
        self.radio.on_clicked(self.update_problem)

        # Main plot area
        self.ax_main = self.fig.add_subplot(gs[0:2, 1:])
        self.ax_result = self.fig.add_subplot(gs[2, :])
        self.ax_result.axis('off')

        # Slider axes - Problem 1
        self.slider_axes_p1 = {}
        slider_positions = [(gs[1, 0], 'load1_mw', 'Load 1 (MW)', 1, 50, 20),
                          (gs[2, 0], 'load1_hrs', 'Load 1 Hours', 0, 24, 6)]

        # Initialize sliders dictionary
        self.sliders = {}

        # Problem 1 default parameters
        self.p1_params = {
            'voltage_kv': 110,
            'load1_mw': 20, 'load1_hrs': 6,
            'load2_mw': 5, 'load2_hrs': 12,
            'load3_mw': 6, 'load3_hrs': 10,
            'pf': 0.8,
            'fixed_cost': 9000,
            'var_cost': 600,
            'interest': 10,
            'energy_cost': 0.06,
            'resistance': 0.176
        }

        # Problem 2 default parameters
        self.p2_params = {
            'current': 120,
            'voltage': 250,
            'length_km': 1,
            'cable_cost': 20,
            'interest': 8,
            'energy_cost': 0.10,
            'resistance': 0.15
        }

        self.current_problem = 'Problem 1: 3-Phase'
        self.create_sliders_p1()
        self.calculate()

        plt.show()

    def create_sliders_p1(self):
        """Create sliders for Problem 1"""
        # Clear existing sliders
        for ax in self.slider_axes_p1.values():
            ax.clear()

        # Define slider parameters
        slider_defs = [
            ('voltage_kv', 'Voltage (kV)', 50, 220, 110, 5),
            ('load1_mw', 'Load 1 (MW)', 1, 50, 20, 1),
            ('load1_hrs', 'Load 1 Hours', 0, 24, 6, 1),
            ('load2_mw', 'Load 2 (MW)', 1, 50, 5, 1),
            ('load2_hrs', 'Load 2 Hours', 0, 24, 12, 1),
            ('load3_mw', 'Load 3 (MW)', 1, 50, 6, 1),
            ('load3_hrs', 'Load 3 Hours', 0, 24, 10, 1),
            ('pf', 'Power Factor', 0.5, 1.0, 0.8, 0.05),
            ('energy_cost', 'Energy Cost (Rs/kWh)', 0.02, 0.15, 0.06, 0.01),
        ]

        # Create sliders in a column
        num_sliders = len(slider_defs)
        slider_height = 0.03
        slider_spacing = 0.04
        start_y = 0.85

        for i, (key, label, vmin, vmax, vinit, step) in enumerate(slider_defs):
            ax = plt.axes([0.15, start_y - i * slider_spacing, 0.3, slider_height])
            slider = Slider(ax, label, vmin, vmax, valinit=vinit, valstep=step)
            slider.on_changed(lambda val, k=key: self.update_param(k, val))
            self.sliders[key] = slider
            self.slider_axes_p1[key] = ax

    def update_param(self, key, val):
        """Update parameter and recalculate"""
        if self.current_problem == 'Problem 1: 3-Phase':
            self.p1_params[key] = val
        else:
            self.p2_params[key] = val
        self.calculate()

    def update_problem(self, label):
        """Switch between problems"""
        self.current_problem = label
        self.calculate()

    def calculate(self):
        """Calculate and update display"""
        if self.current_problem == 'Problem 1: 3-Phase':
            self.calculate_problem1()
        else:
            self.calculate_problem2()

    def calculate_problem1(self):
        """Calculate Problem 1"""
        p = self.p1_params

        # Calculate currents
        V = p['voltage_kv'] * 1000
        loads_mw = [p['load1_mw'], p['load2_mw'], p['load3_mw']]
        hours = [p['load1_hrs'], p['load2_hrs'], p['load3_hrs']]
        pf = p['pf']

        P = [mw * 1e6 for mw in loads_mw]
        currents = [power / (np.sqrt(3) * V * pf) for power in P]
        I_rms = np.sqrt(sum(I**2 * h for I, h in zip(currents, hours)) / 24)

        # Calculate costs
        A_range = np.linspace(0.5, 20, 1000)
        total_costs = []

        for A in A_range:
            capital = (p['fixed_cost'] + p['var_cost'] * A) * (p['interest'] / 100)
            energy_loss = 3 * I_rms**2 * (p['resistance']/A) * 8760 / 1000
            energy_cost = energy_loss * p['energy_cost']
            total = capital + energy_cost
            total_costs.append(total)

        total_costs = np.array(total_costs)
        opt_idx = np.argmin(total_costs)
        opt_A = A_range[opt_idx]
        opt_cost = total_costs[opt_idx]

        # Update plot
        self.ax_main.clear()
        self.ax_main.plot(A_range, total_costs, 'g-', linewidth=2.5, label='Total Cost')
        self.ax_main.axvline(opt_A, color='r', linestyle='--', linewidth=2,
                           label=f'Optimal: {opt_A:.3f} cm²')
        self.ax_main.axvline(1.64, color='orange', linestyle=':', linewidth=2,
                           label='Expected: 1.64 cm²')
        self.ax_main.set_xlabel('Cross-section (cm²)', fontsize=12)
        self.ax_main.set_ylabel('Total Annual Cost (Rs/km)', fontsize=12)
        self.ax_main.set_title('Problem 1: 3-Phase Transmission Line', fontsize=13, fontweight='bold')
        self.ax_main.legend(fontsize=10)
        self.ax_main.grid(True, alpha=0.3)
        self.ax_main.set_xlim(0, 10)

        # Update results text
        self.ax_result.clear()
        self.ax_result.axis('off')
        result_text = f"""
PROBLEM 1 RESULTS:
═══════════════════════════════════════════════════════════════════════════════
RMS Current: {I_rms:.2f} A  |  Optimal Cross-section: {opt_A:.3f} cm²  |  Min Annual Cost: Rs. {opt_cost:.2f}/km
Currents: Load1={currents[0]:.1f}A, Load2={currents[1]:.1f}A, Load3={currents[2]:.1f}A
        """
        self.ax_result.text(0.05, 0.5, result_text, fontsize=10, family='monospace',
                          verticalalignment='center')

        self.fig.canvas.draw_idle()

    def calculate_problem2(self):
        """Calculate Problem 2"""
        p = self.p2_params

        # Calculate costs
        A_range = np.linspace(0.5, 10, 1000)
        total_costs = []

        for A in A_range:
            capital = p['cable_cost'] * A * p['length_km'] * 1000 * (p['interest'] / 100)
            R_total = 2 * p['resistance'] * p['length_km'] / A
            P_loss = p['current']**2 * R_total / 1000
            energy_loss = P_loss * 8760
            energy_cost = energy_loss * p['energy_cost']
            total = capital + energy_cost
            total_costs.append(total)

        total_costs = np.array(total_costs)
        opt_idx = np.argmin(total_costs)
        opt_A = A_range[opt_idx]
        opt_cost = total_costs[opt_idx]

        # System characteristics
        R_opt = 2 * p['resistance'] * p['length_km'] / opt_A
        V_drop = p['current'] * R_opt
        V_drop_pct = (V_drop / p['voltage']) * 100

        # Update plot
        self.ax_main.clear()
        self.ax_main.plot(A_range, total_costs, 'g-', linewidth=2.5, label='Total Cost')
        self.ax_main.axvline(opt_A, color='r', linestyle='--', linewidth=2,
                           label=f'Optimal: {opt_A:.3f} cm²')
        self.ax_main.set_xlabel('Cross-section (cm²)', fontsize=12)
        self.ax_main.set_ylabel('Total Annual Cost (Rs)', fontsize=12)
        self.ax_main.set_title('Problem 2: DC Feeder System', fontsize=13, fontweight='bold')
        self.ax_main.legend(fontsize=10)
        self.ax_main.grid(True, alpha=0.3)

        # Update results text
        self.ax_result.clear()
        self.ax_result.axis('off')
        result_text = f"""
PROBLEM 2 RESULTS:
═══════════════════════════════════════════════════════════════════════════════
Optimal Cross-section: {opt_A:.3f} cm²  |  Min Annual Cost: Rs. {opt_cost:.2f}
Voltage Drop: {V_drop:.2f}V ({V_drop_pct:.2f}%)  |  Resistance: {R_opt:.4f}Ω
        """
        self.ax_result.text(0.05, 0.5, result_text, fontsize=10, family='monospace',
                          verticalalignment='center')

        self.fig.canvas.draw_idle()


if __name__ == "__main__":
    print("Starting Interactive Calculator...")
    print("Use sliders to adjust parameters and see real-time updates!")
    print("Note: If GUI doesn't appear, use economical_conductor_solver.py instead")
    try:
        app = InteractiveConductorCalculator()
    except Exception as e:
        print(f"Error: {e}")
        print("GUI not available in this environment.")
        print("Please use: python economical_conductor_solver.py")
