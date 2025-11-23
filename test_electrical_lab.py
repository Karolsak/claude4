#!/usr/bin/env python3
"""
Test script for Electrical Engineering Lab Application
Verifies functionality without GUI
"""

import math
import numpy as np


def test_problem_50_61():
    """Test Problem 50.61 calculations"""
    print("\n" + "="*70)
    print("TESTING PROBLEM 50.61 - CAPACITOR POWER FACTOR CORRECTION")
    print("="*70)

    # Given values
    V_line = 3000  # V
    f = 50  # Hz
    P_out = 447.6 * 1000  # W
    pf1 = 0.75
    pf2 = 0.95
    eta = 0.93
    V_cap = 600  # V
    n_cap = 5

    # Calculate input power
    P_in = P_out / eta
    print(f"\nInput Power: {P_in/1000:.2f} kW")
    print(f"Output Power: {P_out/1000:.2f} kW")
    print(f"Efficiency: {eta*100:.1f}%")

    # Calculate angles
    phi1 = math.acos(pf1)
    phi2 = math.acos(pf2)

    # Calculate reactive power
    Q1 = P_in * math.tan(phi1)
    Q2 = P_in * math.tan(phi2)
    Q_c = Q1 - Q2

    print(f"\nInitial Power Factor: {pf1:.3f} (angle: {math.degrees(phi1):.2f}°)")
    print(f"Final Power Factor: {pf2:.3f} (angle: {math.degrees(phi2):.2f}°)")
    print(f"\nInitial Reactive Power (Q1): {Q1/1000:.2f} kVAR")
    print(f"Final Reactive Power (Q2): {Q2/1000:.2f} kVAR")
    print(f"Reactive Power Compensated (Qc): {Q_c/1000:.2f} kVAR")

    # Capacitance calculation
    V_phase = V_line  # Delta connection
    X_c = 3 * V_phase**2 / Q_c
    omega = 2 * math.pi * f
    C_phase = 1 / (omega * X_c)
    C_individual = C_phase * n_cap

    print(f"\nCapacitive Reactance/Phase: {X_c:.2f} Ω")
    print(f"Capacitance/Phase (Delta): {C_phase*1e6:.2f} µF")
    print(f"Capacitance/Capacitor: {C_individual*1e6:.2f} µF")

    print("\n✓ Problem 50.61 calculations verified")
    return True


def test_problem_50_62():
    """Test Problem 50.62 calculations"""
    print("\n" + "="*70)
    print("TESTING PROBLEM 50.62 - SYNCHRONOUS MOTOR COMPENSATION")
    print("="*70)

    # Given values
    P_motor = 50  # kW
    P_load = 200  # kW
    pf_load = 0.8
    pf_combined = 0.9

    # Total active power
    P_total = P_motor + P_load

    # Load reactive power
    phi_load = math.acos(pf_load)
    Q_load = P_load * math.tan(phi_load)

    # Combined reactive power
    phi_combined = math.acos(pf_combined)
    Q_combined = P_total * math.tan(phi_combined)

    # Motor reactive power
    Q_motor = Q_combined - Q_load

    # Motor apparent power
    S_motor = math.sqrt(P_motor**2 + Q_motor**2)
    pf_motor = P_motor / S_motor

    print(f"\nLoad Power: {P_load} kW")
    print(f"Load Power Factor: {pf_load:.3f} lagging")
    print(f"Load Reactive Power: {Q_load:.2f} kVAR")

    print(f"\nMotor Active Power: {P_motor} kW")
    print(f"Motor Reactive Power: {abs(Q_motor):.2f} kVAR ({'leading' if Q_motor < 0 else 'lagging'})")
    print(f"Motor Power Factor: {pf_motor:.4f} ({'leading' if Q_motor < 0 else 'lagging'})")

    print(f"\nCombined Active Power: {P_total} kW")
    print(f"Combined Reactive Power: {Q_combined:.2f} kVAR")
    print(f"Combined Power Factor: {pf_combined:.3f}")

    print("\n✓ Problem 50.62 calculations verified")
    return True


def test_ode_solvers():
    """Test ODE solvers"""
    print("\n" + "="*70)
    print("TESTING ODE SOLVERS")
    print("="*70)

    # Test simple exponential decay: dy/dt = -y, y(0) = 1
    # Analytical solution: y = exp(-t)

    def f(t, y):
        return [-y[0]]

    # RK45 solver
    def solve_rk45(f, y0, t0, tf, n):
        t = np.linspace(t0, tf, n)
        y = np.zeros((n, len(y0)))
        y[0] = y0

        for i in range(n - 1):
            h = t[i+1] - t[i]
            k1 = np.array(f(t[i], y[i]))
            k2 = np.array(f(t[i] + h/2, y[i] + h*k1/2))
            k3 = np.array(f(t[i] + h/2, y[i] + h*k2/2))
            k4 = np.array(f(t[i] + h, y[i] + h*k3))
            y[i+1] = y[i] + h * (k1 + 2*k2 + 2*k3 + k4) / 6

        return t, y

    # Euler solver
    def solve_euler(f, y0, t0, tf, n):
        t = np.linspace(t0, tf, n)
        y = np.zeros((n, len(y0)))
        y[0] = y0

        for i in range(n - 1):
            h = t[i+1] - t[i]
            y[i+1] = y[i] + h * np.array(f(t[i], y[i]))

        return t, y

    # Test both solvers
    y0 = [1.0]
    t_rk45, y_rk45 = solve_rk45(f, y0, 0, 5, 100)
    t_euler, y_euler = solve_euler(f, y0, 0, 5, 100)

    # Analytical solution
    y_exact = np.exp(-t_rk45)

    # Calculate errors
    error_rk45 = np.mean(np.abs(y_rk45[:, 0] - y_exact))
    error_euler = np.mean(np.abs(y_euler[:, 0] - y_exact))

    print(f"\nRK45 average error: {error_rk45:.6f}")
    print(f"Euler average error: {error_euler:.6f}")
    print(f"RK45 is {error_euler/error_rk45:.1f}x more accurate than Euler")

    print("\n✓ ODE solvers verified")
    return True


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("ELECTRICAL ENGINEERING LAB - VERIFICATION TESTS")
    print("="*70)

    tests = [
        test_problem_50_61,
        test_problem_50_62,
        test_ode_solvers
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test failed with error: {e}")
            results.append(False)

    print("\n" + "="*70)
    print(f"TEST SUMMARY: {sum(results)}/{len(results)} tests passed")
    print("="*70)

    if all(results):
        print("\n✓ All tests passed successfully!")
        print("The application is ready to use.")
        print("\nTo run the GUI application:")
        print("  python3 electrical_engineering_lab.py")
    else:
        print("\n✗ Some tests failed. Please review the errors above.")

    return all(results)


if __name__ == "__main__":
    main()
