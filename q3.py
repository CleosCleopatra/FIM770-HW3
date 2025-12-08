import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def f(t, X, mu):
    x, y = X
    return [
        mu*x + y - x**2,
        -x + mu*y + 2*x**2
    ]

# equilibrium is at (0,0)
x0 = np.array([1e-4, 0])   # small initial offset along unstable direction
mus = np.linspace(0.1, 1.0, 30)  # sweep range

for mu in mus:
    sol = solve_ivp(lambda t, X: f(t, X, mu),
                    [0, 100],
                    x0,
                    max_step=0.1)

    x, y = sol.y

    plt.figure()
    plt.plot(x, y)
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)

    plt.title(f"Phase portrait for mu={mu:.2f}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axhline(0, color="k", linewidth=0.3)
    plt.axvline(0, color="k", linewidth=0.3)
    plt.gca().set_aspect("equal", 'box')
    plt.show()
