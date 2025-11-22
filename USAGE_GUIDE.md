# Kelvin's Law Calculator - Usage Guide

## Quick Start

### Option 1: Run Complete Demonstration (Recommended for first-time users)

This will run all calculations, show detailed analysis, and save visualization plots:

```bash
python kelvins_law_demo.py
```

**Output:**
- Detailed console output with step-by-step calculations
- Analysis of optimal conductor size
- Practical considerations and limitations
- Saved plot: `kelvins_law_complete_analysis.png`

### Option 2: Interactive Matplotlib GUI (No Tkinter required)

If you want to experiment with parameters using sliders:

```bash
python kelvins_law_matplotlib.py
```

**Features:**
- Interactive sliders for all parameters
- Real-time plot updates
- Works without Tkinter (uses matplotlib backend)

### Option 3: Tkinter GUI (If Tkinter is installed)

For a full-featured GUI experience:

```bash
python kelvins_law_calculator.py
```

**Features:**
- Professional windowed interface
- Tabbed interface with results and limitations
- More polished UI
- **Note:** Requires `python3-tk` package

### Option 4: Verification and Testing

To verify calculations without GUI:

```bash
python verify_calculations.py
```

## What Each File Does

### 1. `kelvins_law_demo.py` ⭐ **START HERE**
**Purpose:** Complete educational demonstration

**What it does:**
- Solves the complete problem step-by-step
- Explains Kelvin's Law principle
- Calculates optimal conductor size
- Checks practical constraints (voltage drop, current capacity)
- Recommends practical standard size
- Discusses limitations
- Creates comprehensive visualization

**Use when:**
- Learning about Kelvin's Law
- Understanding the complete problem
- Preparing reports or presentations
- Need publication-quality plots

**Output files:**
- Console: Full detailed analysis
- File: `kelvins_law_complete_analysis.png` (4-panel visualization)

---

### 2. `kelvins_law_matplotlib.py`
**Purpose:** Interactive parameter exploration (no Tkinter)

**What it does:**
- Provides sliders to adjust all parameters
- Updates plots in real-time
- Shows cost analysis and limitations

**Use when:**
- Experimenting with different scenarios
- Performing sensitivity analysis
- No Tkinter available
- Teaching/demonstration

**Controls:**
- 13 sliders for various parameters
- Automatic plot updates
- Results shown on right panel

---

### 3. `kelvins_law_calculator.py`
**Purpose:** Professional GUI application (Tkinter)

**What it does:**
- Full-featured windowed application
- Tabbed interface
- Polished user experience

**Use when:**
- Tkinter is available
- Prefer traditional desktop application
- Need professional-looking interface

**Requirements:**
- Tkinter (`python3-tk` on Linux)

---

### 4. `verify_calculations.py`
**Purpose:** Non-interactive verification

**What it does:**
- Verifies calculations are correct
- Shows detailed breakdown
- Creates basic plots
- No GUI required

**Use when:**
- Testing the calculations
- Debugging
- Automated testing
- Generating quick reports

## Problem Being Solved

**Industrial Power Distribution Problem:**

An industrial load needs a 3-phase cable over 6 km from a sub-station at 11 kV.

**Load Cycle (6 days/week):**
- Load 1: 700 kW at 0.8 p.f. for 7 hours/day
- Load 2: 400 kW at 0.9 p.f. for 3 hours/day
- Load 3: 88 kW at 1.0 p.f. for 14 hours/day

**Economic Parameters:**
- Cable cost: Rs. (5000A + 1500) per km (A = area in mm²)
- Tariff: Rs. 150/year per kVA + Rs. 0.05 per kWh
- Interest + Depreciation: 15%
- Resistance: 0.173/A Ω-km

**Question:** What is the most economical conductor size?

## Understanding the Results

### Kelvin's Law Optimal vs. Practical Size

The calculator finds two different sizes:

1. **Kelvin's Law Optimal:** ~5-10 mm²
   - Minimizes only economic costs
   - Ignores practical constraints
   - Theoretical minimum

2. **Practical Recommended:** ~25-35 mm²
   - Considers voltage drop
   - Ensures current capacity
   - Accounts for future growth
   - Uses standard sizes

### Why the Difference?

This demonstrates key limitations:

1. **Low Energy Tariff:** At 5 paise/kWh, energy losses cost almost nothing
2. **Voltage Drop:** 5mm² would cause excessive voltage drop (though not in this specific case)
3. **Current Capacity:** 5mm² would overheat with 45.93 A (current density = 9.2 A/mm²)
4. **Mechanical Strength:** Small conductors may not be strong enough
5. **Standard Sizes:** 5mm² may not be commercially available

## Interpreting the Plots

### Plot 1: Kelvin's Law Cost Components
- **Green line:** Capital cost (increases with size)
- **Orange line:** Energy loss cost (decreases with size)
- **Blue dashed:** Total of above two (Kelvin's law objective)
- **Red vertical:** Optimal point where total is minimum
- **Purple vertical:** Practical recommended size

**Key insight:** Capital cost dominates because energy tariff is low

### Plot 2: Voltage Drop vs. Size
- Shows voltage drop percentage
- **Orange line:** 5% typical limit
- **Red line:** 6% maximum limit
- Smaller conductors = higher voltage drop

### Plot 3: Current Density vs. Size
- **Green zone:** Safe range (2-4 A/mm²)
- Shows risk of overheating for small conductors

### Plot 4: Total Annual Cost
- Includes all costs (MD charge, energy, capital, losses)
- Shows that total cost doesn't vary much with size
- This is because MD and energy costs are fixed

## Parameters You Can Adjust

### Load Parameters (3 independent loads)
- **Power (kW):** Active power consumption
- **Power Factor:** 0.6 to 1.0 (1.0 = unity, purely resistive)
- **Hours/day:** Operating hours for each load

### System Parameters
- **Distance (km):** Cable length
- **Voltage (kV):** Line-to-line voltage

### Economic Parameters
- **Energy Tariff (Rs/kWh):** Cost per unit of energy
- **Interest + Depreciation (%):** Annual charge on capital

## Example Use Cases

### Use Case 1: "What if energy cost doubles?"
1. Run `kelvins_law_matplotlib.py`
2. Move "Tariff (Rs/kWh)" slider from 0.05 to 0.10
3. Observe optimal size increases
4. Higher energy cost → justify larger conductors

### Use Case 2: "What if load increases 50%?"
1. Run `kelvins_law_matplotlib.py`
2. Increase all load powers by 50%
3. Observe impact on optimal size
4. Check current density and voltage drop

### Use Case 3: "Shorter distance?"
1. Adjust "Distance (km)" slider to 2 km
2. Observe optimal size decreases
3. Shorter distance → less resistance → smaller conductor acceptable

### Use Case 4: "Generate report for presentation"
1. Run `python kelvins_law_demo.py > report.txt`
2. Use the generated `kelvins_law_complete_analysis.png`
3. You have complete documentation

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'tkinter'"
**Solution:** Use matplotlib version instead:
```bash
python kelvins_law_matplotlib.py
```

### Issue: "ModuleNotFoundError: No module named 'matplotlib'"
**Solution:** Install requirements:
```bash
pip install -r requirements.txt
```

### Issue: Plot window doesn't show
**Solution:** Ensure you're not running over SSH without X11 forwarding. Use the demo version which saves plots to files:
```bash
python kelvins_law_demo.py
```

### Issue: Optimal size seems too small
**This is correct!** It demonstrates a key limitation. The practical recommended size accounts for real-world constraints.

## Advanced Usage

### Modifying the Code

All three versions share the same `KelvinsLawCalculator` class with these methods:

```python
calc = KelvinsLawCalculator()

# Modify parameters
calc.distance = 10  # km
calc.voltage = 33   # kV
calc.load1_kw = 1000
calc.load1_pf = 0.85

# Calculate
optimal_area, areas, costs, data = calc.find_optimal_area()

print(f"Optimal size: {optimal_area:.2f} mm²")
print(f"Total cost: Rs. {data['total_cost']:,.2f}")
```

### Batch Analysis

Create a script to test multiple scenarios:

```python
from kelvins_law_matplotlib import KelvinsLawCalculator
import matplotlib.pyplot as plt

calc = KelvinsLawCalculator()
distances = [2, 4, 6, 8, 10]
optimal_sizes = []

for dist in distances:
    calc.distance = dist
    optimal, _, _, _ = calc.find_optimal_area()
    optimal_sizes.append(optimal)

plt.plot(distances, optimal_sizes)
plt.xlabel('Distance (km)')
plt.ylabel('Optimal Area (mm²)')
plt.title('Optimal Conductor Size vs. Distance')
plt.savefig('sensitivity_distance.png')
```

## Educational Value

This tool demonstrates:

1. **Kelvin's Law Principle:** Economic optimization in conductor selection
2. **Real-world Constraints:** Why theory differs from practice
3. **Multi-factor Decision Making:** Economics vs. engineering requirements
4. **Variable Load Handling:** Working with non-constant loads
5. **Tariff Structures:** Two-part tariffs (demand + energy)
6. **Sensitivity Analysis:** How parameters affect outcomes

## Key Takeaways

1. ✅ Kelvin's Law provides a good starting point
2. ⚠️ Always check practical constraints
3. ⚠️ Voltage drop and current capacity often dominate
4. ⚠️ Low energy costs push toward minimal sizes
5. ✅ Use standard sizes closest to calculated optimum
6. ✅ Include margin for future load growth

## References & Further Reading

- Kelvin's Law: Economic conductor size selection
- Voltage Drop: Typically limit to 3-6%
- Current Density: Copper = 2-4 A/mm² (depends on installation)
- Power Factor: cos(φ), affects current magnitude
- Standard Conductor Sizes: IEC/IS standards

## Support

For issues or questions:
- Check this guide first
- Run `verify_calculations.py` to test
- Review the code comments
- See `README_kelvins_law.md` for theory

---

**Version:** 1.0
**Last Updated:** November 2025
