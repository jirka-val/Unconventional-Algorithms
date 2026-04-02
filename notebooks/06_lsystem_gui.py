import tkinter as tk
from tkinter import ttk
import numpy as np
import sys
import os

# Import modelu z tvé struktury
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.models.lsystem import LSystem


class LSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("L-systems drawing")

        # --- Levá část: Kreslicí plátno ---
        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        # --- Pravá část: Ovládací panel ---
        self.controls = tk.Frame(root)
        self.controls.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        # Vstupy (Starting X, Y, Angle, Nesting, Size)
        self.start_x = self.create_input("Starting X position (int)", "200")
        self.start_y = self.create_input("Starting Y position (int)", "200")
        self.start_angle = self.create_input("Starting angle (degree)", "0")
        self.nesting = self.create_input("The number of nesting (int)", "3")
        self.line_size = self.create_input("Size of the line (int)", "5")

        # Tlačítka pro předdefinované příklady (Draw first, second, atd.)
        tk.Button(self.controls, text="Draw first", bg="#90EE90", command=self.draw_first).pack(fill=tk.X, pady=2)
        tk.Button(self.controls, text="Draw second", bg="#90EE90", command=self.draw_second).pack(fill=tk.X, pady=2)
        tk.Button(self.controls, text="Draw third", bg="#90EE90", command=self.draw_third).pack(fill=tk.X, pady=2)
        tk.Button(self.controls, text="Draw fourth", bg="#90EE90", command=self.draw_fourth).pack(fill=tk.X, pady=2)

        # Vlastní nastavení (Custom)
        tk.Label(self.controls, text="Custom", font=('Arial', 10, 'bold')).pack(pady=5)
        self.custom_axiom = self.create_input("Axiom (F, +, -, [, ])", "F+F+F+F")
        self.custom_rule = self.create_input("Rule (F -> ...)", "F+F-F-FF+F+F-F")
        self.custom_angle = self.create_input("Angle (degree)", "90")

        tk.Button(self.controls, text="Draw custom", bg="#90EE90", command=self.draw_custom).pack(fill=tk.X, pady=5)
        tk.Button(self.controls, text="Clear canvas", bg="#FFCCCB", command=lambda: self.canvas.delete("all")).pack(
            fill=tk.X)

    def create_input(self, label_text, default_val):
        tk.Label(self.controls, text=label_text).pack(anchor=tk.W)
        entry = tk.Entry(self.controls)
        entry.insert(0, default_val)
        entry.pack(fill=tk.X, pady=2)
        return entry

    def draw_lsystem(self, lsystem, iterations):
        # Načtení parametrů
        x = float(self.start_x.get())
        y = float(self.start_y.get())
        angle = np.radians(float(self.start_angle.get()))
        size = float(self.line_size.get())
        angle_step = np.radians(lsystem.angle_degree)

        path = lsystem.generate_path(iterations)
        stack = []

        for cmd in path:
            if cmd == 'F':
                new_x = x + size * np.cos(angle)
                new_y = y - size * np.sin(angle)  # y jde v GUI dolů
                self.canvas.create_line(x, y, new_x, new_y)
                x, y = new_x, new_y
            elif cmd == '+':
                angle -= angle_step
            elif cmd == '-':
                angle += angle_step
            elif cmd == '[':
                stack.append((x, y, angle))
            elif cmd == ']':
                x, y, angle = stack.pop()

    # Metody pro tlačítka odpovídající zadání v PDF
    def draw_first(self):
        ls = LSystem("F+F+F+F", {"F": "F+F-F-FF+F+F-F"}, 90)
        self.draw_lsystem(ls, int(self.nesting.get()))

    def draw_second(self):
        ls = LSystem("F++F++F", {"F": "F+F--F+F"}, 60)
        self.draw_lsystem(ls, int(self.nesting.get()))

    def draw_third(self):
        ls = LSystem("F", {"F": "F[+F]F[-F]F"}, 25.7)  # pi/7
        self.draw_lsystem(ls, int(self.nesting.get()))

    def draw_fourth(self):
        ls = LSystem("F", {"F": "FF+[+F-F-F]-[-F+F+F]"}, 22.5)  # pi/8
        self.draw_lsystem(ls, int(self.nesting.get()))

    def draw_custom(self):
        # Logika pro parsování pravidla "F -> ..."
        raw_rule = self.custom_rule.get()
        rule_content = raw_rule.split("->")[-1].strip()
        ls = LSystem(self.custom_axiom.get(), {"F": rule_content}, float(self.custom_angle.get()))
        self.draw_lsystem(ls, int(self.nesting.get()))


if __name__ == "__main__":
    root = tk.Tk()
    app = LSystemApp(root)
    root.mainloop()