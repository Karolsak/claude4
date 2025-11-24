"""
Advanced Salient Pole Alternator Analysis and Simulation Laboratory
Comprehensive Python + Tkinter Application for Electrical Engineering

Features:
- Complete alternator parameter calculations
- Dynamic simulation with multiple ODE solvers (RK45, Euler)
- Interactive GUI with real-time controls
- Multiple visualization modes (Phasor diagrams, Time plots, 3D surfaces)
- Automatic scaling and responsive design
- Practical electrical engineering applications
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.integrate import solve_ivp
import math
from dataclasses import dataclass
from typing import Tuple, List
import threading
import time


@dataclass
class AlternatorParameters:
    """Data class for alternator parameters"""
    kva_rating: float = 25.0  # kVA
    voltage_rating: float = 440.0  # V (line voltage)
    frequency: float = 50.0  # Hz
    ra: float = 0.3  # Armature resistance (Ω)
    xd: float = 5.0  # Direct axis reactance (Ω)
    xq: float = 3.0  # Quadrature axis reactance (Ω)
    power_factor: float = 0.8  # Lagging
    connection: str = "star"
    poles: int = 4
    inertia: float = 0.5  # kg.m^2
    damping: float = 0.1  # N.m.s


class AlternatorCalculator:
    """Core calculation engine for alternator analysis"""

    def __init__(self, params: AlternatorParameters):
        self.params = params
        self.results = {}

    def calculate_steady_state(self) -> dict:
        """Calculate steady-state parameters using two-reaction theory"""
        p = self.params

        # Basic calculations
        v_phase = p.voltage_rating / np.sqrt(3) if p.connection == "star" else p.voltage_rating
        i_rated = (p.kva_rating * 1000) / (np.sqrt(3) * p.voltage_rating)

        # Power factor angle
        phi = np.arccos(p.power_factor)

        # Terminal voltage phasor (reference)
        v_t = v_phase + 0j

        # Current phasor (lagging by phi)
        i_a = i_rated * (np.cos(-phi) + 1j * np.sin(-phi))

        # Initial estimate of torque angle
        delta = phi  # Initial guess

        # Iterative solution for torque angle using two-reaction theory
        for iteration in range(50):
            # Id and Iq components
            id_comp = i_rated * np.sin(delta - phi)
            iq_comp = i_rated * np.cos(delta - phi)

            # Voltage equation components
            e_d = -p.xq * iq_comp
            e_q = v_phase * np.sin(delta) + p.ra * id_comp + p.xd * id_comp

            # Induced EMF magnitude
            ef = np.sqrt(e_d**2 + e_q**2)

            # Update torque angle
            psi = np.arctan2(e_d, e_q)
            delta_new = phi + psi

            if abs(delta_new - delta) < 1e-6:
                break
            delta = delta_new

        # Final calculations
        id_comp = i_rated * np.sin(delta - phi)
        iq_comp = i_rated * np.cos(delta - phi)

        e_q = v_phase * np.sin(delta) + p.ra * id_comp + p.xd * id_comp
        e_d = -v_phase * np.cos(delta) + p.ra * iq_comp + p.xq * iq_comp

        ef = np.sqrt(e_q**2 + e_d**2)

        # Voltage regulation
        vr = ((ef - v_phase) / v_phase) * 100

        # Power calculations
        p_out = 3 * v_phase * i_rated * p.power_factor
        p_loss = 3 * i_rated**2 * p.ra
        p_in = p_out + p_loss
        efficiency = (p_out / p_in) * 100 if p_in > 0 else 0

        # Electromagnetic torque
        omega_s = 2 * np.pi * p.frequency
        te = p_out / omega_s

        self.results = {
            'v_phase': v_phase,
            'i_rated': i_rated,
            'phi': phi,
            'phi_deg': np.degrees(phi),
            'delta': delta,
            'delta_deg': np.degrees(delta),
            'id': id_comp,
            'iq': iq_comp,
            'ef': ef,
            'voltage_regulation': vr,
            'power_output': p_out / 1000,  # kW
            'power_loss': p_loss / 1000,  # kW
            'efficiency': efficiency,
            'torque': te,
            'omega_s': omega_s
        }

        return self.results

    def get_phasor_data(self) -> dict:
        """Generate phasor diagram data"""
        if not self.results:
            self.calculate_steady_state()

        r = self.results
        p = self.params

        # Phasors (using V_t as reference at 0°)
        v_t = r['v_phase']
        i_a = r['i_rated'] * np.exp(-1j * r['phi'])
        ef = r['ef'] * np.exp(1j * r['delta'])

        # Voltage drops
        i_ra = i_a * p.ra
        i_xd = r['id'] * p.xd * np.exp(1j * (r['delta'] - np.pi/2))
        i_xq = r['iq'] * p.xq * np.exp(1j * (r['delta']))

        return {
            'v_t': v_t,
            'i_a': i_a,
            'ef': ef,
            'i_ra': i_ra,
            'i_xd': i_xd,
            'i_xq': i_xq
        }


class DynamicSimulator:
    """Dynamic simulation engine with multiple ODE solvers"""

    def __init__(self, params: AlternatorParameters):
        self.params = params
        self.running = False
        self.time_data = []
        self.state_data = []

    def swing_equation(self, t: float, y: np.ndarray, tm: float, te: float) -> np.ndarray:
        """
        Swing equation for alternator dynamics
        y[0] = delta (rotor angle)
        y[1] = omega (rotor speed)
        """
        p = self.params
        omega_s = 2 * np.pi * p.frequency

        # State derivatives
        d_delta = y[1] - omega_s
        d_omega = (tm - te - p.damping * (y[1] - omega_s)) / p.inertia

        return np.array([d_delta, d_omega])

    def simulate_rk45(self, t_span: Tuple[float, float], y0: np.ndarray,
                      tm: float, te: float, n_points: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """Simulate using RK45 (Runge-Kutta 4-5) method"""
        sol = solve_ivp(
            lambda t, y: self.swing_equation(t, y, tm, te),
            t_span,
            y0,
            method='RK45',
            dense_output=True,
            max_step=0.001
        )

        t_eval = np.linspace(t_span[0], t_span[1], n_points)
        y_eval = sol.sol(t_eval)

        return t_eval, y_eval

    def simulate_euler(self, t_span: Tuple[float, float], y0: np.ndarray,
                       tm: float, te: float, dt: float = 0.0001) -> Tuple[np.ndarray, np.ndarray]:
        """Simulate using Euler method"""
        t_points = np.arange(t_span[0], t_span[1], dt)
        y_points = np.zeros((len(y0), len(t_points)))
        y_points[:, 0] = y0

        for i in range(1, len(t_points)):
            dydt = self.swing_equation(t_points[i-1], y_points[:, i-1], tm, te)
            y_points[:, i] = y_points[:, i-1] + dydt * dt

        return t_points, y_points

    def simulate_transient(self, fault_time: float, clearing_time: float,
                          method: str = 'RK45') -> dict:
        """Simulate transient stability with fault"""
        calc = AlternatorCalculator(self.params)
        ss = calc.calculate_steady_state()

        # Initial conditions
        delta0 = ss['delta']
        omega0 = ss['omega_s']
        y0 = np.array([delta0, omega0])

        # Pre-fault
        tm = ss['torque']
        te_pre = ss['torque']

        if method == 'RK45':
            t1, y1 = self.simulate_rk45((0, fault_time), y0, tm, te_pre)
        else:
            t1, y1 = self.simulate_euler((0, fault_time), y0, tm, te_pre)

        # During fault (Te = 0)
        y_fault_start = y1[:, -1]
        fault_duration = clearing_time - fault_time

        if method == 'RK45':
            t2, y2 = self.simulate_rk45((fault_time, clearing_time), y_fault_start, tm, 0)
        else:
            t2, y2 = self.simulate_euler((fault_time, clearing_time), y_fault_start, tm, 0)

        # Post-fault
        y_post_start = y2[:, -1]
        post_time = 1.0

        if method == 'RK45':
            t3, y3 = self.simulate_rk45((clearing_time, clearing_time + post_time),
                                        y_post_start, tm, te_pre)
        else:
            t3, y3 = self.simulate_euler((clearing_time, clearing_time + post_time),
                                         y_post_start, tm, te_pre)

        # Combine results
        t_total = np.concatenate([t1, t2[1:], t3[1:]])
        y_total = np.concatenate([y1, y2[:, 1:], y3[:, 1:]], axis=1)

        return {
            'time': t_total,
            'delta': y_total[0, :],
            'omega': y_total[1, :],
            'delta_deg': np.degrees(y_total[0, :]),
            'speed_pu': y_total[1, :] / omega0
        }


class AdvancedAlternatorGUI:
    """Main GUI application"""

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Salient Pole Alternator Analysis Laboratory")
        self.root.geometry("1400x900")

        # Initialize parameters
        self.params = AlternatorParameters()
        self.calculator = AlternatorCalculator(self.params)
        self.simulator = DynamicSimulator(self.params)

        # Simulation control
        self.simulation_running = False
        self.simulation_thread = None

        # Setup GUI
        self.setup_styles()
        self.create_menu()
        self.create_main_layout()
        self.create_input_panel()
        self.create_control_panel()
        self.create_visualization_panel()
        self.create_results_panel()

        # Bind resize event
        self.root.bind('<Configure>', self.on_window_resize)

        # Initial calculation
        self.calculate_and_update()

    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Subtitle.TLabel', font=('Arial', 10, 'bold'))
        style.configure('Info.TLabel', font=('Arial', 9))

    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Results", command=self.save_results)
        file_menu.add_command(label="Load Configuration", command=self.load_config)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Analysis menu
        analysis_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Analysis", menu=analysis_menu)
        analysis_menu.add_command(label="Steady State", command=self.analyze_steady_state)
        analysis_menu.add_command(label="Transient Stability", command=self.analyze_transient)
        analysis_menu.add_command(label="Load Variation", command=self.analyze_load_variation)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Theory", command=self.show_theory)

    def create_main_layout(self):
        """Create main layout with panels"""
        # Main container with grid
        self.main_container = ttk.Frame(self.root, padding="5")
        self.main_container.grid(row=0, column=0, sticky="nsew")

        # Configure root grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Configure main container grid
        self.main_container.grid_rowconfigure(0, weight=0)  # Input panel
        self.main_container.grid_rowconfigure(1, weight=0)  # Control panel
        self.main_container.grid_rowconfigure(2, weight=1)  # Visualization panel
        self.main_container.grid_rowconfigure(3, weight=0)  # Results panel
        self.main_container.grid_columnconfigure(0, weight=1)

    def create_input_panel(self):
        """Create input parameters panel"""
        input_frame = ttk.LabelFrame(self.main_container, text="Machine Parameters", padding="10")
        input_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Create input grid
        params_list = [
            ("kVA Rating:", "kva_rating", 25.0, 1, 500, "kVA"),
            ("Voltage (Line):", "voltage_rating", 440.0, 100, 11000, "V"),
            ("Frequency:", "frequency", 50.0, 50, 60, "Hz"),
            ("Armature Resistance:", "ra", 0.3, 0.01, 5.0, "Ω"),
            ("Xd (Direct Axis):", "xd", 5.0, 0.1, 20.0, "Ω"),
            ("Xq (Quadrature Axis):", "xq", 3.0, 0.1, 20.0, "Ω"),
            ("Power Factor:", "power_factor", 0.8, 0.1, 1.0, ""),
            ("Poles:", "poles", 4, 2, 12, ""),
        ]

        self.input_vars = {}
        self.input_sliders = {}

        for i, (label, key, default, min_val, max_val, unit) in enumerate(params_list):
            row = i // 4
            col = (i % 4) * 3

            # Label
            ttk.Label(input_frame, text=label).grid(row=row, column=col, sticky="w", padx=5, pady=2)

            # Entry
            var = tk.DoubleVar(value=default)
            self.input_vars[key] = var
            entry = ttk.Entry(input_frame, textvariable=var, width=10)
            entry.grid(row=row, column=col+1, padx=5, pady=2)

            # Unit label
            ttk.Label(input_frame, text=unit).grid(row=row, column=col+2, sticky="w", padx=2, pady=2)

    def create_control_panel(self):
        """Create control panel with sliders and buttons"""
        control_frame = ttk.LabelFrame(self.main_container, text="Simulation Controls", padding="10")
        control_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        # Left side: Sliders
        slider_frame = ttk.Frame(control_frame)
        slider_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Load variation slider
        ttk.Label(slider_frame, text="Load (%):", style='Subtitle.TLabel').grid(row=0, column=0, sticky="w", padx=5)
        self.load_var = tk.DoubleVar(value=100.0)
        self.load_slider = ttk.Scale(slider_frame, from_=0, to=150, variable=self.load_var,
                                     orient=tk.HORIZONTAL, command=self.on_load_change)
        self.load_slider.grid(row=0, column=1, sticky="ew", padx=5)
        self.load_label = ttk.Label(slider_frame, text="100%")
        self.load_label.grid(row=0, column=2, padx=5)

        # Power factor slider
        ttk.Label(slider_frame, text="Power Factor:", style='Subtitle.TLabel').grid(row=1, column=0, sticky="w", padx=5)
        self.pf_slider_var = tk.DoubleVar(value=0.8)
        self.pf_slider = ttk.Scale(slider_frame, from_=0.5, to=1.0, variable=self.pf_slider_var,
                                   orient=tk.HORIZONTAL, command=self.on_pf_change)
        self.pf_slider.grid(row=1, column=1, sticky="ew", padx=5)
        self.pf_label = ttk.Label(slider_frame, text="0.80")
        self.pf_label.grid(row=1, column=2, padx=5)

        # Fault time slider
        ttk.Label(slider_frame, text="Fault Time:", style='Subtitle.TLabel').grid(row=2, column=0, sticky="w", padx=5)
        self.fault_time_var = tk.DoubleVar(value=0.1)
        self.fault_time_slider = ttk.Scale(slider_frame, from_=0.0, to=0.5, variable=self.fault_time_var,
                                          orient=tk.HORIZONTAL)
        self.fault_time_slider.grid(row=2, column=1, sticky="ew", padx=5)
        self.fault_time_label = ttk.Label(slider_frame, text="0.10 s")
        self.fault_time_label.grid(row=2, column=2, padx=5)

        slider_frame.grid_columnconfigure(1, weight=1)

        # Right side: Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.RIGHT, padx=10)

        self.start_btn = ttk.Button(button_frame, text="▶ Start Simulation",
                                    command=self.start_simulation, width=18)
        self.start_btn.grid(row=0, column=0, padx=5, pady=2)

        self.stop_btn = ttk.Button(button_frame, text="⏸ Stop Simulation",
                                   command=self.stop_simulation, width=18, state=tk.DISABLED)
        self.stop_btn.grid(row=1, column=0, padx=5, pady=2)

        self.reset_btn = ttk.Button(button_frame, text="↺ Reset",
                                    command=self.reset_simulation, width=18)
        self.reset_btn.grid(row=2, column=0, padx=5, pady=2)

        self.calculate_btn = ttk.Button(button_frame, text="⚡ Calculate",
                                       command=self.calculate_and_update, width=18)
        self.calculate_btn.grid(row=3, column=0, padx=5, pady=2)

        # Solver selection
        ttk.Label(button_frame, text="ODE Solver:").grid(row=4, column=0, pady=(10, 2))
        self.solver_var = tk.StringVar(value="RK45")
        solver_combo = ttk.Combobox(button_frame, textvariable=self.solver_var,
                                    values=["RK45", "Euler"], width=16, state='readonly')
        solver_combo.grid(row=5, column=0, padx=5)

    def create_visualization_panel(self):
        """Create visualization panel with multiple plot types"""
        viz_frame = ttk.LabelFrame(self.main_container, text="Visualization", padding="5")
        viz_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Notebook for different visualizations
        self.notebook = ttk.Notebook(viz_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Phasor Diagram
        self.phasor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.phasor_frame, text="Phasor Diagram")

        # Tab 2: Time Domain
        self.time_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.time_frame, text="Time Domain Response")

        # Tab 3: Characteristics
        self.char_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.char_frame, text="Characteristics")

        # Tab 4: 3D Visualization
        self.viz_3d_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.viz_3d_frame, text="3D Power-Angle")

        # Create initial plots
        self.create_phasor_plot()
        self.create_time_plot()
        self.create_characteristics_plot()
        self.create_3d_plot()

    def create_phasor_plot(self):
        """Create phasor diagram plot"""
        self.phasor_fig = Figure(figsize=(8, 6), dpi=100)
        self.phasor_ax = self.phasor_fig.add_subplot(111)

        self.phasor_canvas = FigureCanvasTkAgg(self.phasor_fig, self.phasor_frame)
        self.phasor_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_time_plot(self):
        """Create time domain plot"""
        self.time_fig = Figure(figsize=(8, 6), dpi=100)
        self.time_ax1 = self.time_fig.add_subplot(211)
        self.time_ax2 = self.time_fig.add_subplot(212)

        self.time_canvas = FigureCanvasTkAgg(self.time_fig, self.time_frame)
        self.time_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_characteristics_plot(self):
        """Create characteristics plot"""
        self.char_fig = Figure(figsize=(8, 6), dpi=100)
        self.char_ax1 = self.char_fig.add_subplot(221)
        self.char_ax2 = self.char_fig.add_subplot(222)
        self.char_ax3 = self.char_fig.add_subplot(223)
        self.char_ax4 = self.char_fig.add_subplot(224)

        self.char_canvas = FigureCanvasTkAgg(self.char_fig, self.char_frame)
        self.char_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_3d_plot(self):
        """Create 3D visualization"""
        self.viz_3d_fig = Figure(figsize=(8, 6), dpi=100)
        self.viz_3d_ax = self.viz_3d_fig.add_subplot(111, projection='3d')

        self.viz_3d_canvas = FigureCanvasTkAgg(self.viz_3d_fig, self.viz_3d_frame)
        self.viz_3d_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_results_panel(self):
        """Create results display panel"""
        results_frame = ttk.LabelFrame(self.main_container, text="Calculation Results", padding="10")
        results_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        # Create text widget for results
        self.results_text = tk.Text(results_frame, height=8, wrap=tk.WORD, font=('Courier', 9))
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)

    def update_parameters(self):
        """Update alternator parameters from input fields"""
        self.params.kva_rating = self.input_vars['kva_rating'].get()
        self.params.voltage_rating = self.input_vars['voltage_rating'].get()
        self.params.frequency = self.input_vars['frequency'].get()
        self.params.ra = self.input_vars['ra'].get()
        self.params.xd = self.input_vars['xd'].get()
        self.params.xq = self.input_vars['xq'].get()
        self.params.power_factor = self.pf_slider_var.get()
        self.params.poles = int(self.input_vars['poles'].get())

        # Update calculator and simulator
        self.calculator = AlternatorCalculator(self.params)
        self.simulator = DynamicSimulator(self.params)

    def calculate_and_update(self):
        """Calculate and update all displays"""
        try:
            self.update_parameters()
            results = self.calculator.calculate_steady_state()

            # Update results display
            self.display_results(results)

            # Update visualizations
            self.update_phasor_diagram()
            self.update_characteristics()

        except Exception as e:
            messagebox.showerror("Calculation Error", f"Error during calculation:\n{str(e)}")

    def display_results(self, results: dict):
        """Display calculation results"""
        self.results_text.delete(1.0, tk.END)

        output = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SALIENT POLE ALTERNATOR ANALYSIS RESULTS                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

ELECTRICAL PARAMETERS:
├─ Phase Voltage (V_ph):          {results['v_phase']:.2f} V
├─ Rated Current (I_a):            {results['i_rated']:.2f} A
├─ Power Factor Angle (φ):         {results['phi_deg']:.2f}°
└─ Power Factor:                   {self.params.power_factor:.3f} lagging

MACHINE CONSTANTS (Two-Reaction Theory):
├─ Direct Axis Current (I_d):      {results['id']:.2f} A
├─ Quadrature Axis Current (I_q):  {results['iq']:.2f} A
├─ Torque Angle (δ):               {results['delta_deg']:.2f}°
└─ Induced EMF per phase (E_f):    {results['ef']:.2f} V

VOLTAGE REGULATION:
└─ Voltage Regulation:             {results['voltage_regulation']:.2f} %

POWER AND EFFICIENCY:
├─ Output Power:                   {results['power_output']:.2f} kW
├─ Copper Losses:                  {results['power_loss']:.3f} kW
├─ Efficiency:                     {results['efficiency']:.2f} %
└─ Electromagnetic Torque:         {results['torque']:.2f} N·m

OPERATING CONDITIONS:
├─ Synchronous Speed:              {results['omega_s']:.2f} rad/s
├─ Frequency:                      {self.params.frequency} Hz
└─ Number of Poles:                {self.params.poles}

═══════════════════════════════════════════════════════════════════════════════
"""
        self.results_text.insert(1.0, output)

    def update_phasor_diagram(self):
        """Update phasor diagram"""
        self.phasor_ax.clear()

        phasors = self.calculator.get_phasor_data()
        results = self.calculator.results

        # Plot phasors
        origin = [0, 0]

        # Terminal voltage (reference)
        v_t = phasors['v_t']
        self.phasor_ax.quiver(0, 0, v_t.real, v_t.imag, angles='xy', scale_units='xy',
                             scale=1, color='blue', width=0.008, label=f'V_t = {abs(v_t):.1f}∠0°')

        # Current
        i_a = phasors['i_a'] * 5  # Scale for visibility
        self.phasor_ax.quiver(0, 0, i_a.real, i_a.imag, angles='xy', scale_units='xy',
                             scale=1, color='red', width=0.006, label=f'I_a = {results["i_rated"]:.1f}∠{-results["phi_deg"]:.1f}°')

        # Induced EMF
        ef = phasors['ef']
        self.phasor_ax.quiver(0, 0, ef.real, ef.imag, angles='xy', scale_units='xy',
                             scale=1, color='green', width=0.008, label=f'E_f = {results["ef"]:.1f}∠{results["delta_deg"]:.1f}°')

        # Voltage drops (starting from V_t)
        i_ra = phasors['i_ra'] * 5
        self.phasor_ax.quiver(v_t.real, v_t.imag, i_ra.real, i_ra.imag, angles='xy',
                             scale_units='xy', scale=1, color='orange', width=0.004,
                             linestyle='--', label='I·R_a')

        # Add angle annotations
        angle_arc = np.linspace(0, -results['phi'], 50)
        arc_radius = 30
        self.phasor_ax.plot(arc_radius * np.cos(angle_arc), arc_radius * np.sin(angle_arc),
                           'k--', linewidth=0.5)
        self.phasor_ax.text(arc_radius * 1.3, -10, f'φ = {results["phi_deg"]:.1f}°', fontsize=9)

        delta_arc = np.linspace(0, results['delta'], 50)
        self.phasor_ax.plot(arc_radius * 1.5 * np.cos(delta_arc),
                           arc_radius * 1.5 * np.sin(delta_arc), 'g--', linewidth=0.5)
        self.phasor_ax.text(arc_radius * 1.8, 20, f'δ = {results["delta_deg"]:.1f}°',
                           fontsize=9, color='green')

        # Formatting
        self.phasor_ax.set_xlabel('Real Axis (V, A×5)', fontsize=10)
        self.phasor_ax.set_ylabel('Imaginary Axis (V, A×5)', fontsize=10)
        self.phasor_ax.set_title('Phasor Diagram - Salient Pole Alternator', fontsize=12, fontweight='bold')
        self.phasor_ax.grid(True, alpha=0.3)
        self.phasor_ax.legend(loc='upper right', fontsize=8)
        self.phasor_ax.axis('equal')
        self.phasor_ax.axhline(y=0, color='k', linewidth=0.5)
        self.phasor_ax.axvline(x=0, color='k', linewidth=0.5)

        self.phasor_fig.tight_layout()
        self.phasor_canvas.draw()

    def update_characteristics(self):
        """Update characteristic curves"""
        # Clear all axes
        for ax in [self.char_ax1, self.char_ax2, self.char_ax3, self.char_ax4]:
            ax.clear()

        # 1. Load vs Power Factor
        pf_range = np.linspace(0.5, 1.0, 50)
        ef_values = []
        vr_values = []

        original_pf = self.params.power_factor
        for pf in pf_range:
            self.params.power_factor = pf
            calc_temp = AlternatorCalculator(self.params)
            res = calc_temp.calculate_steady_state()
            ef_values.append(res['ef'])
            vr_values.append(res['voltage_regulation'])

        self.params.power_factor = original_pf

        self.char_ax1.plot(pf_range, ef_values, 'b-', linewidth=2)
        self.char_ax1.set_xlabel('Power Factor', fontsize=9)
        self.char_ax1.set_ylabel('Induced EMF (V)', fontsize=9, color='b')
        self.char_ax1.tick_params(axis='y', labelcolor='b')
        self.char_ax1.grid(True, alpha=0.3)
        self.char_ax1.set_title('E_f vs Power Factor', fontsize=10, fontweight='bold')

        # 2. Voltage Regulation vs Load
        load_range = np.linspace(0.25, 1.5, 50)
        vr_load = []
        original_kva = self.params.kva_rating

        for load in load_range:
            self.params.kva_rating = original_kva * load
            calc_temp = AlternatorCalculator(self.params)
            res = calc_temp.calculate_steady_state()
            vr_load.append(res['voltage_regulation'])

        self.params.kva_rating = original_kva

        self.char_ax2.plot(load_range * 100, vr_load, 'r-', linewidth=2)
        self.char_ax2.set_xlabel('Load (%)', fontsize=9)
        self.char_ax2.set_ylabel('Voltage Regulation (%)', fontsize=9)
        self.char_ax2.grid(True, alpha=0.3)
        self.char_ax2.set_title('Voltage Regulation vs Load', fontsize=10, fontweight='bold')

        # 3. Power-Angle Curve
        delta_range = np.linspace(0, np.pi/2, 100)
        power_values = []

        results = self.calculator.calculate_steady_state()
        v_t = results['v_phase']
        ef = results['ef']

        for delta in delta_range:
            # Salient pole power equation
            p1 = (v_t * ef / self.params.xd) * np.sin(delta)
            p2 = (v_t**2 / 2) * ((1/self.params.xq) - (1/self.params.xd)) * np.sin(2*delta)
            power = 3 * (p1 + p2) / 1000  # kW
            power_values.append(power)

        self.char_ax3.plot(np.degrees(delta_range), power_values, 'g-', linewidth=2)
        self.char_ax3.axvline(x=results['delta_deg'], color='r', linestyle='--',
                             label=f'Operating Point δ={results["delta_deg"]:.1f}°')
        self.char_ax3.set_xlabel('Torque Angle δ (degrees)', fontsize=9)
        self.char_ax3.set_ylabel('Power Output (kW)', fontsize=9)
        self.char_ax3.grid(True, alpha=0.3)
        self.char_ax3.legend(fontsize=8)
        self.char_ax3.set_title('Power-Angle Characteristic', fontsize=10, fontweight='bold')

        # 4. Efficiency vs Load
        eff_values = []
        loss_values = []

        for load in load_range:
            self.params.kva_rating = original_kva * load
            calc_temp = AlternatorCalculator(self.params)
            res = calc_temp.calculate_steady_state()
            eff_values.append(res['efficiency'])
            loss_values.append(res['power_loss'])

        self.params.kva_rating = original_kva

        self.char_ax4.plot(load_range * 100, eff_values, 'b-', linewidth=2, label='Efficiency')
        ax4_twin = self.char_ax4.twinx()
        ax4_twin.plot(load_range * 100, loss_values, 'r--', linewidth=2, label='Losses')

        self.char_ax4.set_xlabel('Load (%)', fontsize=9)
        self.char_ax4.set_ylabel('Efficiency (%)', fontsize=9, color='b')
        ax4_twin.set_ylabel('Losses (kW)', fontsize=9, color='r')
        self.char_ax4.tick_params(axis='y', labelcolor='b')
        ax4_twin.tick_params(axis='y', labelcolor='r')
        self.char_ax4.grid(True, alpha=0.3)
        self.char_ax4.set_title('Efficiency & Losses vs Load', fontsize=10, fontweight='bold')

        self.char_fig.tight_layout()
        self.char_canvas.draw()

    def update_3d_visualization(self):
        """Update 3D power surface plot"""
        self.viz_3d_ax.clear()

        # Create meshgrid for delta and excitation
        delta_range = np.linspace(0, np.pi/2, 50)
        ef_range = np.linspace(200, 500, 50)
        Delta, Ef = np.meshgrid(delta_range, ef_range)

        results = self.calculator.calculate_steady_state()
        v_t = results['v_phase']

        # Calculate power surface
        Power = np.zeros_like(Delta)
        for i in range(len(ef_range)):
            for j in range(len(delta_range)):
                p1 = (v_t * Ef[i, j] / self.params.xd) * np.sin(Delta[i, j])
                p2 = (v_t**2 / 2) * ((1/self.params.xq) - (1/self.params.xd)) * np.sin(2*Delta[i, j])
                Power[i, j] = 3 * (p1 + p2) / 1000

        # Plot surface
        surf = self.viz_3d_ax.plot_surface(np.degrees(Delta), Ef, Power,
                                           cmap='viridis', alpha=0.8,
                                           edgecolor='none')

        # Mark operating point
        self.viz_3d_ax.scatter([results['delta_deg']], [results['ef']],
                              [results['power_output']],
                              color='red', s=100, marker='o',
                              label='Operating Point')

        self.viz_3d_ax.set_xlabel('Torque Angle δ (°)', fontsize=9)
        self.viz_3d_ax.set_ylabel('Excitation E_f (V)', fontsize=9)
        self.viz_3d_ax.set_zlabel('Power Output (kW)', fontsize=9)
        self.viz_3d_ax.set_title('3D Power Surface - Salient Pole Alternator',
                                 fontsize=10, fontweight='bold')
        self.viz_3d_ax.legend()

        self.viz_3d_fig.colorbar(surf, ax=self.viz_3d_ax, shrink=0.5)
        self.viz_3d_canvas.draw()

    def start_simulation(self):
        """Start dynamic simulation"""
        if not self.simulation_running:
            self.simulation_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)

            # Run simulation in separate thread
            self.simulation_thread = threading.Thread(target=self.run_dynamic_simulation)
            self.simulation_thread.daemon = True
            self.simulation_thread.start()

    def stop_simulation(self):
        """Stop dynamic simulation"""
        self.simulation_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def reset_simulation(self):
        """Reset simulation parameters"""
        self.stop_simulation()

        # Reset sliders
        self.load_var.set(100.0)
        self.pf_slider_var.set(0.8)
        self.fault_time_var.set(0.1)

        # Reset parameters to defaults
        self.params = AlternatorParameters()
        for key, var in self.input_vars.items():
            var.set(getattr(self.params, key))

        # Recalculate
        self.calculate_and_update()

    def run_dynamic_simulation(self):
        """Run dynamic simulation with transient"""
        try:
            self.update_parameters()

            fault_time = self.fault_time_var.get()
            clearing_time = fault_time + 0.1
            method = self.solver_var.get()

            sim_results = self.simulator.simulate_transient(fault_time, clearing_time, method)

            # Update time domain plots
            self.root.after(0, self.update_time_domain_plot, sim_results)

        except Exception as e:
            self.root.after(0, messagebox.showerror, "Simulation Error",
                          f"Error during simulation:\n{str(e)}")
        finally:
            self.simulation_running = False
            self.root.after(0, self.start_btn.config, {'state': tk.NORMAL})
            self.root.after(0, self.stop_btn.config, {'state': tk.DISABLED})

    def update_time_domain_plot(self, sim_results: dict):
        """Update time domain plots with simulation results"""
        self.time_ax1.clear()
        self.time_ax2.clear()

        t = sim_results['time']
        delta_deg = sim_results['delta_deg']
        speed_pu = sim_results['speed_pu']

        # Plot rotor angle
        self.time_ax1.plot(t, delta_deg, 'b-', linewidth=2)
        self.time_ax1.set_ylabel('Rotor Angle δ (degrees)', fontsize=9)
        self.time_ax1.grid(True, alpha=0.3)
        self.time_ax1.set_title(f'Transient Response - {self.solver_var.get()} Method',
                               fontsize=10, fontweight='bold')

        # Mark fault period
        fault_time = self.fault_time_var.get()
        self.time_ax1.axvspan(fault_time, fault_time + 0.1, alpha=0.2, color='red',
                             label='Fault Period')
        self.time_ax1.legend(fontsize=8)

        # Plot rotor speed
        self.time_ax2.plot(t, speed_pu, 'r-', linewidth=2)
        self.time_ax2.set_xlabel('Time (s)', fontsize=9)
        self.time_ax2.set_ylabel('Speed (pu)', fontsize=9)
        self.time_ax2.grid(True, alpha=0.3)
        self.time_ax2.axhline(y=1.0, color='k', linestyle='--', linewidth=1, alpha=0.5)

        # Mark fault period
        self.time_ax2.axvspan(fault_time, fault_time + 0.1, alpha=0.2, color='red')

        self.time_fig.tight_layout()
        self.time_canvas.draw()

    def on_load_change(self, value):
        """Handle load slider change"""
        load_pct = float(value)
        self.load_label.config(text=f"{load_pct:.0f}%")

        # Update kVA rating
        original_kva = 25.0  # Base rating
        new_kva = original_kva * (load_pct / 100.0)
        self.input_vars['kva_rating'].set(new_kva)

    def on_pf_change(self, value):
        """Handle power factor slider change"""
        pf = float(value)
        self.pf_label.config(text=f"{pf:.2f}")
        self.pf_slider_var.set(pf)

    def on_window_resize(self, event):
        """Handle window resize for autoscaling"""
        # This will be called on window resize
        # The matplotlib canvases will automatically adjust
        pass

    def analyze_steady_state(self):
        """Perform detailed steady-state analysis"""
        self.calculate_and_update()
        self.update_3d_visualization()
        messagebox.showinfo("Analysis Complete",
                          "Steady-state analysis completed.\nCheck all tabs for detailed results.")

    def analyze_transient(self):
        """Perform transient stability analysis"""
        self.start_simulation()

    def analyze_load_variation(self):
        """Analyze system under load variation"""
        self.notebook.select(self.char_frame)
        self.update_characteristics()
        messagebox.showinfo("Analysis Complete",
                          "Load variation analysis completed.\nCheck Characteristics tab.")

    def save_results(self):
        """Save results to file"""
        try:
            with open('alternator_results.txt', 'w') as f:
                f.write(self.results_text.get(1.0, tk.END))
            messagebox.showinfo("Success", "Results saved to alternator_results.txt")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results:\n{str(e)}")

    def load_config(self):
        """Load configuration"""
        messagebox.showinfo("Info", "Configuration loading feature - To be implemented")

    def show_about(self):
        """Show about dialog"""
        about_text = """
Advanced Salient Pole Alternator Analysis Laboratory
Version 1.0

Developed for Electrical Engineering Education and Research

Features:
• Comprehensive steady-state analysis using two-reaction theory
• Dynamic simulation with multiple ODE solvers (RK45, Euler)
• Interactive visualization with phasor diagrams
• Real-time parameter adjustment
• Transient stability analysis
• Load variation studies

© 2025 Electrical Engineering Laboratory
"""
        messagebox.showinfo("About", about_text)

    def show_theory(self):
        """Show theoretical background"""
        theory_text = """
SALIENT POLE ALTERNATOR THEORY

Two-Reaction Theory:
The two-reaction theory decomposes the armature MMF into two components:
• Direct axis (d-axis): aligned with pole axis
• Quadrature axis (q-axis): 90° electrical from d-axis

Power Equation (Salient Pole):
P = (V·Ef/Xd)·sin(δ) + (V²/2)·[(1/Xq) - (1/Xd)]·sin(2δ)

Where:
• V = terminal voltage
• Ef = induced EMF
• δ = torque angle
• Xd = direct axis synchronous reactance
• Xq = quadrature axis synchronous reactance

The first term represents the fundamental power component.
The second term is the reluctance power (unique to salient pole).

Voltage Regulation:
VR = [(Ef - V) / V] × 100%

Swing Equation:
M·d²δ/dt² + D·dδ/dt = Tm - Te

Used for transient stability analysis.
"""
        messagebox.showinfo("Theory", theory_text)


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = AdvancedAlternatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
