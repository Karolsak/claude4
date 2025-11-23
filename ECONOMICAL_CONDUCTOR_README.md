# Economical Conductor Cross-Section Calculator

A comprehensive Python application using Tkinter to solve economical conductor sizing problems based on **Kelvin's Law**.

## Theory: Kelvin's Law

Kelvin's Law states that the most economical cross-section of a conductor is achieved when the **annual cost of energy losses** equals the **annual interest and depreciation on the capital cost** of the conductor.

### Formula

For the most economical cross-section `A`:

```
A = √[(Annual Energy Loss Factor × Energy Cost) / (Annual Capital Cost Factor)]
```

The total annual cost consists of:
1. **Capital Cost**: Interest and depreciation on initial investment
2. **Energy Cost**: Cost of power losses due to conductor resistance

## Problem 1: 3-Phase Transmission Line

### Given Data
- **Voltage**: 110 kV, 3-phase
- **Load Cycles** (daily):
  - 6 hours at 20 MW, pf = 0.8 lag
  - 12 hours at 5 MW, pf = 0.8 lag
  - 10 hours at 6 MW, pf = 0.8 lag
- **Line Cost**: Rs. (9,000 + 600A) per km, where A is in cm²
- **Interest + Depreciation**: 10%
- **Energy Cost**: 6 paise/unit (Rs. 0.06/kWh)
- **Resistance**: 0.176/A Ω per km per conductor
- **Expected Answer**: 1.64 cm²

### Solution Approach

1. **Calculate currents** for each load:
   ```
   I = P / (√3 × V × pf)
   ```

2. **Calculate RMS current** considering daily cycle:
   ```
   I_rms = √[(I₁²×h₁ + I₂²×h₂ + I₃²×h₃) / 24]
   ```

3. **Calculate costs** for various cross-sections:
   - Capital cost per km per year = (9000 + 600A) × 0.10
   - Annual energy loss = 3 × I_rms² × R × 8760 hours
   - Energy cost = Annual loss × 0.06 Rs/kWh

4. **Find minimum** total cost

## Problem 2: DC Feeder System

### Given Data
- **Current**: 120 A
- **Voltage**: 250 V DC
- **Length**: 1 km
- **Cable Cost**: Rs. 20A per metre (two-core), where A is in cm²
- **Energy Cost**: 10 paise/kWh (Rs. 0.10/kWh)
- **Interest + Depreciation**: 8%
- **Resistance**: 0.15 Ω per km per cm² cross-section

### Solution Approach

1. **Total capital cost** for two-core cable:
   ```
   Capital = 20 × A × 1000 Rs
   ```

2. **Annual capital charge**:
   ```
   Annual Capital Cost = Capital × 0.08
   ```

3. **Resistance** (both cores):
   ```
   R_total = 2 × (0.15 × L / A)
   ```

4. **Annual energy loss**:
   ```
   Loss = I² × R × 8760 / 1000 kWh
   ```

5. **Find minimum** total annual cost

## Features

### Interactive Sliders
- **Problem 1**: Adjust voltage, load powers, hours, power factor, costs, interest rate
- **Problem 2**: Adjust current, voltage, length, costs, interest rate

### Real-Time Visualization
- Cost breakdown graphs (Capital vs Energy vs Total)
- Zoomed view around optimal point
- Clear indication of minimum cost point

### Detailed Results
- Optimal cross-section from numerical optimization
- Optimal cross-section from Kelvin's Law formula
- Annual cost breakdown
- System characteristics (losses, efficiency, voltage drop)

## Installation

```bash
# Required packages
pip install numpy matplotlib tkinter
```

## Usage

```bash
python economical_conductor_calculator.py
```

### Navigation
1. Use tabs to switch between Problem 1 and Problem 2
2. Adjust sliders to change parameters
3. Results and graphs update in real-time
4. Observe how different parameters affect the optimal cross-section

## Key Insights

### Problem 1 Results
- With default parameters: **Optimal A ≈ 1.64 cm²**
- Shows how variable loads affect conductor sizing
- Demonstrates importance of RMS current calculation
- Three-phase system considerations

### Problem 2 Results
- Simpler DC system analysis
- Direct relationship between current and conductor size
- Voltage drop considerations for long feeders
- Two-core cable cost modeling

## Educational Value

This calculator helps understand:

1. **Trade-offs**: Larger conductors cost more but save energy
2. **Optimization**: Finding the sweet spot between capital and operating costs
3. **System Design**: How different parameters affect economic decisions
4. **Kelvin's Law**: Practical application of classical electrical engineering principle

## Mathematical Background

### For 3-Phase System (Problem 1)

Power loss per phase:
```
P_loss = I² × R
```

Total loss (3 phases):
```
P_total = 3 × I_rms² × (ρ/A)
```

Annual energy loss:
```
E_loss = P_total × 8760 hours
```

### For DC System (Problem 2)

Total resistance (go and return):
```
R_total = 2 × ρ × L / A
```

Power loss:
```
P_loss = I² × R_total
```

Voltage drop:
```
V_drop = I × R_total
```

## Tips for Using the Calculator

1. **Start with default values** to see the baseline solution
2. **Vary one parameter at a time** to understand its impact
3. **Watch the graphs** to see how costs interact
4. **Compare numerical and analytical results** - they should match closely
5. **Note the flat minimum** - small variations around optimal A don't significantly change cost

## Verification

The calculator's results can be verified by:
- Comparing with textbook solutions
- Checking dimensional consistency
- Verifying Kelvin's Law condition at optimum
- Ensuring capital cost equals energy cost at optimal point (approximately)

## License

Educational tool for electrical engineering students and professionals.

## Author

Created for demonstrating Kelvin's Law applications in transmission line and feeder design.
