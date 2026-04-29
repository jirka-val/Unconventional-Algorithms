import tkinter as tk
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Propojení se složkou src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.models.logistic_map import LogisticMapModel


class LogisticMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chaos Theory: Logistic Map Prediction")
        self.root.geometry("1200x850")

        # Matplotlib Plátno pro vykreslování
        self.fig, self.ax = plt.subplots(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Pravý panel s ovládacími prvky
        control_frame = tk.Frame(self.root, width=300)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=15, pady=10)

        # Definice proměnných pro parametry
        self.a_min = tk.DoubleVar(value=0.0)
        self.a_max = tk.DoubleVar(value=4.0)
        self.samples = tk.IntVar(value=1000)
        self.iterations = tk.IntVar(value=100)
        self.transients = tk.IntVar(value=200)

        # Vytvoření vstupních polí
        self.create_input(control_frame, "Parameter 'a' Min", self.a_min)
        self.create_input(control_frame, "Parameter 'a' Max", self.a_max)
        self.create_input(control_frame, "Number of Samples", self.samples)
        self.create_input(control_frame, "Plot Iterations", self.iterations)
        self.create_input(control_frame, "Transient Iterations", self.transients)

        self.nn_model = None

        # Hlavní akční tlačítka
        tk.Button(control_frame, text="1. Draw Actual Bifurcation", command=self.draw_actual, bg="#90EE90",
                  height=2).pack(pady=(30, 5), fill=tk.X)
        tk.Button(control_frame, text="2. Train Neural Network", command=self.train_nn, bg="#FFD700", height=2).pack(
            pady=5, fill=tk.X)
        tk.Button(control_frame, text="3. Draw Predicted Bifurcation", command=self.draw_predicted, bg="#87CEFA",
                  height=2).pack(pady=5, fill=tk.X)
        tk.Button(control_frame, text="Clear Canvas", command=self.clear_canvas, bg="#FFB6C1").pack(pady=(20, 5),
                                                                                                    fill=tk.X)

        self.status_label = tk.Label(control_frame, text="Status: Ready", fg="blue", font=("Arial", 10, "bold"))
        self.status_label.pack(pady=15)

    def create_input(self, parent, label_text, variable):
        tk.Label(parent, text=label_text).pack(pady=(5, 0))
        tk.Entry(parent, textvariable=variable, justify='center').pack()

    def draw_actual(self):
        self.status_label.config(text="Status: Generating map...")
        self.root.update()

        a, x = LogisticMapModel.generate_data(
            self.a_min.get(), self.a_max.get(), self.samples.get(),
            self.iterations.get(), self.transients.get()
        )

        self.ax.clear()
        self.ax.scatter(a, x, s=0.1, color='black', alpha=0.5, label="Actual")
        self.ax.set_title("Bifurcation Diagram")
        self.ax.set_xlabel("Parameter (a)")
        self.ax.set_ylabel("Population")
        self.ax.set_xlim(self.a_min.get(), self.a_max.get())
        self.ax.set_ylim(-0.05, 1.05)
        self.ax.legend(loc="upper left")
        self.canvas.draw()
        self.status_label.config(text="Status: Ready")

    def train_nn(self):
        self.status_label.config(text="Status: Training NN (Wait a few sec)...")
        self.root.update()

        self.nn_model = LogisticMapModel.train_nn(epochs=1000)

        self.status_label.config(text="Status: Neural Network Trained!")

    def draw_predicted(self):
        if self.nn_model is None:
            self.status_label.config(text="Status: ERROR - Train NN first!", fg="red")
            return

        self.status_label.config(text="Status: Predicting point-by-point...", fg="blue")
        self.root.update()

        # Vygenerujeme si nejprve data pro aktuální vstupy
        a_actual, x_actual = LogisticMapModel.generate_data(
            self.a_min.get(), self.a_max.get(), self.samples.get(),
            self.iterations.get(), self.transients.get()
        )

        a_pred, x_pred = LogisticMapModel.predict_bifurcation(self.nn_model, a_actual, x_actual)

        self.ax.clear()
        self.ax.scatter(a_actual, x_actual, s=0.2, color='black', alpha=0.5, label="Actual")
        self.ax.scatter(a_pred, x_pred, s=0.2, color='red', alpha=0.5, label="Predicted")

        self.ax.set_title("Bifurcation Diagram with Predictions")
        self.ax.set_xlabel("Parameter (a)")
        self.ax.set_ylabel("Population")
        self.ax.set_xlim(self.a_min.get(), self.a_max.get())
        self.ax.set_ylim(-0.05, 1.05)

        # Zabráníme duplikaci v legendě
        handles, labels = self.ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        self.ax.legend(by_label.values(), by_label.keys(), loc="upper left")

        self.canvas.draw()
        self.status_label.config(text="Status: Ready")

    def clear_canvas(self):
        self.ax.clear()
        self.canvas.draw()
        self.status_label.config(text="Status: Ready", fg="blue")


if __name__ == "__main__":
    root = tk.Tk()
    app = LogisticMapApp(root)
    root.mainloop()