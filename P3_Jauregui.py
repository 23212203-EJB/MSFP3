"""
Práctica 3: Sistema Musculoesquelético

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Jáuregui Bogarin Ernesto
Número de control: 23212203
Correo institucional: l23212203@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Datos de la simulación
F0 = 1.0
alpha = 0.25
Cg = 10e-6
Cp = 100e-6
R_control = 100
R_caso = 10e3

t = np.arange(0, 10.001, 1e-3)
A = F0
u = np.zeros_like(t)
u[(t >= 1) & (t <= 2)] = A


# Función de respuesta RC por ecuación en diferencias
def rc_ce(u, t, tau):
    y = np.zeros_like(u)
    dt = t[1] - t[0]
    a = np.exp(-dt / tau)

    for k in range(1, len(t)):
        y[k] = a * y[k - 1] + (1 - a) * u[k - 1]

    return y


# Función de respuesta RC por función de transferencia
def rc_ft(u, t, tau):
    sys = signal.TransferFunction([1], [tau, 1])
    _, y, _ = signal.lsim(sys, U=u, T=t)
    return y


# Constantes de tiempo
tau_control = R_control * Cp
tau_caso = R_caso * Cp


# Respuestas de los sistemas RC
F_control_CE = rc_ce(u, t, tau_control)
F_control_FT = rc_ft(u, t, tau_control)

F_caso_CE = rc_ce(u, t, tau_caso)
F_caso_FT = rc_ft(u, t, tau_caso)


# Función de respuesta del controlador PID
def pid_response(u, t, tau, Kp, Ki, Kd):
    num = [Kd, Kp, Ki]
    den = [tau + Kd, 1 + Kp, Ki]

    sys = signal.TransferFunction(num, den)
    _, y, _ = signal.lsim(sys, U=u, T=t)

    return y

# Parámetros del controlador PID
PID_caso = pid_response(u, t, tau_caso, 45, 120, 0.02)

# Señales de salida
Fsx = 0.75 * F_control_FT
Fsy = F_caso_FT
PID = 0.75 * PID_caso


plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'cm'


clr1 = np.array([165,214,167]) / 255
clr2 = np.array([102,187,106]) / 255
clr3 = np.array([27,94,32]) / 255
clr4 = np.array([255,222,100]) / 255

fig, ax = plt.subplots(figsize=(11, 4.5), facecolor='white')

ax.plot(
    t, u, '-',
    linewidth=1.5,
    color=clr1,
    label=r'$F(t)$'
)


ax.plot(
    t, Fsx, '-',
    linewidth=1.5,
    color=clr2,
    label=r'$F_s(t): Control$'
)


ax.plot(
    t, Fsy, '-',
    linewidth=2,
    color=clr3,
    label=r'$F_s(t): Caso$'
)


ax.plot(
    t, PID, '-',
    linewidth=1.5,
    color=clr4,
    label=r'$PI(t): Tratamiento$'
)


ax.set_xlabel(r'$t$ [s]')
ax.set_ylabel(r'$F(t)$ [V]')

ax.set_xlim(0, 10)
ax.set_xticks(np.arange(0, 11, 1))

ax.set_ylim(-0.1, 1.1)
ax.set_yticks(np.arange(-0.1, 1.11, 0.1))


ax.set_title('')
ax.grid(False)
ax.tick_params(
    direction='in',
    top=True,
    right=True
)

for spine in ax.spines.values():
    spine.set_linewidth(1.1)

ax.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, 1.13),
    ncol=4,
    frameon=False,
    fontsize=10
)

plt.tight_layout()

plt.savefig(
    'Sistema_Musculoesqueletico.pdf',
    format='pdf',
    bbox_inches='tight'
)

plt.show()