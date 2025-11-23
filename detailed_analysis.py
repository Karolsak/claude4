"""
Detailed analysis of Economical Conductor problems
Explores wider range and provides comprehensive analysis
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def analyze_problem1_detailed():
    """Detailed analysis of Problem 1 with extended range"""

    print("\n" + "="*80)
    print(" DETAILED ANALYSIS: PROBLEM 1 - 3-PHASE TRANSMISSION LINE")
    print("="*80)

    # Parameters
    V = 110000  # V
    loads_mw = [20, 5, 6]
    hours = [6, 12, 10]
    pf = 0.8

    # Calculate currents
    P = [mw * 1e6 for mw in loads_mw]
    currents = [p / (np.sqrt(3) * V * pf) for p in P]
    I_rms = np.sqrt(sum(I**2 * h for I, h in zip(currents, hours)) / 24)

    print(f"\nRMS Current: {I_rms:.2f} A")

    # Try different interpretations
    print("\n" + "-"*80)
    print("TESTING DIFFERENT FORMULATIONS:")
    print("-"*80)

    # Formulation 1: As originally coded
    print("\n1. Standard formulation (3 conductors, all costs per km):")
    A_range_1 = np.linspace(0.1, 20, 2000)
    costs_1 = []
    for A in A_range_1:
        capital = (9000 + 600 * A) * 0.10
        energy_loss = 3 * I_rms**2 * (0.176/A) * 8760 / 1000
        energy_cost = energy_loss * 0.06
        total = capital + energy_cost
        costs_1.append(total)

    opt_idx_1 = np.argmin(costs_1)
    opt_A_1 = A_range_1[opt_idx_1]
    print(f"   Optimal A = {opt_A_1:.4f} cm²")
    print(f"   Min Cost  = Rs. {costs_1[opt_idx_1]:.2f}/km/year")

    # Formulation 2: Cost is for all 3 conductors
    print("\n2. Total cost includes all 3 conductors (capital = 3 * cost):")
    costs_2 = []
    for A in A_range_1:
        capital = 3 * (9000 + 600 * A) * 0.10
        energy_loss = 3 * I_rms**2 * (0.176/A) * 8760 / 1000
        energy_cost = energy_loss * 0.06
        total = capital + energy_cost
        costs_2.append(total)

    opt_idx_2 = np.argmin(costs_2)
    opt_A_2 = A_range_1[opt_idx_2]
    print(f"   Optimal A = {opt_A_2:.4f} cm²")
    print(f"   Min Cost  = Rs. {costs_2[opt_idx_2]:.2f}/km/year")

    # Formulation 3: Per-phase power loss (I_phase instead of I_line)
    # For balanced 3-phase, line current = phase current
    print("\n3. Using line-to-neutral voltage and phase current:")
    V_phase = V / np.sqrt(3)
    I_phase = I_rms  # For balanced system
    costs_3 = []
    for A in A_range_1:
        capital = (9000 + 600 * A) * 0.10
        # Power loss per phase, 3 phases total
        energy_loss = 3 * I_phase**2 * (0.176/A) * 8760 / 1000
        energy_cost = energy_loss * 0.06
        total = capital + energy_cost
        costs_3.append(total)

    opt_idx_3 = np.argmin(costs_3)
    opt_A_3 = A_range_1[opt_idx_3]
    print(f"   Optimal A = {opt_A_3:.4f} cm²")
    print(f"   Min Cost  = Rs. {costs_3[opt_idx_3]:.2f}/km/year")

    # Formulation 4: What if the answer key is expecting 1.64 cm²?
    # Let's reverse engineer what conditions would give that answer
    print("\n4. Reverse engineering for A = 1.64 cm²:")
    A_expected = 1.64

    # Using Kelvin's Law: A_opt = sqrt((energy_loss_factor * Ce) / (capital_rate * Cc))
    # If A_opt = 1.64, then:
    # 1.64² = (P_factor * 0.06) / (0.10 * 600)
    # 2.6896 = (P_factor * 0.06) / 60
    # P_factor = 2.6896 * 60 / 0.06 = 2689.6

    # If P_factor = 3 * I² * 8760 * ρ / 1000, then:
    # 2689.6 = 3 * I² * 8760 * 0.176 / 1000
    # I² = 2689.6 * 1000 / (3 * 8760 * 0.176)
    # I² = 2689600 / 4624.32
    # I = 23.84 A

    required_I = np.sqrt(2689.6 * 1000 / (3 * 8760 * 0.176))
    print(f"   Required RMS current for A=1.64: {required_I:.2f} A")
    print(f"   Actual RMS current: {I_rms:.2f} A")
    print(f"   Ratio: {I_rms / required_I:.2f}")

    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Problem 1: Detailed Analysis of Different Formulations',
                 fontsize=14, fontweight='bold')

    # Plot 1: Formulation 1
    ax1 = axes[0, 0]
    ax1.plot(A_range_1, costs_1, 'b-', linewidth=2)
    ax1.axvline(opt_A_1, color='r', linestyle='--', label=f'Opt: {opt_A_1:.3f} cm²')
    ax1.axvline(1.64, color='g', linestyle='--', label='Expected: 1.64 cm²')
    ax1.set_xlabel('Cross-section (cm²)')
    ax1.set_ylabel('Total Annual Cost (Rs/km)')
    ax1.set_title('Formulation 1: Standard')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 10)

    # Plot 2: Formulation 2
    ax2 = axes[0, 1]
    ax2.plot(A_range_1, costs_2, 'b-', linewidth=2)
    ax2.axvline(opt_A_2, color='r', linestyle='--', label=f'Opt: {opt_A_2:.3f} cm²')
    ax2.axvline(1.64, color='g', linestyle='--', label='Expected: 1.64 cm²')
    ax2.set_xlabel('Cross-section (cm²)')
    ax2.set_ylabel('Total Annual Cost (Rs/km)')
    ax2.set_title('Formulation 2: 3x Capital Cost')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 10)

    # Plot 3: All formulations compared (zoomed to 0-5 cm²)
    ax3 = axes[1, 0]
    zoom_mask = A_range_1 <= 5
    ax3.plot(A_range_1[zoom_mask], np.array(costs_1)[zoom_mask], 'b-',
             label='Form 1', linewidth=2)
    ax3.plot(A_range_1[zoom_mask], np.array(costs_2)[zoom_mask], 'r-',
             label='Form 2', linewidth=2)
    ax3.axvline(1.64, color='g', linestyle='--', alpha=0.7, label='Expected: 1.64')
    ax3.set_xlabel('Cross-section (cm²)')
    ax3.set_ylabel('Total Annual Cost (Rs/km)')
    ax3.set_title('Comparison (Zoomed: 0-5 cm²)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Plot 4: Cost components at expected answer
    ax4 = axes[1, 1]
    A_test = np.array([0.5, 1.0, 1.64, 2.0, 3.0, 5.0])
    cap_costs = (9000 + 600 * A_test) * 0.10
    energy_losses = 3 * I_rms**2 * (0.176/A_test) * 8760 / 1000 * 0.06

    x = np.arange(len(A_test))
    width = 0.35
    ax4.bar(x - width/2, cap_costs, width, label='Capital Cost')
    ax4.bar(x + width/2, energy_losses, width, label='Energy Cost')
    ax4.set_xlabel('Cross-section (cm²)')
    ax4.set_ylabel('Annual Cost (Rs/km)')
    ax4.set_title('Cost Breakdown at Different Cross-sections')
    ax4.set_xticks(x)
    ax4.set_xticklabels([f'{a:.2f}' for a in A_test])
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('/home/user/claude4/problem1_detailed_analysis.png', dpi=300, bbox_inches='tight')
    print(f"\n✓ Detailed visualization saved: problem1_detailed_analysis.png")
    plt.close()

    return opt_A_1, opt_A_2

if __name__ == "__main__":
    analyze_problem1_detailed()
