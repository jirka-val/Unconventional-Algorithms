import tkinter as tk
from tkinter import messagebox
import numpy as np
import os
from src.models.q_learning import QLearningModel


class QLearningApp:
    def __init__(self, root, rows=10, cols=10):
        self.root = root
        self.root.title("Task 4 - Q-Learning: Find the Cheese")
        self.rows, self.cols = rows, cols
        self.cell_size = 40

        self.model = QLearningModel(rows, cols)
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.mouse_pos = [0, 0]
        self.start_pos = [0, 0]

        self.training_in_progress = False
        self.demo_in_progress = False
        self.current_episode = 0
        self.max_episodes = 300

        # Načtení ikon
        self.icons = {}
        self.load_assets()

        self.setup_ui()

    def load_assets(self):
        """Načte a zmenší obrázky tak, aby se přesně vešly do políčka."""
        current_dir = os.path.dirname(__file__)
        asset_path = os.path.abspath(os.path.join(current_dir, "..", "src", "utils", "assets"))

        icon_files = {
            'M': "mouse.png",
            'C': "cheese.png",
            'T': "trap.png",
            'W': "wall.png"
        }

        for key, filename in icon_files.items():
            full_path = os.path.join(asset_path, filename)
            if os.path.exists(full_path):
                try:
                    img = tk.PhotoImage(file=full_path)
                    width = img.width()
                    height = img.height()

                    ratio_x = width // self.cell_size
                    ratio_y = height // self.cell_size

                    if ratio_x > 1 or ratio_y > 1:
                        self.icons[key] = img.subsample(ratio_x, ratio_y)
                    else:
                        self.icons[key] = img

                except Exception as e:
                    print(f"Chyba při načítání {filename}: {e}")
                    self.icons[key] = None
            else:
                print(f"Soubor nenalezen: {full_path}")
                self.icons[key] = None

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=self.cols * self.cell_size,
                                height=self.rows * self.cell_size, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_click)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(side=tk.RIGHT, padx=10, fill="y")

        tk.Label(btn_frame, text="Editor Mode", font=("Arial", 10, "bold")).pack(pady=5)
        self.mode = tk.StringVar(value="Wall")
        for m in ["Mouse", "Trap", "Wall", "Cheese"]:
            tk.Radiobutton(btn_frame, text=f"Select {m}", variable=self.mode, value=m).pack(anchor="w")

        tk.Label(btn_frame, text="Animation Delay (ms)", font=("Arial", 8)).pack(pady=(10, 0))
        self.speed_slider = tk.Scale(btn_frame, from_=0, to=100, orient=tk.HORIZONTAL)
        self.speed_slider.set(5)
        self.speed_slider.pack(fill="x")

        self.info_label = tk.Label(btn_frame, text="Episode: 0", font=("Arial", 10, "bold"), fg="blue")
        self.info_label.pack(pady=10)

        self.btn_train = tk.Button(btn_frame, text="Start Learning", bg="#90ee90", command=self.start_animated_train)
        self.btn_train.pack(fill="x", pady=2)

        self.btn_stop = tk.Button(btn_frame, text="STOP", bg="#ff9999", command=self.stop_all, state=tk.DISABLED)
        self.btn_stop.pack(fill="x", pady=2)

        self.btn_demo = tk.Button(btn_frame, text="Find the Cheese!", bg="#add8e6", command=self.run_demo)
        self.btn_demo.pack(fill="x", pady=2)

        tk.Button(btn_frame, text="Reset Q-Table", command=self.reset_brain).pack(fill="x", pady=(10, 0))
        tk.Button(btn_frame, text="Clear Grid", command=self.clear).pack(fill="x", pady=2)

        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                content = self.grid[r][c]
                state = r * self.cols + c
                max_q = np.max(self.model.q_table[state])

                # Heatmapa zůstává pro přehlednost
                color = "white"
                if max_q > 0 and content is None:
                    color = "#e6ffed"
                elif max_q < 0 and content is None:
                    color = "#fff0f0"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#eee")

                # Kreslení IKONY nebo TEXTU
                obj_key = None
                if [r, c] == self.mouse_pos:
                    obj_key = 'M'
                elif content == 'W':
                    obj_key = 'W'
                elif content == 'T':
                    obj_key = 'T'
                elif content == 'C':
                    obj_key = 'C'

                if obj_key:
                    if self.icons.get(obj_key):
                        # Vykreslení obrázku doprostřed buňky
                        self.canvas.create_image(x1 + 20, y1 + 20, image=self.icons[obj_key])
                    else:
                        # Záložní text, pokud obrázek chybí
                        text_colors = {'M': "#87CEFA", 'W': "#555", 'T': "red", 'C': "orange"}
                        self.canvas.create_text(x1 + 20, y1 + 20, text=obj_key,
                                                fill=text_colors.get(obj_key, "black"), font=("Arial", 12, "bold"))

    def stop_all(self):
        self.training_in_progress = False
        self.demo_in_progress = False
        self.btn_stop.config(state=tk.DISABLED)
        self.btn_train.config(state=tk.NORMAL)
        self.btn_demo.config(state=tk.NORMAL)

    def start_animated_train(self):
        if not self.validate_map(): return
        self.training_in_progress = True
        self.btn_stop.config(state=tk.NORMAL)
        self.btn_train.config(state=tk.DISABLED)
        self.current_episode = 0
        self.mouse_pos = list(self.start_pos)
        self.train_step()

    def train_step(self):
        if not self.training_in_progress: return

        r, c = self.mouse_pos
        action = self.model.choose_action(r, c)
        nr, nc, reward = self.move_mouse(action)

        self.model.update(r, c, action, reward, nr, nc)
        self.mouse_pos = [nr, nc]

        if self.current_episode % 2 == 0 or self.speed_slider.get() > 10:
            self.draw()

        if self.grid[nr][nc] in ['C', 'T']:
            self.current_episode += 1
            self.info_label.config(text=f"Episode: {self.current_episode}")
            if self.current_episode < self.max_episodes and self.training_in_progress:
                self.mouse_pos = list(self.start_pos)
                self.root.after(1, self.train_step)
            else:
                self.stop_all()
        else:
            self.root.after(self.speed_slider.get(), self.train_step)

    def move_mouse(self, action):
        r, c = self.mouse_pos
        nr, nc = r, c
        if action == 0 and r > 0:
            nr -= 1
        elif action == 1 and r < self.rows - 1:
            nr += 1
        elif action == 2 and c > 0:
            nc -= 1
        elif action == 3 and c < self.cols - 1:
            nc += 1

        if self.grid[nr][nc] == 'W': return r, c, -2
        if self.grid[nr][nc] == 'C': return nr, nc, 100
        if self.grid[nr][nc] == 'T': return nr, nc, -100
        return nr, nc, -0.1

    def run_demo(self):
        if not self.validate_map(): return
        self.demo_in_progress = True
        self.btn_stop.config(state=tk.NORMAL)
        self.mouse_pos = list(self.start_pos)
        self.animate_demo()

    def animate_demo(self):
        if not self.demo_in_progress: return
        r, c = self.mouse_pos
        if self.grid[r][c] in ['C', 'T']:
            self.stop_all()
            return

        action = self.model.choose_action(r, c, train=False)
        nr, nc, _ = self.move_mouse(action)
        self.mouse_pos = [nr, nc]
        self.draw()
        self.root.after(150, self.animate_demo)

    def on_click(self, event):
        if self.training_in_progress or self.demo_in_progress: return
        c, r = event.x // self.cell_size, event.y // self.cell_size
        if not (0 <= r < self.rows and 0 <= c < self.cols): return
        m = self.mode.get()
        if m == "Mouse":
            self.start_pos = [r, c]
            self.mouse_pos = [r, c]
        else:
            char = m[0]
            self.grid[r][c] = char if self.grid[r][c] != char else None
        self.draw()

    def validate_map(self):
        flat_grid = [item for sublist in self.grid for item in sublist]
        if 'C' not in flat_grid:
            messagebox.showerror("Error", "No Cheese on map!")
            return False
        return True

    def reset_brain(self):
        self.model.q_table.fill(0)
        self.current_episode = 0
        self.draw()

    def clear(self):
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = QLearningApp(root)
    root.mainloop()