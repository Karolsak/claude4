# Advanced Electrical Engineering Laboratory

A comprehensive Python + Tkinter application for electrical engineering calculations, simulations, and analysis.

## Features

### 1. **Problem Solver**
- **Problem 10**: Power factor correction with capacitor bank calculation
  - 3-phase motor analysis
  - Star-connected capacitor bank design
  - Detailed step-by-step solutions

- **Problem 11**: Economic analysis of power factor correction
  - Cost-benefit analysis
  - Maximum economical cost calculation
  - Plant capacity vs. correction apparatus comparison

### 2. **Motor Dynamics Simulation**
- Real-time dynamic simulation with differential equations
- **ODE Solvers**:
  - RK45 (Runge-Kutta 4-5th order adaptive)
  - Euler (Fixed step)
- Interactive parameter control with sliders:
  - Voltage, Frequency, Power
  - Efficiency, Resistance, Inductance
  - Inertia, Friction
- Real-time visualization:
  - Angular velocity (speed in RPM)
  - Rotor angle
  - d-axis and q-axis currents

### 3. **Power Factor Analysis**
- Comprehensive power factor correction analysis
- Interactive parameter adjustment
- Advanced visualizations:
  - Phasor diagrams (before and after correction)
  - Power triangle comparison
  - Current reduction analysis
  - Power factor vs. current curves

### 4. **Advanced GUI Features**
- **Main Menu** with navigation
- **Tabbed Interface** for organized workflow
- **Auto-scaling plots** that adjust to window size
- **Responsive design** with automatic layout adjustment
- **Interactive controls** with real-time sliders
- **Start/Stop/Reset** buttons for simulation control
- **Professional visualizations** with matplotlib integration

## Installation

1. Install required dependencies:
```bash
pip install -r requirements_ee_lab.txt
```

2. Run the application:
```bash
python3 advanced_ee_lab.py
```

## Usage Guide

### Main Menu Tab
- Overview of all features
- Quick navigation buttons to each section

### Problem Solver Tab
Navigate to specific problems:
- **Problem 10**: Click "Solve Problem 10" to calculate capacitor bank requirements
- **Problem 11**: Click "Solve Problem 11" for economic analysis

### Motor Simulation Tab
1. Adjust motor parameters using sliders
2. Select ODE solver (RK45 or Euler)
3. Set simulation duration
4. Click "Start" to run simulation
5. Use "Stop" to pause, "Reset" to clear results
6. View real-time plots of:
   - Speed (RPM)
   - Rotor angle
   - Current components

### Power Factor Analysis Tab
1. Adjust system parameters:
   - Active Power (kW)
   - Voltage (V)
   - Initial and Target Power Factor
   - Frequency (Hz)
2. Click "Calculate & Visualize"
3. View results and visualizations:
   - Calculated reactive power compensation
   - Required capacitance
   - Phasor diagrams
   - Power triangles
   - Current reduction analysis

## Technical Details

### Mathematical Models

#### Power Factor Correction
- **Reactive Power Compensation**: Q_c = Q1 - Q2 = P(tan θ1 - tan θ2)
- **Capacitance Calculation**: C = 1/(ωX_c) where X_c = V²_phase/Q_c
- **Apparent Power Reduction**: ΔS = S1 - S2 = P(1/pf1 - 1/pf2)

#### Motor Dynamics
State equations:
```
dω/dt = (T_e - T_load) / J
dθ/dt = ω
di_d/dt = (V_d - Ri_d + ωLi_q) / L
di_q/dt = (V_q - Ri_q - ωLi_d) / L
```

Where:
- ω: angular velocity
- θ: rotor angle
- i_d, i_q: d-q axis currents
- T_e: electromagnetic torque
- J: moment of inertia
- R, L: resistance and inductance

### ODE Solvers

#### RK45 (Recommended)
- Adaptive step size
- 4th/5th order Runge-Kutta
- High accuracy
- Automatic error control

#### Euler
- Fixed step size
- First order method
- Simple and fast
- Educational purposes

## Problem Solutions

### Problem 10 Results
Given:
- Line Voltage: 3000 V
- Frequency: 50 Hz
- Power Output: 223.8 kW (375 hp)
- Efficiency: 92%
- Initial PF: 0.75 lagging
- Target PF: 0.9 lagging
- Connection: Star, 3 capacitors in series per phase

**Solution**: Capacitance of each capacitor ≈ 118 µF

### Problem 11 Results
Given:
- Initial PF: 0.7 lagging
- Target PF: 0.9 lagging
- Plant cost: Rs. 800/kVA

**Solution**: Maximum cost of correction apparatus to be economical

## Application Architecture

```
AdvancedEELaboratory (Main Application)
├── PowerFactorCorrectionSolver (Problem Solver)
├── MotorDynamicsSimulator (Simulation Engine)
├── PlotManager (Visualization)
└── GUI Components
    ├── Main Menu Tab
    ├── Problem Solver Tab
    ├── Motor Simulation Tab
    └── Power Factor Analysis Tab
```

## Key Features Implementation

### Auto-scaling and Responsive Design
- All plots automatically adjust to window size
- Grid weights configured for proper expansion
- Canvas resize event handling
- Matplotlib tight_layout for optimal spacing

### Real-time ODE Integration
- scipy.integrate.solve_ivp for RK45
- Custom Euler implementation
- Configurable time span and step size
- Real-time visualization updates

### Interactive Controls
- ttk.Scale widgets for smooth parameter adjustment
- Real-time value display
- Callback functions for instant updates
- Disabled/enabled states for simulation control

## Dependencies

- Python 3.7+
- numpy: Numerical computations
- scipy: ODE solvers
- matplotlib: Plotting and visualization
- tkinter: GUI (included with Python)

## Practical Applications

1. **Power System Design**: Calculate required capacitor banks for power factor correction
2. **Economic Analysis**: Evaluate cost-effectiveness of correction equipment
3. **Motor Control**: Understand motor dynamics and transient behavior
4. **Educational Tool**: Learn about power systems, motor theory, and numerical methods
5. **Engineering Projects**: Quick calculations and visualizations for reports

## Advanced Features

- **Multiple ODE Solvers**: Compare different numerical methods
- **Parameter Sweeps**: Easily adjust parameters to see effects
- **Professional Visualizations**: Publication-quality plots
- **Export Capabilities**: Use matplotlib toolbar to save figures
- **Zoom and Pan**: Interactive plot navigation
- **Grid Display**: Clear grid lines for accurate reading

## Tips for Best Results

1. Start with default parameters to understand baseline behavior
2. Use RK45 solver for accurate results
3. Increase simulation time to see steady-state behavior
4. Adjust window size for better visualization
5. Use matplotlib toolbar to zoom into specific regions
6. Export results using toolbar save button

## License

Educational and research purposes.

## Author

Created for electrical engineering education and practical applications.
