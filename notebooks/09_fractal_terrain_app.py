import tkinter as tk
from tkinter import colorchooser
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.models.fractalTerrain import FractalTerrain


class FractalTerrainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FractalTerrain 2D by Michael Machů")
        self.root.geometry("1200x850")

        # Plátno pro vykreslování
        self.canvas = tk.Canvas(self.root, bg="white", width=901, height=800)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Pravý panel s ovládacími prvky
        control_frame = tk.Frame(self.root, width=300)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=15, pady=10)

        # Definice proměnných pro parametry
        self.start_x = tk.DoubleVar(value=0.0)
        self.start_y = tk.DoubleVar(value=450.5)
        self.end_x = tk.DoubleVar(value=901.0)
        self.end_y = tk.DoubleVar(value=450.5)
        self.iterations = tk.IntVar(value=8)
        self.offset = tk.DoubleVar(value=10.0)
        self.selected_color = "#000000"

        # Vytvoření vstupních polí
        self.create_input(control_frame, "Start X position (float)", self.start_x)
        self.create_input(control_frame, "Start Y position (float)", self.start_y)
        self.create_input(control_frame, "End X position (float)", self.end_x)
        self.create_input(control_frame, "End Y position (float)", self.end_y)
        self.create_input(control_frame, "The number of iteration (int)", self.iterations)
        self.create_input(control_frame, "Offset size (float)", self.offset)

        # Sekce pro výběr barvy
        self.color_label = tk.Label(control_frame, text=f"Selected color is {self.selected_color}")
        self.color_label.pack(pady=(15, 0))
        self.color_display = tk.Frame(control_frame, bg=self.selected_color, width=100, height=20)
        self.color_display.pack(pady=5)
        tk.Button(control_frame, text="Pick a color", command=self.pick_color, bg="#FFF8DC").pack()

        # Tlačítka pro načtení příkladů
        tk.Label(control_frame, text="Example Presets", font=("Arial", 10, "bold")).pack(pady=(25, 5))
        presets_frame = tk.Frame(control_frame)
        presets_frame.pack()

        tk.Button(presets_frame, text="Example 1", width=10, command=lambda: self.load_example(1)).grid(row=0, column=0,
                                                                                                        padx=2, pady=2)
        tk.Button(presets_frame, text="Example 2", width=10, command=lambda: self.load_example(2)).grid(row=0, column=1,
                                                                                                        padx=2, pady=2)
        tk.Button(presets_frame, text="Example 3", width=10, command=lambda: self.load_example(3)).grid(row=1, column=0,
                                                                                                        padx=2, pady=2)
        tk.Button(presets_frame, text="Example 4", width=10, command=lambda: self.load_example(4)).grid(row=1, column=1,
                                                                                                        padx=2, pady=2)

        # Hlavní akční tlačítka
        tk.Button(control_frame, text="Draw", command=self.draw_terrain, bg="#90EE90", width=15, height=2).pack(pady=(30, 10))
        tk.Button(control_frame, text="Clear canvas", command=self.clear_canvas, bg="#FFB6C1", width=15).pack()

    def load_example(self, ex_num):
        """Načte hodnoty parametrů podle screenshotů v zadání."""
        presets = {
            1: {"sy": 450.5, "ey": 450.5, "iter": 8, "off": 10.0, "col": "#000000"},  #
            2: {"sy": 200.0, "ey": 450.5, "iter": 10, "off": 10.0, "col": "#008000"},  #
            3: {"sy": 550.0, "ey": 550.0, "iter": 5, "off": 10.0, "col": "#000000"},  #
            4: {"sy": 700.0, "ey": 700.0, "iter": 4, "off": 10.0, "col": "#804000"}  #
        }

        p = presets[ex_num]
        self.start_y.set(p["sy"])
        self.end_y.set(p["ey"])
        self.iterations.set(p["iter"])
        self.offset.set(p["off"])
        self.selected_color = p["col"]

        # Aktualizace UI prvků pro barvu
        self.color_label.config(text=f"Selected color is {self.selected_color}")
        self.color_display.config(bg=self.selected_color)

    def create_input(self, parent, label_text, variable):
        tk.Label(parent, text=label_text).pack(pady=(5, 0))
        tk.Entry(parent, textvariable=variable, justify='center').pack()

    def pick_color(self):
        color = colorchooser.askcolor(title="Pick a color")
        if color[1]:
            self.selected_color = color[1]
            self.color_label.config(text=f"Selected color is {self.selected_color}")
            self.color_display.config(bg=self.selected_color)

    def draw_terrain(self):
        points = FractalTerrain.generate_2d_terrain(
            self.start_x.get(), self.start_y.get(),
            self.end_x.get(), self.end_y.get(),
            self.iterations.get(), self.offset.get()
        )
        # Uzavření polygonu pro výplň barvou směrem dolů
        canvas_height = 1000
        polygon_points = points + [(self.end_x.get(), canvas_height), (self.start_x.get(), canvas_height)]
        flat_coords = [coord for pt in polygon_points for coord in pt]
        self.canvas.create_polygon(flat_coords, fill=self.selected_color, outline=self.selected_color)

    def clear_canvas(self):
        self.canvas.delete("all")


if __name__ == "__main__":
    root = tk.Tk()
    app = FractalTerrainApp(root)
    root.mainloop()