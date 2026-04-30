import numpy as np
from scipy.integrate import odeint

class DoublePendulumModel:
    @staticmethod
    def get_derivative(state, t, m1, m2, l1, l2, g=9.81):
        """
        Počítá derivace pro odeint. Vrací [theta1_dot, theta1_ddot, theta2_dot, theta2_ddot]
        """
        theta1, omega1, theta2, omega2 = state
        delta = theta1 - theta2

        # Společná část jmenovatele [m1 + m2 * sin^2(theta1 - theta2)]
        den_common = m1 + m2 * (np.sin(delta) ** 2)
        den1 = l1 * den_common
        den2 = l2 * den_common

        dydx = np.zeros_like(state)

        # d(theta_1)/dt = omega_1
        dydx[0] = omega1

        # rozdil oproti prezentace -> mělo na levé straně úhlovou rychlost theta s tečkou
        # tady počítáme úhlové zrychlení, změnu rychlosti omega_1
        dydx[1] = (
            m2 * g * np.sin(theta2) * np.cos(delta)
            - m2 * np.sin(delta) * (l1 * (omega1 ** 2) * np.cos(delta) + l2 * (omega2 ** 2))
            - (m1 + m2) * g * np.sin(theta1)
        ) / den1

        # d(theta_2)/dt = omega_2
        dydx[2] = omega2

        # ten samy problem jako u omega_1
        dydx[3] = (
            (m1 + m2) * (l1 * (omega1 ** 2) * np.sin(delta) - g * np.sin(theta2) + g * np.sin(theta1) * np.cos(delta))
            + m2 * l2 * (omega2 ** 2) * np.sin(delta) * np.cos(delta)
        ) / den2

        return dydx

    @staticmethod
    def simulate(state_0, t_max=30, dt=0.02, m1=1.0, m2=1.0, l1=1.0, l2=1.0):
        """
        Vyřeší diferenciální rovnice a převede úhly na x, y souřadnice.
        """
        t = np.arange(0, t_max, dt)
        sol = odeint(DoublePendulumModel.get_derivative, state_0, t, args=(m1, m2, l1, l2))

        theta1 = sol[:, 0]
        theta2 = sol[:, 2]

        x1 = l1 * np.sin(theta1)
        y1 = -l1 * np.cos(theta1)

        x2 = x1 + l2 * np.sin(theta2)
        y2 = y1 - l2 * np.cos(theta2)

        return x1, y1, x2, y2, t