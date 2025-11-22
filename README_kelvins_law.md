# Kelvin's Law - Economic Conductor Size Calculator

## Overview

This application provides an interactive visualization and calculation tool for determining the most economical conductor cross-section using **Kelvin's Law**, applied to a real-world electrical engineering problem.

## Problem Statement

An industrial load is supplied by a 3-phase cable from a sub-station at a distance of 6 km. The voltage at the load is 11 kV. The daily load cycle for six days in a week for the entire year is:

1. 700 kW at 0.8 p.f. for 7 hours
2. 400 kW at 0.9 p.f. for 3 hours
3. 88 kW at unity p.f. for 14 hours

**Objective**: Compute the most economical cross-section of conductors.

## Features

### 1. Interactive Visualization
- **Cost vs. Conductor Size Plot**: Shows how total annual cost varies with conductor cross-section
- **Cost Breakdown Plot**: Visualizes capital costs vs. energy loss costs
- **Real-time Updates**: All plots update instantly as you adjust parameters

### 2. Adjustable Parameters (Sliders)
- **Distance**: 1-20 km
- **Voltage**: 3.3-33 kV
- **Load 1, 2, 3**: Independent control of:
  - Power (kW)
  - Power Factor (0.6-1.0)
  - Operating Hours (1-24 hours/day)
- **Economic Parameters**:
  - Energy Tariff (Rs/kWh)
  - Interest + Depreciation Rate (%)

### 3. Comprehensive Results
- Optimal conductor cross-section
- Electrical characteristics (resistance, current, kVA)
- Energy analysis (consumption, losses, percentage)
- Detailed cost breakdown

### 4. Kelvin's Law Limitations Discussion
Comprehensive explanation of 12 major limitations:
- Variable load assumptions
- Voltage drop considerations
- Mechanical strength requirements
- Standard size availability
- Load growth projections
- Temperature effects
- And more...

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Required Packages

```bash
pip install numpy matplotlib
```

Or using the requirements file:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python kelvins_law_calculator.py
```

### Using the Interface

1. **Adjust Parameters**: Use the sliders on the left panel to modify:
   - System parameters (distance, voltage)
   - Load conditions (power, power factor, hours)
   - Economic factors (tariffs, interest rates)

2. **View Results**:
   - Top-right panel shows cost analysis plots
   - Bottom-right panel has two tabs:
     - **Calculation Results**: Detailed numerical results
     - **Kelvin's Law Limitations**: Educational content about limitations

3. **Recalculate**: Click "Recalculate" button or adjust any slider to update

## Understanding the Results

### Optimal Conductor Size
The application calculates the conductor cross-section that minimizes total annual cost, which includes:
- **Capital Cost**: Annual charge (interest + depreciation) on cable investment
- **Energy Cost**: Cost of energy consumed by the load
- **Loss Cost**: Cost of energy losses in the conductor

### Kelvin's Law Principle
The economic optimum occurs when:
```
Annual cost of energy losses = Annual fixed charges on capital cost
```

This is shown graphically where the capital cost curve (decreasing) intersects with the loss cost curve (increasing).

## Technical Details

### Calculations

1. **Current Calculation**:
   ```
   I = (kVA × 1000) / (√3 × V_L × 1000)
   ```

2. **Resistance**:
   ```
   R = (0.173 / A) × L  [Ω]
   ```
   where A = cross-section (mm²), L = length (km)

3. **Power Loss** (3-phase):
   ```
   P_loss = 3 × I² × R  [W]
   ```

4. **Annual Energy Loss**:
   ```
   E_loss = Σ(P_loss × hours × days)  [kWh]
   ```

5. **Total Annual Cost**:
   ```
   TAC = Capital_charge + MD_charge + Energy_cost + Loss_cost
   ```

### Default Problem Values

```
Distance          : 6 km
Voltage           : 11 kV
Load 1            : 700 kW, 0.8 pf, 7 hrs
Load 2            : 400 kW, 0.9 pf, 3 hrs
Load 3            : 88 kW, 1.0 pf, 14 hrs
Cable Cost        : Rs. (5000×A + 1500) per km
MD Tariff         : Rs. 150/annum per kVA
Energy Tariff     : Rs. 0.05 per kWh
Interest + Depr.  : 15%
Resistance        : 0.173/A Ω-km
```

## Key Limitations of Kelvin's Law

The application includes a comprehensive discussion of limitations. Key points:

1. **Variable Loads**: Assumes constant load; real loads vary continuously
2. **Voltage Drop**: Focuses only on economics, not voltage regulation
3. **Mechanical Strength**: Economic size may be too small structurally
4. **Standard Sizes**: Calculated size may not match available sizes
5. **Load Growth**: Doesn't account for future expansion
6. **Temperature Effects**: Assumes constant resistance
7. **Power Factor Variations**: Complex with varying power factors
8. **Cost Fluctuations**: Metal and energy prices change over time

## Educational Value

This tool is designed for:
- **Students**: Understanding Kelvin's Law and its application
- **Engineers**: Quick economic analysis of conductor sizing
- **Educators**: Demonstrating the principles and limitations
- **Researchers**: Sensitivity analysis of various parameters

## Practical Considerations

When selecting actual conductors, also consider:
- ✓ Voltage drop (typically ±6% limit)
- ✓ Short circuit capacity
- ✓ Mechanical strength (span, wind, ice loading)
- ✓ Standard available sizes (round to nearest)
- ✓ Future load growth (25-50% margin typical)
- ✓ Regulatory requirements
- ✓ Safety factors

## Example Output

For the default problem:
```
Optimal Conductor Cross-Section: ~47-50 mm²
Maximum Demand: 875 kVA
Annual Energy Consumption: ~1.65 million kWh
Annual Energy Losses: ~25,000 kWh
Loss Percentage: ~1.5%
Total Annual Cost: ~Rs. 214,000
```

## File Structure

```
kelvins_law_calculator.py    # Main application file
README_kelvins_law.md        # This file
requirements.txt             # Python dependencies
```

## License

This is an educational tool created for learning purposes.

## Author

Created as a comprehensive solution for understanding Kelvin's Law in electrical power systems.

## Version

Version 1.0 - November 2025

---

**Note**: This tool provides theoretical calculations. Always verify with detailed engineering analysis and consult relevant electrical codes and standards before implementing in real-world scenarios.
