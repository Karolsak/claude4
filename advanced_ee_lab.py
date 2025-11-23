"""
Advanced Electrical Engineering Laboratory
==========================================
Comprehensive Python + Tkinter application for electrical engineering calculations,
simulations, and analysis including power factor correction and motor dynamics.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from scipy.integrate import solve_ivp
import math
from dataclasses import dataclass
from typing import Callable, List, Tuple, Optional


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class MotorParameters:
    """Motor parameters for simulation"""
    voltage: float = 3000.0  # V
    frequency: float = 50.0  # Hz
    poles: int = 4
    power_output: float = 223800.0  # W (223.8 kW)
    efficiency: float = 0.92
    power_factor_initial: float = 0.75
    power_factor_target: float = 0.9
    resistance: float = 0.5  # Ohm
    inductance: float = 0.05  # H
    inertia: float = 2.0  # kg.m^2
    friction: float = 0.01  # N.m.s


@dataclass
class SimulationState:
    """Simulation state management"""
    is_running: bool = False
    is_paused: bool = False
    time: float = 0.0
    results: Optional[np.ndarray] = None


# ============================================================================
# PROBLEM SOLVERS
# ============================================================================

class PowerFactorCorrectionSolver:
    """Solves power factor correction problems"""

    @staticmethod
    def solve_problem_10():
        """
        Problem 10: Capacitor bank calculation
        3-phase, 3000V, 50Hz motor, 223.8 kW output
        p.f. 0.75 -> 0.9 lagging, efficiency 92%
        Star-connected capacitors, 3 in series per phase
        """
        # Given data
        V_line = 3000  # V
        f = 50  # Hz
        P_output = 223800  # W
        efficiency = 0.92
        pf1 = 0.75  # Initial power factor
        pf2 = 0.9   # Final power factor
        capacitors_per_phase = 3

        # Calculate input power
        P_input = P_output / efficiency  # W

        # Calculate initial reactive power
        theta1 = math.acos(pf1)
        Q1 = P_input * math.tan(theta1)

        # Calculate final reactive power
        theta2 = math.acos(pf2)
        Q2 = P_input * math.tan(theta2)

        # Reactive power to be compensated
        Q_c = Q1 - Q2

        # Phase voltage (star connection)
        V_phase = V_line / math.sqrt(3)

        # Angular frequency
        omega = 2 * math.pi * f

        # Capacitive reactance per phase
        X_c = (V_phase ** 2) / Q_c * 3

        # Capacitance per phase (series combination)
        C_phase = 1 / (omega * X_c)

        # Each capacitor in series
        C_each = C_phase * capacitors_per_phase

        # Convert to microfarads
        C_each_uF = C_each * 1e6

        return {
            'P_input': P_input,
            'P_output': P_output,
            'Q1': Q1,
            'Q2': Q2,
            'Q_c': Q_c,
            'V_phase': V_phase,
            'X_c': X_c,
            'C_phase': C_phase,
            'C_each': C_each,
            'C_each_uF': C_each_uF,
            'theoretical_answer': 118  # µF from problem
        }

    @staticmethod
    def solve_problem_11():
        """
        Problem 11: Economic analysis of power factor correction
        Current p.f. 0.7 -> 0.9 lagging
        Additional plant cost: Rs. 800 per kVA
        """
        # Given data
        pf1 = 0.7  # Initial power factor
        pf2 = 0.9  # Target power factor
        cost_per_kVA_plant = 800  # Rs.

        # For a given real power P (let's assume 1 kW for calculation)
        P = 1  # kW (normalized)

        # Initial apparent power
        S1 = P / pf1

        # Final apparent power
        S2 = P / pf2

        # Reduction in kVA
        delta_S = S1 - S2

        # This reduction means we don't need additional plant capacity
        # Cost saving per kW of real power
        cost_saving = delta_S * cost_per_kVA_plant

        # Calculate reactive power compensation needed
        theta1 = math.acos(pf1)
        theta2 = math.acos(pf2)
        Q1 = P * math.tan(theta1)
        Q2 = P * math.tan(theta2)
        Q_c = Q1 - Q2  # kVAR to be compensated

        # Maximum cost per kVA of correction apparatus
        # Should be less than the cost of additional plant
        max_cost_per_kVA = (delta_S / Q_c) * cost_per_kVA_plant

        return {
            'pf1': pf1,
            'pf2': pf2,
            'S1': S1,
            'S2': S2,
            'delta_S': delta_S,
            'Q1': Q1,
            'Q2': Q2,
            'Q_c': Q_c,
            'cost_saving_per_kW': cost_saving,
            'max_cost_per_kVA': max_cost_per_kVA,
            'cost_per_kVA_plant': cost_per_kVA_plant
        }


# ============================================================================
# DYNAMIC SIMULATION ENGINE
# ============================================================================

class MotorDynamicsSimulator:
    """Real-time motor dynamics simulation with ODE solvers"""

    def __init__(self, params: MotorParameters):
        self.params = params
        self.solver_method = 'RK45'

    def motor_dynamics(self, t, y):
        """
        Differential equations for motor dynamics
        y = [omega, theta, i_d, i_q]
        omega: angular velocity (rad/s)
        theta: rotor angle (rad)
        i_d, i_q: d-q axis currents (A)
        """
        omega, theta, i_d, i_q = y

        # Synchronous speed
        omega_s = 2 * math.pi * self.params.frequency * 2 / self.params.poles

        # Electromagnetic torque
        T_e = 1.5 * self.params.poles * (i_d * i_q * 0.1)

        # Load torque (simplified)
        T_load = self.params.friction * omega

        # Mechanical equation
        d_omega = (T_e - T_load) / self.params.inertia

        # Rotor angle
        d_theta = omega

        # Electrical equations (simplified d-q model)
        V_d = self.params.voltage / math.sqrt(3) * math.cos(omega_s * t)
        V_q = self.params.voltage / math.sqrt(3) * math.sin(omega_s * t)

        d_i_d = (V_d - self.params.resistance * i_d + omega * self.params.inductance * i_q) / self.params.inductance
        d_i_q = (V_q - self.params.resistance * i_q - omega * self.params.inductance * i_d) / self.params.inductance

        return [d_omega, d_theta, d_i_d, d_i_q]

    def simulate_rk45(self, t_span, y0, t_eval=None):
        """Simulate using RK45 method"""
        sol = solve_ivp(self.motor_dynamics, t_span, y0, method='RK45',
                       t_eval=t_eval, rtol=1e-6, atol=1e-9)
        return sol

    def simulate_euler(self, t_span, y0, dt=0.001):
        """Simulate using Euler method"""
        t_start, t_end = t_span
        t_points = np.arange(t_start, t_end, dt)
        y_points = np.zeros((len(y0), len(t_points)))
        y_points[:, 0] = y0

        for i in range(1, len(t_points)):
            t = t_points[i-1]
            y = y_points[:, i-1]
            dy = np.array(self.motor_dynamics(t, y))
            y_points[:, i] = y + dy * dt

        return t_points, y_points

    def calculate_performance(self, omega, i_d, i_q):
        """Calculate motor performance metrics"""
        # Power
        P_elec = 3 * self.params.voltage / math.sqrt(3) * (i_d**2 + i_q**2)**0.5
        P_mech = self.params.inertia * omega**2 / 2

        # Torque
        T = 1.5 * self.params.poles * (i_d * i_q * 0.1)

        # Efficiency
        efficiency = P_mech / P_elec if P_elec > 0 else 0

        return {
            'power_electrical': P_elec,
            'power_mechanical': P_mech,
            'torque': T,
            'efficiency': efficiency,
            'speed_rpm': omega * 60 / (2 * math.pi)
        }


# ============================================================================
# VISUALIZATION ENGINE
# ============================================================================

class PlotManager:
    """Manages matplotlib plots with auto-scaling"""

    def __init__(self, figure: Figure):
        self.figure = figure
        self.axes = []
        self.auto_scale = True

    def create_subplots(self, rows, cols):
        """Create subplot grid"""
        self.figure.clear()
        self.axes = []
        for i in range(rows * cols):
            ax = self.figure.add_subplot(rows, cols, i + 1)
            self.axes.append(ax)
        return self.axes

    def plot_time_series(self, ax, t, y, label, xlabel='Time (s)', ylabel='Value'):
        """Plot time series data"""
        ax.clear()
        ax.plot(t, y, label=label, linewidth=2)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend()
        ax.grid(True, alpha=0.3)
        if self.auto_scale:
            ax.relim()
            ax.autoscale_view()

    def plot_phasor_diagram(self, ax, voltage, current, power_factor):
        """Plot phasor diagram for power factor analysis"""
        ax.clear()
        ax.set_aspect('equal')

        # Voltage phasor (reference)
        V_mag = abs(voltage)
        ax.arrow(0, 0, V_mag, 0, head_width=V_mag*0.05, head_length=V_mag*0.05,
                fc='blue', ec='blue', linewidth=2, label='Voltage')

        # Current phasor
        I_mag = abs(current)
        angle = -math.acos(power_factor)  # lagging
        I_x = I_mag * math.cos(angle)
        I_y = I_mag * math.sin(angle)
        ax.arrow(0, 0, I_x, I_y, head_width=I_mag*0.05, head_length=I_mag*0.05,
                fc='red', ec='red', linewidth=2, label=f'Current (pf={power_factor:.2f})')

        # Power triangle
        P = V_mag * I_mag * power_factor
        Q = V_mag * I_mag * math.sin(-angle)
        ax.plot([0, P, P], [0, 0, -Q], 'g--', linewidth=1.5, label='Power Triangle')

        ax.set_xlabel('Real Component')
        ax.set_ylabel('Imaginary Component')
        ax.legend()
        ax.grid(True, alpha=0.3)
        if self.auto_scale:
            ax.relim()
            ax.autoscale_view()


# ============================================================================
# MAIN APPLICATION GUI
# ============================================================================

class AdvancedEELaboratory(tk.Tk):
    """Main application window"""

    def __init__(self):
        super().__init__()

        self.title("Advanced Electrical Engineering Laboratory")
        self.geometry("1400x900")
        self.minsize(1000, 700)

        # State management
        self.simulation_state = SimulationState()
        self.motor_params = MotorParameters()
        self.simulator = MotorDynamicsSimulator(self.motor_params)

        # Configure grid weights for responsive design
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create main notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        # Create tabs
        self.create_main_menu_tab()
        self.create_problem_solver_tab()
        self.create_motor_simulation_tab()
        self.create_power_factor_analysis_tab()

        # Bind resize event
        self.bind('<Configure>', self.on_resize)

    def on_resize(self, event):
        """Handle window resize for auto-scaling"""
        if hasattr(self, 'canvas_sim'):
            self.canvas_sim.draw_idle()
        if hasattr(self, 'canvas_pf'):
            self.canvas_pf.draw_idle()

    # ========================================================================
    # TAB 1: MAIN MENU
    # ========================================================================

    def create_main_menu_tab(self):
        """Create main menu and overview tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Main Menu")

        # Configure grid
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        # Main frame
        main_frame = ttk.Frame(tab)
        main_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        # Title
        title = ttk.Label(main_frame, text="Advanced Electrical Engineering Laboratory",
                         font=('Arial', 24, 'bold'))
        title.pack(pady=20)

        subtitle = ttk.Label(main_frame,
                            text="Comprehensive tool for power system analysis, motor dynamics, and simulations",
                            font=('Arial', 12))
        subtitle.pack(pady=10)

        # Feature cards
        features_frame = ttk.Frame(main_frame)
        features_frame.pack(pady=20, fill='both', expand=True)

        features = [
            ("Problem Solver", "Solve complex power factor correction and economic analysis problems"),
            ("Motor Simulation", "Real-time dynamic simulation with RK45 and Euler ODE solvers"),
            ("Power Factor Analysis", "Comprehensive power factor correction analysis and visualization"),
            ("Advanced Features", "Interactive controls, auto-scaling plots, and parameter adjustment")
        ]

        for i, (title_text, desc) in enumerate(features):
            card = ttk.LabelFrame(features_frame, text=title_text, padding=15)
            card.pack(fill='x', pady=5)
            ttk.Label(card, text=desc, wraplength=600).pack()

        # Quick start buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Solve Problems 10 & 11",
                  command=lambda: self.notebook.select(1)).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Run Motor Simulation",
                  command=lambda: self.notebook.select(2)).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Power Factor Analysis",
                  command=lambda: self.notebook.select(3)).pack(side='left', padx=5)

    # ========================================================================
    # TAB 2: PROBLEM SOLVER
    # ========================================================================

    def create_problem_solver_tab(self):
        """Create problem solver tab for Problems 10 & 11"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Problem Solver")

        # Configure grid
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        # Main container
        container = ttk.Frame(tab)
        container.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Title
        title = ttk.Label(container, text="Power Factor Correction Problem Solver",
                         font=('Arial', 16, 'bold'))
        title.grid(row=0, column=0, pady=10, sticky='ew')

        # Notebook for problems
        problem_notebook = ttk.Notebook(container)
        problem_notebook.grid(row=1, column=0, sticky='nsew')

        # Problem 10
        self.create_problem_10_panel(problem_notebook)

        # Problem 11
        self.create_problem_11_panel(problem_notebook)

    def create_problem_10_panel(self, parent):
        """Create Problem 10 solver panel"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="Problem 10: Capacitor Bank")

        # Configure grid
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Problem statement
        statement_frame = ttk.LabelFrame(frame, text="Problem Statement", padding=10)
        statement_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

        statement = """A 3-phase, 3,000-V, 50-Hz motor develops 375 h.p. (223.8 kW), the p.f. being 0.75 lagging and
the efficiency 92%. A bank of capacitors is star-connected in parallel with the motor and the total
p.f. raised to 0.9 lagging. Each phase of the capacitor bank is made up of 3 capacitors joined in
series. Determine the capacitance of each. [Expected: 118 µF]"""

        ttk.Label(statement_frame, text=statement, wraplength=700, justify='left').pack()

        # Solution frame
        solution_frame = ttk.Frame(frame)
        solution_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        solution_frame.grid_rowconfigure(0, weight=1)
        solution_frame.grid_columnconfigure(0, weight=1)

        # Results text widget
        self.problem10_text = scrolledtext.ScrolledText(solution_frame, wrap=tk.WORD,
                                                        font=('Courier', 10))
        self.problem10_text.grid(row=0, column=0, sticky='nsew')

        # Solve button
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, pady=10)

        ttk.Button(button_frame, text="Solve Problem 10",
                  command=self.solve_problem_10).pack()

    def create_problem_11_panel(self, parent):
        """Create Problem 11 solver panel"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="Problem 11: Economic Analysis")

        # Configure grid
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Problem statement
        statement_frame = ttk.LabelFrame(frame, text="Problem Statement", padding=10)
        statement_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

        statement = """For increasing the kW capacity of a power plant working at 0.7 lagging power factor, the necessary
increase in power can be obtained by raising the power factor to 0.9 or by installing additional
plant. What is the maximum cost per kVA of power factor correction apparatus to make its use
more economical than additional plant at Rs. 800 per kVA?"""

        ttk.Label(statement_frame, text=statement, wraplength=700, justify='left').pack()

        # Solution frame
        solution_frame = ttk.Frame(frame)
        solution_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        solution_frame.grid_rowconfigure(0, weight=1)
        solution_frame.grid_columnconfigure(0, weight=1)

        # Results text widget
        self.problem11_text = scrolledtext.ScrolledText(solution_frame, wrap=tk.WORD,
                                                        font=('Courier', 10))
        self.problem11_text.grid(row=0, column=0, sticky='nsew')

        # Solve button
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, pady=10)

        ttk.Button(button_frame, text="Solve Problem 11",
                  command=self.solve_problem_11).pack()

    def solve_problem_10(self):
        """Solve and display Problem 10"""
        solver = PowerFactorCorrectionSolver()
        results = solver.solve_problem_10()

        output = "=" * 80 + "\n"
        output += "PROBLEM 10: CAPACITOR BANK CALCULATION\n"
        output += "=" * 80 + "\n\n"

        output += "Given Data:\n"
        output += "-" * 40 + "\n"
        output += f"Line Voltage: 3000 V\n"
        output += f"Frequency: 50 Hz\n"
        output += f"Power Output: 223.8 kW (375 hp)\n"
        output += f"Efficiency: 92%\n"
        output += f"Initial Power Factor: 0.75 lagging\n"
        output += f"Target Power Factor: 0.9 lagging\n"
        output += f"Capacitors per phase: 3 (series)\n"
        output += f"Connection: Star\n\n"

        output += "Calculations:\n"
        output += "-" * 40 + "\n"
        output += f"Input Power: {results['P_input']/1000:.2f} kW\n"
        output += f"Output Power: {results['P_output']/1000:.2f} kW\n"
        output += f"Initial Reactive Power (Q1): {results['Q1']/1000:.2f} kVAR\n"
        output += f"Final Reactive Power (Q2): {results['Q2']/1000:.2f} kVAR\n"
        output += f"Reactive Power to Compensate (Qc): {results['Q_c']/1000:.2f} kVAR\n"
        output += f"Phase Voltage: {results['V_phase']:.2f} V\n"
        output += f"Capacitive Reactance per Phase: {results['X_c']:.2f} Ω\n"
        output += f"Total Capacitance per Phase: {results['C_phase']*1e6:.2f} µF\n\n"

        output += "RESULT:\n"
        output += "=" * 80 + "\n"
        output += f"Capacitance of Each Capacitor: {results['C_each_uF']:.2f} µF\n"
        output += f"Expected Answer: {results['theoretical_answer']} µF\n"
        output += f"Difference: {abs(results['C_each_uF'] - results['theoretical_answer']):.2f} µF\n"
        output += "=" * 80 + "\n"

        self.problem10_text.delete(1.0, tk.END)
        self.problem10_text.insert(1.0, output)

    def solve_problem_11(self):
        """Solve and display Problem 11"""
        solver = PowerFactorCorrectionSolver()
        results = solver.solve_problem_11()

        output = "=" * 80 + "\n"
        output += "PROBLEM 11: ECONOMIC ANALYSIS OF POWER FACTOR CORRECTION\n"
        output += "=" * 80 + "\n\n"

        output += "Given Data:\n"
        output += "-" * 40 + "\n"
        output += f"Initial Power Factor: {results['pf1']}\n"
        output += f"Target Power Factor: {results['pf2']}\n"
        output += f"Cost of Additional Plant: Rs. {results['cost_per_kVA_plant']}/kVA\n\n"

        output += "Analysis (per kW of real power):\n"
        output += "-" * 40 + "\n"
        output += f"Initial Apparent Power: {results['S1']:.4f} kVA\n"
        output += f"Final Apparent Power: {results['S2']:.4f} kVA\n"
        output += f"Reduction in Apparent Power: {results['delta_S']:.4f} kVA\n\n"

        output += f"Initial Reactive Power (Q1): {results['Q1']:.4f} kVAR\n"
        output += f"Final Reactive Power (Q2): {results['Q2']:.4f} kVAR\n"
        output += f"Reactive Compensation Required: {results['Q_c']:.4f} kVAR\n\n"

        output += "Economic Analysis:\n"
        output += "-" * 40 + "\n"
        output += f"Cost Saving per kW: Rs. {results['cost_saving_per_kW']:.2f}\n"
        output += f"(Due to reduced plant capacity needed)\n\n"

        output += "RESULT:\n"
        output += "=" * 80 + "\n"
        output += f"Maximum Cost per kVA of Correction Apparatus: Rs. {results['max_cost_per_kVA']:.2f}\n"
        output += "\nInterpretation:\n"
        output += f"Power factor correction is economical if its cost is below Rs. {results['max_cost_per_kVA']:.2f} per kVA.\n"
        output += f"This is because improving p.f. from {results['pf1']} to {results['pf2']} saves\n"
        output += f"Rs. {results['cost_saving_per_kW']:.2f} per kW in plant capacity costs.\n"
        output += "=" * 80 + "\n"

        self.problem11_text.delete(1.0, tk.END)
        self.problem11_text.insert(1.0, output)

    # ========================================================================
    # TAB 3: MOTOR SIMULATION
    # ========================================================================

    def create_motor_simulation_tab(self):
        """Create motor dynamics simulation tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Motor Simulation")

        # Configure grid
        tab.grid_rowconfigure(0, weight=0)
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=3)

        # Title
        title = ttk.Label(tab, text="Real-Time Motor Dynamics Simulation",
                         font=('Arial', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')

        # Left panel: Controls
        control_frame = ttk.LabelFrame(tab, text="Simulation Controls", padding=10)
        control_frame.grid(row=1, column=0, sticky='nsew', padx=(10, 5), pady=10)

        # Motor parameters with sliders
        params_frame = ttk.LabelFrame(control_frame, text="Motor Parameters", padding=10)
        params_frame.pack(fill='both', expand=True, pady=5)

        self.param_vars = {}
        parameters = [
            ("Voltage (V)", "voltage", 1000, 5000, 3000),
            ("Frequency (Hz)", "frequency", 40, 60, 50),
            ("Power (kW)", "power_output", 100, 500, 223.8),
            ("Efficiency", "efficiency", 0.8, 0.98, 0.92),
            ("Resistance (Ω)", "resistance", 0.1, 2.0, 0.5),
            ("Inductance (H)", "inductance", 0.01, 0.1, 0.05),
            ("Inertia (kg·m²)", "inertia", 0.5, 5.0, 2.0),
            ("Friction (N·m·s)", "friction", 0.001, 0.1, 0.01)
        ]

        for i, (label, key, min_val, max_val, default) in enumerate(parameters):
            frame = ttk.Frame(params_frame)
            frame.pack(fill='x', pady=2)

            ttk.Label(frame, text=label, width=20).pack(side='left')

            var = tk.DoubleVar(value=default)
            self.param_vars[key] = var

            scale = ttk.Scale(frame, from_=min_val, to=max_val, variable=var,
                            orient='horizontal', command=lambda v, k=key: self.update_param(k, v))
            scale.pack(side='left', fill='x', expand=True, padx=5)

            value_label = ttk.Label(frame, text=f"{default:.2f}", width=8)
            value_label.pack(side='left')
            var.trace_add('write', lambda *args, lbl=value_label, v=var:
                         lbl.config(text=f"{v.get():.2f}"))

        # Solver selection
        solver_frame = ttk.LabelFrame(control_frame, text="ODE Solver", padding=10)
        solver_frame.pack(fill='x', pady=5)

        self.solver_var = tk.StringVar(value='RK45')
        ttk.Radiobutton(solver_frame, text="RK45 (Adaptive)", variable=self.solver_var,
                       value='RK45').pack(anchor='w')
        ttk.Radiobutton(solver_frame, text="Euler (Fixed Step)", variable=self.solver_var,
                       value='Euler').pack(anchor='w')

        # Simulation time
        time_frame = ttk.LabelFrame(control_frame, text="Simulation Time", padding=10)
        time_frame.pack(fill='x', pady=5)

        ttk.Label(time_frame, text="Duration (s):").pack(side='left')
        self.sim_time_var = tk.DoubleVar(value=2.0)
        ttk.Scale(time_frame, from_=0.5, to=10.0, variable=self.sim_time_var,
                 orient='horizontal').pack(side='left', fill='x', expand=True, padx=5)
        time_label = ttk.Label(time_frame, text="2.0", width=8)
        time_label.pack(side='left')
        self.sim_time_var.trace_add('write', lambda *args:
                                   time_label.config(text=f"{self.sim_time_var.get():.1f}"))

        # Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill='x', pady=10)

        self.start_btn = ttk.Button(button_frame, text="Start",
                                    command=self.start_simulation)
        self.start_btn.pack(side='left', padx=2, fill='x', expand=True)

        self.stop_btn = ttk.Button(button_frame, text="Stop",
                                   command=self.stop_simulation, state='disabled')
        self.stop_btn.pack(side='left', padx=2, fill='x', expand=True)

        self.reset_btn = ttk.Button(button_frame, text="Reset",
                                    command=self.reset_simulation)
        self.reset_btn.pack(side='left', padx=2, fill='x', expand=True)

        # Status
        self.status_label = ttk.Label(control_frame, text="Ready",
                                     font=('Arial', 10, 'bold'))
        self.status_label.pack(pady=5)

        # Right panel: Plots
        plot_frame = ttk.Frame(tab)
        plot_frame.grid(row=1, column=1, sticky='nsew', padx=(5, 10), pady=10)
        plot_frame.grid_rowconfigure(0, weight=1)
        plot_frame.grid_columnconfigure(0, weight=1)

        # Create matplotlib figure
        self.fig_sim = Figure(figsize=(10, 8), dpi=100)
        self.plot_manager_sim = PlotManager(self.fig_sim)

        self.canvas_sim = FigureCanvasTkAgg(self.fig_sim, master=plot_frame)
        self.canvas_sim.draw()
        self.canvas_sim.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        # Toolbar
        toolbar_frame = ttk.Frame(plot_frame)
        toolbar_frame.grid(row=1, column=0, sticky='ew')
        toolbar = NavigationToolbar2Tk(self.canvas_sim, toolbar_frame)
        toolbar.update()

    def update_param(self, key, value):
        """Update motor parameters from sliders"""
        value = float(value)
        if key == "power_output":
            value *= 1000  # Convert kW to W
        setattr(self.motor_params, key, value)
        self.simulator = MotorDynamicsSimulator(self.motor_params)

    def start_simulation(self):
        """Start motor simulation"""
        self.simulation_state.is_running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.status_label.config(text="Simulating...")

        # Initial conditions
        omega_s = 2 * math.pi * self.motor_params.frequency * 2 / self.motor_params.poles
        y0 = [omega_s * 0.95, 0, 10, 10]  # Start near synchronous speed

        t_span = (0, self.sim_time_var.get())

        try:
            if self.solver_var.get() == 'RK45':
                t_eval = np.linspace(0, self.sim_time_var.get(), 500)
                sol = self.simulator.simulate_rk45(t_span, y0, t_eval)
                t = sol.t
                y = sol.y
            else:  # Euler
                t, y = self.simulator.simulate_euler(t_span, y0, dt=0.001)

            # Plot results
            axes = self.plot_manager_sim.create_subplots(2, 2)

            # Angular velocity
            self.plot_manager_sim.plot_time_series(
                axes[0], t, y[0, :] * 60 / (2 * math.pi),
                'Angular Velocity', 'Time (s)', 'Speed (RPM)'
            )

            # Rotor angle
            self.plot_manager_sim.plot_time_series(
                axes[1], t, np.rad2deg(y[1, :]),
                'Rotor Angle', 'Time (s)', 'Angle (degrees)'
            )

            # d-axis current
            self.plot_manager_sim.plot_time_series(
                axes[2], t, y[2, :],
                'd-axis Current', 'Time (s)', 'Current (A)'
            )

            # q-axis current
            self.plot_manager_sim.plot_time_series(
                axes[3], t, y[3, :],
                'q-axis Current', 'Time (s)', 'Current (A)'
            )

            self.fig_sim.tight_layout()
            self.canvas_sim.draw()

            self.status_label.config(text="Simulation Complete")

        except Exception as e:
            messagebox.showerror("Simulation Error", f"Error during simulation: {str(e)}")
            self.status_label.config(text="Error")

        finally:
            self.simulation_state.is_running = False
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')

    def stop_simulation(self):
        """Stop simulation"""
        self.simulation_state.is_running = False
        self.status_label.config(text="Stopped")
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')

    def reset_simulation(self):
        """Reset simulation"""
        self.simulation_state.is_running = False
        self.simulation_state.time = 0.0
        self.plot_manager_sim.figure.clear()
        self.canvas_sim.draw()
        self.status_label.config(text="Reset")
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')

    # ========================================================================
    # TAB 4: POWER FACTOR ANALYSIS
    # ========================================================================

    def create_power_factor_analysis_tab(self):
        """Create power factor analysis and visualization tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Power Factor Analysis")

        # Configure grid
        tab.grid_rowconfigure(0, weight=0)
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=2)

        # Title
        title = ttk.Label(tab, text="Power Factor Correction Analysis",
                         font=('Arial', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')

        # Left panel: Parameters
        param_frame = ttk.LabelFrame(tab, text="System Parameters", padding=10)
        param_frame.grid(row=1, column=0, sticky='nsew', padx=(10, 5), pady=10)

        # Input parameters
        inputs_frame = ttk.LabelFrame(param_frame, text="Input Parameters", padding=10)
        inputs_frame.pack(fill='both', expand=True, pady=5)

        self.pf_vars = {}
        pf_parameters = [
            ("Active Power (kW)", "power", 100, 1000, 400),
            ("Voltage (V)", "voltage", 1000, 11000, 3000),
            ("Initial PF", "pf_initial", 0.5, 0.95, 0.75),
            ("Target PF", "pf_target", 0.85, 1.0, 0.9),
            ("Frequency (Hz)", "frequency", 50, 60, 50)
        ]

        for label, key, min_val, max_val, default in pf_parameters:
            frame = ttk.Frame(inputs_frame)
            frame.pack(fill='x', pady=2)

            ttk.Label(frame, text=label, width=20).pack(side='left')

            var = tk.DoubleVar(value=default)
            self.pf_vars[key] = var

            scale = ttk.Scale(frame, from_=min_val, to=max_val, variable=var,
                            orient='horizontal')
            scale.pack(side='left', fill='x', expand=True, padx=5)

            value_label = ttk.Label(frame, text=f"{default:.2f}", width=8)
            value_label.pack(side='left')
            var.trace_add('write', lambda *args, lbl=value_label, v=var:
                         lbl.config(text=f"{v.get():.2f}"))

        # Results display
        results_frame = ttk.LabelFrame(param_frame, text="Calculated Results", padding=10)
        results_frame.pack(fill='both', expand=True, pady=5)

        self.pf_results_text = tk.Text(results_frame, height=15, wrap=tk.WORD,
                                       font=('Courier', 9))
        self.pf_results_text.pack(fill='both', expand=True)

        # Calculate button
        calc_btn = ttk.Button(param_frame, text="Calculate & Visualize",
                             command=self.calculate_power_factor)
        calc_btn.pack(pady=10, fill='x')

        # Right panel: Visualization
        viz_frame = ttk.Frame(tab)
        viz_frame.grid(row=1, column=1, sticky='nsew', padx=(5, 10), pady=10)
        viz_frame.grid_rowconfigure(0, weight=1)
        viz_frame.grid_columnconfigure(0, weight=1)

        # Create matplotlib figure
        self.fig_pf = Figure(figsize=(10, 8), dpi=100)
        self.plot_manager_pf = PlotManager(self.fig_pf)

        self.canvas_pf = FigureCanvasTkAgg(self.fig_pf, master=viz_frame)
        self.canvas_pf.draw()
        self.canvas_pf.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        # Toolbar
        toolbar_frame = ttk.Frame(viz_frame)
        toolbar_frame.grid(row=1, column=0, sticky='ew')
        toolbar = NavigationToolbar2Tk(self.canvas_pf, toolbar_frame)
        toolbar.update()

    def calculate_power_factor(self):
        """Calculate and visualize power factor correction"""
        # Get parameters
        P = self.pf_vars['power'].get() * 1000  # Convert to W
        V = self.pf_vars['voltage'].get()
        pf1 = self.pf_vars['pf_initial'].get()
        pf2 = self.pf_vars['pf_target'].get()
        f = self.pf_vars['frequency'].get()

        # Calculations
        theta1 = math.acos(pf1)
        theta2 = math.acos(pf2)

        Q1 = P * math.tan(theta1)
        Q2 = P * math.tan(theta2)
        Q_c = Q1 - Q2

        S1 = P / pf1
        S2 = P / pf2

        I1 = S1 / (math.sqrt(3) * V)
        I2 = S2 / (math.sqrt(3) * V)

        # Capacitance calculation
        omega = 2 * math.pi * f
        V_phase = V / math.sqrt(3)
        X_c = (V_phase ** 2) / (Q_c / 3)
        C = 1 / (omega * X_c)

        # Display results
        results = f"""Power Factor Correction Analysis
{'='*50}

System Parameters:
  Active Power (P): {P/1000:.2f} kW
  Voltage (V): {V:.0f} V
  Frequency: {f:.0f} Hz

Initial Conditions:
  Power Factor: {pf1:.3f} lagging
  Reactive Power (Q1): {Q1/1000:.2f} kVAR
  Apparent Power (S1): {S1/1000:.2f} kVA
  Current (I1): {I1:.2f} A

Target Conditions:
  Power Factor: {pf2:.3f} lagging
  Reactive Power (Q2): {Q2/1000:.2f} kVAR
  Apparent Power (S2): {S2/1000:.2f} kVA
  Current (I2): {I2:.2f} A

Capacitor Bank Requirements:
  Reactive Compensation: {Q_c/1000:.2f} kVAR
  Capacitive Reactance: {X_c:.2f} Ω/phase
  Capacitance Required: {C*1e6:.2f} µF/phase

Improvements:
  Reduction in Apparent Power: {(S1-S2)/1000:.2f} kVA
  Reduction in Current: {I1-I2:.2f} A
  Percentage Improvement: {((S1-S2)/S1*100):.1f}%
"""

        self.pf_results_text.delete(1.0, tk.END)
        self.pf_results_text.insert(1.0, results)

        # Visualize
        axes = self.plot_manager_pf.create_subplots(2, 2)

        # Phasor diagram - Initial
        ax = axes[0]
        ax.clear()
        ax.set_aspect('equal')
        ax.set_title('Initial Phasor Diagram')

        # Voltage (reference)
        ax.arrow(0, 0, 1, 0, head_width=0.05, head_length=0.05,
                fc='blue', ec='blue', linewidth=2, label='Voltage')

        # Current
        I_norm = I1 / I1
        angle1 = -theta1
        I_x = I_norm * math.cos(angle1)
        I_y = I_norm * math.sin(angle1)
        ax.arrow(0, 0, I_x, I_y, head_width=0.05, head_length=0.05,
                fc='red', ec='red', linewidth=2, label=f'Current (PF={pf1:.2f})')

        # Power components
        P_norm = pf1
        Q_norm = math.sin(angle1) * I_norm
        ax.plot([0, P_norm], [0, 0], 'g-', linewidth=2, label='Active Power')
        ax.plot([P_norm, I_x], [0, I_y], 'orange', linewidth=2, label='Reactive Power')

        ax.set_xlabel('Real')
        ax.set_ylabel('Imaginary')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-0.2, 1.2)
        ax.set_ylim(-1.0, 0.2)

        # Phasor diagram - Corrected
        ax = axes[1]
        ax.clear()
        ax.set_aspect('equal')
        ax.set_title('Corrected Phasor Diagram')

        # Voltage (reference)
        ax.arrow(0, 0, 1, 0, head_width=0.05, head_length=0.05,
                fc='blue', ec='blue', linewidth=2, label='Voltage')

        # Current
        I_norm2 = I2 / I1
        angle2 = -theta2
        I_x2 = I_norm2 * math.cos(angle2)
        I_y2 = I_norm2 * math.sin(angle2)
        ax.arrow(0, 0, I_x2, I_y2, head_width=0.05, head_length=0.05,
                fc='red', ec='red', linewidth=2, label=f'Current (PF={pf2:.2f})')

        # Power components
        P_norm2 = pf2 * I_norm2
        Q_norm2 = math.sin(angle2) * I_norm2
        ax.plot([0, P_norm2], [0, 0], 'g-', linewidth=2, label='Active Power')
        ax.plot([P_norm2, I_x2], [0, I_y2], 'orange', linewidth=2, label='Reactive Power')

        ax.set_xlabel('Real')
        ax.set_ylabel('Imaginary')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-0.2, 1.2)
        ax.set_ylim(-1.0, 0.2)

        # Power triangle comparison
        ax = axes[2]
        ax.clear()
        ax.set_title('Power Triangle Comparison')

        # Initial
        ax.plot([0, P/1000, P/1000, 0], [0, 0, -Q1/1000, 0], 'r-',
               linewidth=2, label='Initial', marker='o')

        # Corrected
        ax.plot([0, P/1000, P/1000, 0], [0, 0, -Q2/1000, 0], 'g-',
               linewidth=2, label='Corrected', marker='o')

        # Compensating reactive power
        ax.arrow(P/1000, -Q1/1000, 0, Q_c/1000*0.9, head_width=P/1000*0.05,
                head_length=Q_c/1000*0.05, fc='blue', ec='blue', linewidth=2,
                label='Capacitor VAR')

        ax.set_xlabel('Active Power (kW)')
        ax.set_ylabel('Reactive Power (kVAR)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5)

        # Current and power factor vs load
        ax = axes[3]
        ax.clear()
        ax.set_title('Current Reduction vs Power Factor')

        pf_range = np.linspace(0.5, 1.0, 100)
        S_range = P / (pf_range * 1000)
        I_range = S_range / (math.sqrt(3) * V) * 1000

        ax.plot(pf_range, I_range, 'b-', linewidth=2)
        ax.axvline(x=pf1, color='r', linestyle='--', label=f'Initial PF={pf1:.2f}')
        ax.axvline(x=pf2, color='g', linestyle='--', label=f'Target PF={pf2:.2f}')
        ax.axhline(y=I1, color='r', linestyle=':', alpha=0.5)
        ax.axhline(y=I2, color='g', linestyle=':', alpha=0.5)

        ax.set_xlabel('Power Factor')
        ax.set_ylabel('Line Current (A)')
        ax.legend()
        ax.grid(True, alpha=0.3)

        self.fig_pf.tight_layout()
        self.canvas_pf.draw()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    app = AdvancedEELaboratory()
    app.mainloop()


if __name__ == "__main__":
    main()
