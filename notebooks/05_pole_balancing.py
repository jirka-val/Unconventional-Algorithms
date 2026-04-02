import tkinter as tk
from tkinter import ttk
import threading
import gymnasium as gym
import numpy as np
from src.models.dqn_agent import DQNAgent
import warnings

# Skrytí upozornění na zastaralé verze knihovny Pygame
warnings.filterwarnings("ignore", category=UserWarning)

class CartPoleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task 5 - DQN Learning Dashboard")
        self.root.geometry("450x700")

        self.running = False
        self.agent = None
        self.scores_history = []

        self.setup_ui()

    def setup_ui(self):
        main_container = tk.Frame(self.root, padx=20, pady=10)
        main_container.pack(expand=True, fill="both")

        tk.Label(main_container, text="DQN CartPole Learning", font=('Arial', 14, 'bold')).pack(pady=10)

        # Nastavení parametrů pro DQN algoritmus
        param_frame = tk.LabelFrame(main_container, text=" Settings ", padx=10, pady=10)
        param_frame.pack(fill="x", pady=5)

        tk.Label(param_frame, text="Learning Rate (Epsilon Decay):").pack(anchor="w")
        self.decay_slider = tk.Scale(param_frame, from_=0.980, to=0.999, resolution=0.001, orient=tk.HORIZONTAL)
        self.decay_slider.set(0.995)
        self.decay_slider.pack(fill="x")

        tk.Label(param_frame, text="Max Episodes:").pack(anchor="w", pady=(5, 0))
        self.episodes_spin = tk.Spinbox(param_frame, from_=10, to=500, increment=10)
        self.episodes_spin.delete(0, "end")
        self.episodes_spin.insert(0, "100")
        self.episodes_spin.pack(fill="x")

        # Příprava plochy pro vykreslování grafu úspěšnosti
        graph_frame = tk.LabelFrame(main_container, text=" Learning Chart (Score per Episode) ", padx=5, pady=5)
        graph_frame.pack(fill="x", pady=5)

        self.graph_canvas = tk.Canvas(graph_frame, width=380, height=150, bg="#fdfdfd", highlightthickness=1)
        self.graph_canvas.pack(pady=5)
        self.graph_canvas.create_text(190, 75, text="Chart will appear during training", fill="#ccc")

        # Ukazatele stavu a průběhu učení
        monitor_frame = tk.Frame(main_container)
        monitor_frame.pack(fill="x", pady=5)

        self.status_var = tk.StringVar(value="Status: Ready")
        tk.Label(monitor_frame, textvariable=self.status_var, font=('Consolas', 10, 'bold'), fg="blue").pack()

        self.progress = ttk.Progressbar(monitor_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progress.pack(fill="x", pady=5)

        # Ovládací tlačítka aplikace
        ctrl_frame = tk.Frame(main_container)
        ctrl_frame.pack(fill="x", pady=10)

        self.btn_train = tk.Button(ctrl_frame, text="START TRAINING & VISUALIZE", bg="#90ee90",
                                   font=('Arial', 10, 'bold'), command=self.start_training)
        self.btn_train.pack(fill="x", pady=2)

        self.btn_stop = tk.Button(ctrl_frame, text="STOP SIMULATION", bg="#ff9999",
                                  command=self.stop, state=tk.DISABLED)
        self.btn_stop.pack(fill="x", pady=5)

    def draw_chart(self):
        """Přepočítá body a vykreslí spojitou čáru skóre do plátna."""
        self.graph_canvas.delete("all")
        if not self.scores_history:
            return

        w, h = 380, 150
        max_score = 500
        padding = 10

        self.graph_canvas.create_line(padding, h - padding, w - padding, h - padding, fill="#999")
        self.graph_canvas.create_line(padding, padding, padding, h - padding, fill="#999")

        if len(self.scores_history) < 2:
            return

        points = []
        for i, score in enumerate(self.scores_history):
            x = padding + (i / (max(len(self.scores_history) - 1, 1))) * (w - 2 * padding)
            y = (h - padding) - (score / max_score) * (h - 2 * padding)
            points.append((x, y))

        for i in range(len(points) - 1):
            self.graph_canvas.create_line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1],
                                          fill="#2ecc71", width=2)

    def stop(self):
        self.running = False
        self.status_var.set("Status: Stopping...")

    def start_training(self):
        """Spustí trénovací smyčku v samostatném vlákně pro plynulost GUI."""
        if not self.running:
            self.running = True
            self.scores_history = []
            self.btn_train.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            threading.Thread(target=self.training_loop, daemon=True).start()

    def training_loop(self):
        # Inicializace fyzikálního prostředí CartPole s vizualizací
        env = gym.make("CartPole-v1", render_mode="human")
        state_dim = env.observation_space.shape[0]
        action_dim = env.action_space.n

        self.agent = DQNAgent(state_dim, action_dim)
        self.agent.epsilon_decay = float(self.decay_slider.get())
        max_episodes = int(self.episodes_spin.get())

        for e in range(max_episodes):
            if not self.running: break

            state, _ = env.reset()
            score = 0
            self.progress['value'] = (e / max_episodes) * 1000

            for _ in range(500):
                if not self.running: break

                # Agent vybere akci a provede krok v simulaci
                action = self.agent.select_action(state)
                next_state, reward, term, trunc, _ = env.step(action)
                done = term or trunc

                # Úprava odměny pro rychlejší učení
                adj_reward = reward if not done else -10
                self.agent.remember(state, int(action), adj_reward, next_state, done)

                state = next_state
                score += 1
                self.agent.train(32) # Učení neuronové sítě na vzorku dat
                if done: break

            # Uložení výsledku a aktualizace grafu v hlavním vlákně
            self.scores_history.append(score)
            self.root.after(0, self.draw_chart)
            self.status_var.set(f"Ep: {e + 1}/{max_episodes} | Last Score: {score}")

            if score >= 5000:
                self.status_var.set("Status: Goal Reached!")
                break

        env.close()
        self.root.after(0, self.reset_ui)

    def reset_ui(self):
        self.running = False
        self.btn_train.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.progress['value'] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = CartPoleApp(root)
    root.mainloop()