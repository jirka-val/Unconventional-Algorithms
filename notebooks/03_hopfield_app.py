import tkinter as tk
from tkinter import messagebox, ttk
from src.models.hopfield import HopfieldNetwork
import numpy as np


class App:
    def __init__(self, root, size=10):
        self.size = size
        self.model = HopfieldNetwork(size * size)
        self.grid = np.full((size, size), -1)
        self.saved_patterns = []  # Seznam pro vizuální správu vzorů

        self.root = root
        self.root.title("Advanced Hopfield Manager")

        # --- ROZVRŽENÍ ---
        # Levý panel: Kreslení
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.canvas = tk.Canvas(self.main_frame, width=300, height=300, bg="white", highlightthickness=1,
                                highlightbackground="black")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click)

        # Střední panel: Ovládání
        self.ctrl_frame = tk.Frame(root)
        self.ctrl_frame.pack(side=tk.LEFT, padx=10, fill="y")

        tk.Label(self.ctrl_frame, text="Operations", font=('Arial', 10, 'bold')).pack(pady=5)
        tk.Button(self.ctrl_frame, text="Save pattern", bg="#90ee90", command=self.save, width=20).pack(pady=2)
        tk.Button(self.ctrl_frame, text="Repair Sync", bg="#fffacd", command=self.sync, width=20).pack(pady=2)
        tk.Button(self.ctrl_frame, text="Repair Async", bg="#fffacd", command=self.async_rep, width=20).pack(pady=2)
        tk.Button(self.ctrl_frame, text="Clear grid", bg="#ffcccb", command=self.clear, width=20).pack(pady=10)

        self.stats_label = tk.Label(self.ctrl_frame, text="Stored: 0/5", fg="blue")
        self.stats_label.pack()

        # Pravý panel: Seznam uložených vzorů (Sidebar)
        self.side_frame = tk.Frame(root, bg="#f0f0f0", width=150)
        self.side_frame.pack(side=tk.RIGHT, fill="y", padx=5)
        tk.Label(self.side_frame, text="Stored Memory", bg="#f0f0f0").pack()

        self.pattern_listbox = tk.Listbox(self.side_frame, height=15)
        self.pattern_listbox.pack(padx=5, pady=5)
        tk.Button(self.side_frame, text="Inspect Pattern", command=self.inspect_pattern).pack(fill="x", padx=5)

        self.draw()

    def draw(self):
        self.canvas.delete("all")
        cell = 300 // self.size
        for r in range(self.size):
            for c in range(self.size):
                color = "black" if self.grid[r, c] == 1 else "white"
                self.canvas.create_rectangle(c * cell, r * cell, (c + 1) * cell, (r + 1) * cell, fill=color,
                                             outline="#eee")

    def click(self, event):
        cell_w = 300 // self.size
        c, r = event.x // cell_w, event.y // cell_w
        if 0 <= r < self.size and 0 <= c < self.size:
            self.grid[r, c] *= -1
            self.draw()

    def save(self):
        # Přidání do logiky sítě
        self.model.train([self.grid])
        # Uložení pro GUI
        self.saved_patterns.append(self.grid.copy())
        self.pattern_listbox.insert(tk.END, f"Pattern {len(self.saved_patterns)}")
        self.stats_label.config(text=f"Stored: {len(self.saved_patterns)}/5")

        if len(self.saved_patterns) > 5:
            messagebox.showwarning("Warning", "Exceeded recommended capacity (5)!")
        self.clear()

    def inspect_pattern(self):
        """Otevře okno s detaily vzoru, jak je na tvém novém obrázku."""
        selection = self.pattern_listbox.curselection()
        if not selection:
            return

        idx = selection[0]
        pattern = self.saved_patterns[idx]

        inspect_win = tk.Toplevel(self.root)
        inspect_win.title(f"Detail: Pattern {idx + 1}")

        # Náhled vzoru
        sub_canvas = tk.Canvas(inspect_win, width=200, height=200, bg="white")
        sub_canvas.pack(side=tk.LEFT, padx=10, pady=10)
        cell = 200 // self.size
        for r in range(self.size):
            for c in range(self.size):
                color = "black" if pattern[r, c] == 1 else "white"
                sub_canvas.create_rectangle(c * cell, r * cell, (c + 1) * cell, (r + 1) * cell, fill=color)

        # Tlačítka podle tvého obrázku [cite: 33, 35, 36, 38]
        btn_p = tk.Frame(inspect_win)
        btn_p.pack(side=tk.RIGHT, padx=10)
        tk.Button(btn_p, text="Show matrix", command=lambda: print(pattern)).pack(fill="x")
        tk.Button(btn_p, text="Show vector", command=lambda: print(pattern.flatten())).pack(fill="x")
        tk.Button(btn_p, text="Forget pattern", bg="#ffcccb", command=lambda: self.forget(idx, inspect_win)).pack(
            fill="x", pady=10)

    def forget(self, idx, window):
        # Poznámka: Hopfieldova síť neumí jen tak "zapomenout" jeden vzor z matice vah bez přepočítání všech
        self.saved_patterns.pop(idx)
        self.pattern_listbox.delete(idx)
        # Resetujeme síť a naučíme ji zbývající vzory znovu
        self.model.weights = np.zeros((self.size * self.size, self.size * self.size))
        self.model.train(self.saved_patterns)
        self.stats_label.config(text=f"Stored: {len(self.saved_patterns)}/5")
        window.destroy()

    def sync(self):
        self.grid = self.model.predict_sync(self.grid)
        self.draw()

    def async_rep(self):
        self.grid = self.model.predict_async(self.grid)
        self.draw()

    def clear(self):
        self.grid = np.full((self.size, self.size), -1)
        self.draw()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()