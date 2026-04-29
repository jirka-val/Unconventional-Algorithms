import tkinter as tk
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap

# Propojení se složkou src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.models.forest_fire import ForestFireModel


class ForestFireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cellular Automata: Forest Fire")
        self.root.geometry("1200x850")

        # Matplotlib Plátno pro vykreslování
        self.fig, self.ax = plt.subplots(figsize=(8, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- NOVÉ: Připojení události kliknutí myší na plátno ---
        self.canvas.mpl_connect('button_press_event', self.on_click)

        # Ovládací panel
        control_frame = tk.Frame(self.root, width=300)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=15, pady=10)

        # Definice parametrů s výchozími hodnotami z PDF
        self.p_prob = tk.DoubleVar(value=0.05)
        self.f_prob = tk.DoubleVar(value=0.001)
        self.density = tk.DoubleVar(value=0.5)
        self.grid_size = tk.IntVar(value=100)
        self.anim_speed = tk.IntVar(value=50)  # ms

        # Vstupy
        self.create_input(control_frame, "Grow Probability (p)", self.p_prob)
        self.create_input(control_frame, "Ignite Probability (f)", self.f_prob)
        self.create_input(control_frame, "Initial Forest Density", self.density)
        self.create_input(control_frame, "Grid Size (N)", self.grid_size)
        self.create_input(control_frame, "Animation Delay (ms)", self.anim_speed)

        # Akční tlačítka
        tk.Button(control_frame, text="1. Start Normal Simulation", command=self.start_animation, bg="#90EE90",
                  height=2).pack(pady=(25, 5), fill=tk.X)
        tk.Button(control_frame, text="2. Start MANUAL Mode", command=self.start_manual_mode, bg="#FFD700",
                  height=2).pack(pady=5, fill=tk.X)
        tk.Button(control_frame, text="Stop Animation", command=self.stop_animation, bg="#FFB6C1", height=2).pack(
            pady=5, fill=tk.X)

        # Instrukce pro uživatele
        tk.Label(control_frame, text="⚡ TIP: Click on the map\nto start a fire! ⚡", fg="red",
                 font=("Arial", 11, "bold")).pack(pady=15)

        self.ani = None
        self.grid = None

        # Nastavení barev pro matici: 0=Černá, 1=Zelená, 2=Červená
        self.cmap = ListedColormap(['black', 'green', 'red'])

    def create_input(self, parent, label_text, variable):
        tk.Label(parent, text=label_text).pack(pady=(5, 0))
        tk.Entry(parent, textvariable=variable, justify='center').pack()

    def start_animation(self):
        self.stop_animation()
        self.grid = ForestFireModel.initialize_grid(self.grid_size.get(), self.density.get())

        self.ax.clear()
        self.ax.set_title("Forest Fire Algorithm (Normal Mode)")
        self.im = self.ax.imshow(self.grid, cmap=self.cmap, vmin=0, vmax=2)

        self.ani = FuncAnimation(
            self.fig, self.update_frame,
            interval=self.anim_speed.get(),
            blit=False, cache_frame_data=False
        )
        self.canvas.draw()

    def start_manual_mode(self):
        """
        Spustí simulaci, kde zruší pravděpodobnost blesku,
        takže oheň může začít pouze kliknutím uživatele.
        """
        self.stop_animation()

        # Dočasně nastavíme blesk na 0
        self.f_prob.set(0.0)

        self.grid = ForestFireModel.initialize_grid(self.grid_size.get(), self.density.get())

        self.ax.clear()
        self.ax.set_title("Interactive Forest Fire (CLICK TO IGNITE!)", color="red")
        self.im = self.ax.imshow(self.grid, cmap=self.cmap, vmin=0, vmax=2)

        self.ani = FuncAnimation(
            self.fig, self.update_frame,
            interval=self.anim_speed.get(),
            blit=False, cache_frame_data=False
        )
        self.canvas.draw()

    def update_frame(self, frame):
        self.grid = ForestFireModel.step(self.grid, self.p_prob.get(), self.f_prob.get())
        self.im.set_data(self.grid)
        return [self.im]

    def on_click(self, event):
        """
        Zachytí kliknutí myši a vytvoří na daném místě oheň.
        """
        # Ignorujeme kliknutí mimo samotný graf nebo pokud ještě neběží simulace
        if event.inaxes != self.ax or self.grid is None:
            return

        # Převedeme X,Y myši na sloupce a řádky matice (zaokrouhlujeme na nejbližší políčko)
        col = int(round(event.xdata))
        row = int(round(event.ydata))

        # Ochrana proti indexu mimo pole
        if 0 <= row < self.grid_size.get() and 0 <= col < self.grid_size.get():
            # Zapálíme danou buňku (stav 2 = oheň)
            self.grid[row, col] = ForestFireModel.FIRE

            # Okamžitě překreslíme matici, aby oheň blikl ještě před dalším krokem animace
            self.im.set_data(self.grid)
            self.canvas.draw()

    def stop_animation(self):
        if self.ani:
            self.ani.event_source.stop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ForestFireApp(root)
    root.mainloop()