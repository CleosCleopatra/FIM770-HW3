import numpy as np
import matplotlib.pyplot as plt

a = 4 / 9
b = 5 / 9
Ic = 68 / 405
eps = 1

I_values = np.linspace(0,1, 400)

def f(t, inp, I):
    x, y = inp
    return [(x - x ** 3 / 3 - y + I)/eps, (x + a - b *y)]

from scipy.optimize import fsolve
real_parts = np.zeros(len(I_values))
imag_parts = np.zeros(len(I_values))
#from numpy.linalg import eigvals
for k, I in enumerate(I_values):
    #coeff = [1, 0, (3-3*b), (3*b *I - 3* a)]
    #roots = np.roots(coeff)
    #print(roots)
    #reals = [r.real for r in roots if abs(r.imag) < 1e-6]
    #if reals:
    #    if k == 0:
    #        x = reals[0]
    #    else:
    #        x = min (reals, key = lambda r: abs(r-x_values[k-1]))
    #lse:
    #    chose = min(roots, key = lambda r: abs(r.imag))
    #    x = chose.real
    #x_values[k] = x

    x = None
    coeffs = [b/3.0, 0, (1-b), a-b*I]
    r = np.roots(coeffs)
    for val in r:
        if abs(val.imag) < 1e-8:
            x = val.real
    if not x:
        idx = np.argmin(np.abs(r.imag))
        x = r[idx].real


    y = x - (1/3) * x**3 + I

    J = [[(1/eps)*(1-x**2), -(1/eps)], [1, -b]]
    eigs = np.linalg.eigvals(J)

    real_parts[k] = np.mean([eig.real for eig in eigs])
    imag_parts[k] = np.mean([abs(eig.imag) for eig in eigs])

Ic = 68/405

plt.figure()
plt.plot(I_values, real_parts, label = 'Real')
plt.plot(I_values, imag_parts, label='Imaginary')
plt.axvline(Ic, label = "Bifurcation", c="green")
plt.xlabel('I')
plt.ylabel('Value')
plt.title('Eigenvalue over I')
plt.legend()
plt.show()


#c

I_below = 0.1
I_above = 0.3

xs = np.linspace(-3, 3, 30)
ys = np.linspace(-3, 3, 30)
X, Y = np.meshgrid(xs, ys)

fig, ax = plt.subplots(1,2)

U_below = (1/eps) * (X - X**3/3-Y + I_below)
U_above = (1/eps) * (X - X**3/3-Y + I_above)
V = X + a -b * Y

time = np.linspace(0,200, 5000)

start_points = [(-2, 1), (-1, 2), (0,-2), (1,0)]
from scipy.integrate import solve_ivp
for values in start_points:
    sol = solve_ivp(f, [0,200], values, args=(I_below, ), t_eval = time)
    ax[0].plot(sol.y[0], sol.y[1], label = f"start point is {values}")
    ax[0].quiver(X, Y, U_below, V, color="gray", alpha=0.4)


    sol = solve_ivp(f, [0,200], values, args=(I_above, ), t_eval=time)
    ax[1].plot(sol.y[0], sol.y[1], label = f"start point is {values}")
    ax[1].quiver(X, Y, U_below, V, color="gray", alpha=0.4)


ax[0].set_title(f"I = {I_below}")
ax[1].set_title("I = {I_above}")
ax[0].set_xlabel("x")
ax[0].set_ylabel("y")
ax[1].set_xlabel("x")
ax[1].set_ylabel("y")
plt.legend()
plt.title("phase diagram")
plt.show()
