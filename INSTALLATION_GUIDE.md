# Installation and Usage Guide

## Advanced Salient Pole Alternator Analysis Laboratory

---

## System Requirements

### Python Version
- Python 3.7 or higher
- Tested on Python 3.8, 3.9, 3.10, and 3.11

### Operating Systems
- ✓ Linux (Ubuntu, Debian, Fedora, etc.)
- ✓ Windows 10/11
- ✓ macOS 10.14+

---

## Installation Steps

### Step 1: Install Required Python Packages

Open a terminal (Linux/macOS) or Command Prompt (Windows) and run:

```bash
pip3 install numpy matplotlib scipy
```

Or using the requirements file:

```bash
pip3 install -r requirements.txt
```

### Step 2: Verify Installation

```bash
python3 -c "import numpy, matplotlib, scipy; print('All packages installed successfully!')"
```

### Step 3: Download the Application

Ensure you have the following files:
- `alternator_advanced_lab.py` - Main application
- `test_alternator_calculations.py` - Test and verification script
- `ALTERNATOR_SOLUTION.md` - Complete solution documentation
- `requirements.txt` - Package dependencies

---

## Running the Application

### Method 1: Direct Execution

```bash
python3 alternator_advanced_lab.py
```

### Method 2: Make Executable (Linux/macOS)

```bash
chmod +x alternator_advanced_lab.py
./alternator_advanced_lab.py
```

---

## Testing the Calculations

To verify the calculations are correct, run the test script:

```bash
python3 test_alternator_calculations.py
```

This will:
1. Calculate all parameters for the given problem
2. Display the primary answers (torque angle, induced EMF, voltage regulation)
3. Validate the calculations against expected values
4. Show additional performance metrics

**Expected Output:**
```
TORQUE ANGLE (δ):                   42.45°
INDUCED EMF PER PHASE (E_f):        204.81 V
VOLTAGE REGULATION (VR):            -19.37 %
```

---

## Quick Start Tutorial

### 1. Launch Application

```bash
python3 alternator_advanced_lab.py
```

A window titled "Advanced Salient Pole Alternator Analysis Laboratory" will appear.

### 2. Default Problem Solution

The application opens with the default parameters matching the problem:
- 25 kVA, 440 V, 50 Hz
- Star-connected
- Ra = 0.3 Ω, Xd = 5 Ω, Xq = 3 Ω
- Power Factor = 0.8 lagging

The results are immediately calculated and displayed.

### 3. View Phasor Diagram

Click on the "Phasor Diagram" tab to see:
- Terminal voltage (V_t) - blue arrow
- Armature current (I_a) - red arrow
- Induced EMF (E_f) - green arrow
- Voltage drops - orange dashed arrows
- Angles φ and δ annotated

### 4. Explore Characteristics

Click on the "Characteristics" tab to view:
- **Top Left:** E_f vs Power Factor
- **Top Right:** Voltage Regulation vs Load
- **Bottom Left:** Power-Angle Curve (operating point marked)
- **Bottom Right:** Efficiency & Losses vs Load

### 5. Run Dynamic Simulation

1. Click on "Time Domain Response" tab
2. Select ODE solver (RK45 or Euler) from dropdown
3. Adjust fault time using slider if desired
4. Click "▶ Start Simulation" button
5. Watch the transient response unfold

The simulation shows:
- Rotor angle oscillations during fault
- Speed variations
- Fault period (red shaded region)
- System stability assessment

### 6. Adjust Parameters

**Using Input Fields:**
- Modify any parameter in the "Machine Parameters" panel
- Click "⚡ Calculate" to update all results

**Using Sliders:**
- **Load (%):** Adjusts kVA rating (0-150%)
- **Power Factor:** Changes from 0.5 to 1.0
- **Fault Time:** Sets when fault occurs (0-0.5s)

Changes from sliders update in real-time.

### 7. 3D Visualization

Click "3D Power-Angle" tab to see:
- Power surface as function of torque angle and excitation
- Current operating point marked in red
- Interactive 3D rotation (click and drag)
- Zoom (scroll wheel)

### 8. Analyze Different Scenarios

**Menu: Analysis → Steady State**
- Comprehensive steady-state analysis
- Updates 3D visualization
- Complete results display

**Menu: Analysis → Transient Stability**
- Initiates transient simulation
- Assesses stability margins
- Shows dynamic response

**Menu: Analysis → Load Variation**
- Studies system under varying loads
- Updates characteristic curves
- Performance assessment

### 9. Save Results

**Menu: File → Save Results**
- Saves calculation results to `alternator_results.txt`
- Includes all computed parameters
- Formatted for easy reading

---

## Understanding the Interface

### Top Section: Machine Parameters
- Input fields for all alternator parameters
- Direct editing capability
- Unit labels provided

### Middle Section: Simulation Controls
- **Sliders:** Interactive parameter adjustment
- **Buttons:**
  - ▶ Start Simulation - Begin dynamic analysis
  - ⏸ Stop Simulation - Halt current simulation
  - ↺ Reset - Return to default parameters
  - ⚡ Calculate - Update all calculations
- **ODE Solver:** Choose between RK45 (accurate) or Euler (fast)

### Center Section: Visualization Tabs
Four tabs provide different views:
1. **Phasor Diagram** - Vector representation
2. **Time Domain Response** - Dynamic behavior
3. **Characteristics** - Performance curves
4. **3D Power-Angle** - Surface visualization

### Bottom Section: Results Display
- Comprehensive text output
- All calculated parameters
- Formatted tables
- Scrollable for long results

---

## Tips and Best Practices

### 1. Parameter Ranges

**Realistic Ranges:**
- kVA Rating: 1 - 500 kVA
- Voltage: 100 - 11000 V
- Frequency: 50 or 60 Hz
- Ra: 0.01 - 5 Ω
- Xd: 0.5 - 20 Ω (typically > Xq)
- Xq: 0.5 - 15 Ω (typically < Xd)
- Power Factor: 0.5 - 1.0

**Important:** Xd should always be greater than Xq for salient pole machines.

### 2. Simulation Settings

**For Stable Results:**
- Use RK45 solver for accurate results
- Keep fault time < 0.2s
- Ensure inertia > 0.1

**For Quick Exploration:**
- Use Euler solver for faster computation
- Increase time step (trade accuracy for speed)

### 3. Visualization

**Phasor Diagram:**
- All phasors scaled appropriately
- Current scaled by 5× for visibility
- Reference: Terminal voltage at 0°

**3D Plot:**
- Rotate: Click and drag
- Zoom: Scroll wheel or pinch gesture
- Reset view: Double-click

### 4. Performance

**For Smooth Operation:**
- Close unused applications
- Use moderate window size
- Limit excessive parameter changes during simulation

---

## Common Use Cases

### Case 1: Design Verification

**Scenario:** Verify a new alternator design meets specifications

**Steps:**
1. Enter design parameters
2. Set rated load and power factor
3. Click Calculate
4. Check voltage regulation < 5% (typical requirement)
5. Verify efficiency > 95%
6. Assess torque angle < 60° (stability margin)

### Case 2: Load Analysis

**Scenario:** Understand performance across load range

**Steps:**
1. Go to Characteristics tab
2. Observe "Voltage Regulation vs Load" curve
3. Check "Efficiency & Losses vs Load"
4. Identify optimal operating region
5. Note maximum efficiency point

### Case 3: Stability Assessment

**Scenario:** Evaluate transient stability

**Steps:**
1. Click Start Simulation
2. Observe rotor angle oscillations
3. Check for damping (oscillations should decay)
4. Verify speed returns to synchronous
5. Adjust fault time to find critical clearing time

### Case 4: Educational Demonstration

**Scenario:** Teach two-reaction theory

**Steps:**
1. Show phasor diagram
2. Explain Id and Iq components
3. Vary power factor with slider
4. Observe phasor changes
5. Discuss voltage regulation at different PF
6. Show power-angle curve
7. Highlight reluctance power component

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'numpy'"

**Solution:**
```bash
pip3 install numpy matplotlib scipy
```

If pip3 doesn't work, try:
```bash
python3 -m pip install numpy matplotlib scipy
```

### Issue: "TclError" or Tkinter not available

**Solution (Linux):**
```bash
sudo apt-get install python3-tk
```

**Solution (macOS):**
```bash
brew install python-tk
```

**Solution (Windows):**
- Reinstall Python with "tcl/tk and IDLE" option checked

### Issue: Plots not displaying properly

**Solution:**
1. Resize window - plots auto-scale
2. Switch between tabs
3. Click Calculate again
4. Close and restart application

### Issue: Calculation errors or unrealistic results

**Check:**
1. All parameters are positive
2. Xd > Xq (for salient pole)
3. Power factor between 0 and 1
4. Voltage and current ratings reasonable
5. Reactances appropriate for rating

### Issue: Simulation doesn't start

**Check:**
1. ODE solver is selected
2. Parameters are valid
3. Click Stop, then Reset, then Start again
4. Check console for error messages

### Issue: Application runs slow

**Solutions:**
1. Close other resource-intensive applications
2. Use Euler solver instead of RK45
3. Reduce simulation time
4. Use smaller window size

---

## Advanced Features

### Custom Scenarios

Create your own test cases:

```python
# Example: High-voltage industrial alternator
params = AlternatorParameters(
    kva_rating=500.0,      # 500 kVA
    voltage_rating=6600.0, # 6.6 kV
    frequency=50.0,
    ra=0.5,
    xd=12.0,
    xq=8.0,
    power_factor=0.85,
    poles=6
)
```

### Batch Analysis

For research or multiple calculations:

```python
# Analyze across power factor range
pf_range = [0.6, 0.7, 0.8, 0.9, 1.0]
results_list = []

for pf in pf_range:
    params.power_factor = pf
    calc = AlternatorCalculator(params)
    results_list.append(calc.calculate_steady_state())
```

### Data Export

Results can be saved and further processed:

```python
import json

# Export to JSON
with open('results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

---

## Educational Resources

### Recommended Reading

1. **Two-Reaction Theory**
   - P.S. Bimbhra - "Electrical Machinery"
   - Chapter on Synchronous Machines

2. **Transient Analysis**
   - P. Kundur - "Power System Stability and Control"
   - Section on Generator Dynamics

3. **Phasor Diagrams**
   - A.E. Fitzgerald - "Electric Machinery"
   - Salient Pole Synchronous Machines

### Practice Problems

The application can solve problems with:
- Different ratings (1 kVA to 500 kVA)
- Various voltages (220V to 11kV)
- Multiple pole configurations
- Leading/lagging power factors
- Overload conditions

### Lab Exercises

1. **Exercise 1:** Effect of Power Factor
   - Vary PF from 0.5 to 1.0
   - Plot VR vs PF
   - Explain the relationship

2. **Exercise 2:** Stability Limits
   - Increase load gradually
   - Find maximum stable torque angle
   - Determine pull-out power

3. **Exercise 3:** Fault Response
   - Simulate 3-phase fault
   - Measure critical clearing time
   - Assess equal area criterion

---

## Version History

### Version 1.0 (2025)
- Initial release
- Steady-state analysis with two-reaction theory
- Dynamic simulation with RK45 and Euler
- Multiple visualization modes
- Interactive GUI with real-time controls
- Comprehensive documentation

---

## Support

For technical support:
1. Check this installation guide
2. Review ALTERNATOR_SOLUTION.md
3. Run test_alternator_calculations.py
4. Check Python and package versions

For educational questions:
1. Review the Theory section in Help menu
2. Consult recommended textbooks
3. Contact your instructor

---

## Contributing

Suggestions for improvements:
- Additional analysis features
- More visualization options
- Extended machine models
- Database integration
- Report generation

---

## License

This software is provided for educational and research purposes.

© 2025 Electrical Engineering Laboratory

---

**Happy Learning and Analyzing! ⚡**

For the best experience:
- Start with default parameters to see the solution
- Experiment with sliders for interactive learning
- Run simulations to understand dynamic behavior
- Use 3D visualization for comprehensive understanding

*"From theory to practice - bringing electrical engineering to life!"*
