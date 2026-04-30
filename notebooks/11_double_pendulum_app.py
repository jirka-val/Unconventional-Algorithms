import tkinter as tk
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

# Propojení se složkou src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.models.double_pendulum import DoublePendulumModel


class DoublePendulumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chaos Theory: Double Pendulum Animation")
        self.root.geometry("1200x850")

        # Matplotlib Plátno
        self.fig, self.ax = plt.subplots(figsize=(8, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Ovládací panel vpravo
        control_frame = tk.Frame(self.root, width=300)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=15, pady=10)

        # Proměnné
        self.m1 = tk.DoubleVar(value=1.0)
        self.m2 = tk.DoubleVar(value=1.0)
        self.l1 = tk.DoubleVar(value=1.0)
        self.l2 = tk.DoubleVar(value=1.0)

        # Počáteční úhly
        self.theta1_pi = tk.DoubleVar(value=0.99)
        self.theta2_pi = tk.DoubleVar(value=1.01)

        # Tvorba inputů
        self.create_input(control_frame, "Mass 1 (m1)", self.m1)
        self.create_input(control_frame, "Mass 2 (m2)", self.m2)
        self.create_input(control_frame, "Length 1 (l1)", self.l1)
        self.create_input(control_frame, "Length 2 (l2)", self.l2)
        tk.Label(control_frame, text="--- Angles (Multipliers of π) ---", fg="gray").pack(pady=(15, 0))
        self.create_input(control_frame, "Theta 1 (Start angle)", self.theta1_pi)
        self.create_input(control_frame, "Theta 2 (Start angle)", self.theta2_pi)

        # Akční tlačítka
        tk.Button(control_frame, text="Start Animation", command=self.start_animation, bg="#90EE90", height=2).pack(
            pady=(30, 10), fill=tk.X)
        tk.Button(control_frame, text="Stop Animation", command=self.stop_animation, bg="#FFB6C1", height=2).pack(
            fill=tk.X)

        self.ani = None
        self.is_running = False

    def create_input(self, parent, label_text, variable):
        tk.Label(parent, text=label_text).pack(pady=(5, 0))
        tk.Entry(parent, textvariable=variable, justify='center').pack()

    def start_animation(self):
        self.stop_animation()

        # Získání dat z UI
        m1, m2 = self.m1.get(), self.m2.get()
        l1, l2 = self.l1.get(), self.l2.get()
        th1_base = self.theta1_pi.get() * np.pi
        th2_base = self.theta2_pi.get() * np.pi

        # Přidání více kyvadel
        self.num_pendulums = 3
        colors = ['red', 'blue', 'green']

        self.all_x1 = []
        self.all_y1 = []
        self.all_x2 = []
        self.all_y2 = []

        # Smyčka, která spočítá trajektorii pro každé kyvadlo zvlášť
        for i in range(self.num_pendulums):
            # Každé další kyvadlo má úhel posunutý o nepatrných 0.001 rad
            state_0 = [th1_base + (i * 0.000), 0.0, th2_base, 0.0]

            x1, y1, x2, y2, self.t = DoublePendulumModel.simulate(
                state_0, t_max=30, dt=0.02, m1=m1, m2=m2, l1=l1, l2=l2
            )

            self.all_x1.append(x1)
            self.all_y1.append(y1)
            self.all_x2.append(x2)
            self.all_y2.append(y2)

        # Příprava os a grafiky
        self.ax.clear()
        max_len = l1 + l2
        self.ax.set_xlim(-max_len - 0.5, max_len + 0.5)
        self.ax.set_ylim(-max_len - 0.5, max_len + 0.5)
        self.ax.set_aspect('equal')
        self.ax.set_title("Motýlí efekt: 3 kyvadla s rozdílem 0.001 rad")
        self.ax.grid(True, linestyle='--', alpha=0.5)

        # Vytvoření grafických prvků pro každé kyvadlo
        self.lines = []
        self.traces = []

        for i in range(self.num_pendulums):
            line, = self.ax.plot([], [], 'o-', lw=2, color=colors[i], markersize=6)
            trace, = self.ax.plot([], [], '-', lw=1, color=colors[i], alpha=0.5)
            self.lines.append(line)
            self.traces.append(trace)

        # Spuštění animace
        self.ani = FuncAnimation(
            self.fig, self.update_frame, frames=len(self.t),
            interval=20, blit=True, repeat=False
        )
        self.is_running = True
        self.canvas.draw()

    def update_frame(self, i):
        history_len = 50  # delka čary za kyvadlem
        start_idx = max(0, i - history_len)

        # Aktualizace všech kyvadel najednou
        for p in range(self.num_pendulums):
            thisx = [0, self.all_x1[p][i], self.all_x2[p][i]]
            thisy = [0, self.all_y1[p][i], self.all_y2[p][i]]

            self.lines[p].set_data(thisx, thisy)
            self.traces[p].set_data(self.all_x2[p][start_idx:i], self.all_y2[p][start_idx:i])

        return self.lines + self.traces

    def stop_animation(self):
        if self.ani and self.is_running:
            self.ani.event_source.stop()
            self.is_running = False


if __name__ == "__main__":
    root = tk.Tk()
    app = DoublePendulumApp(root)
    root.mainloop()