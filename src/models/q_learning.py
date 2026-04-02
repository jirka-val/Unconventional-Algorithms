import numpy as np
import random


class QLearningModel:
    def __init__(self, rows, cols, actions=4):
        self.rows = rows
        self.cols = cols
        self.actions = actions  # 0: nahoru, 1: dolů, 2: vlevo, 3: vpravo
        # Q-tabulka: stav je (row * cols + col)
        self.q_table = np.zeros((rows * cols, actions))

        # Hyperparametry
        self.lr = 0.1  # Learning rate (alfa)
        self.discount = 0.95  # Discount factor (gamma)
        self.epsilon = 0.1  # Epsilon-greedy

    def get_state(self, r, c):
        return r * self.cols + c

    def choose_action(self, r, c, train=True):
        """Vybere akci na základě epsilon-greedy strategie."""
        if train and random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.actions - 1)
        return np.argmax(self.q_table[self.get_state(r, c)])

    def update(self, r, c, action, reward, next_r, next_c):
        """Q-learning vzorec: Q(s,a) = Q(s,a) + lr * [reward + gamma * max(Q(s',a')) - Q(s,a)]"""
        state = self.get_state(r, c)
        next_state = self.get_state(next_r, next_c)

        old_value = self.q_table[state, action]
        next_max = np.max(self.q_table[next_state])

        # Aktualizace hodnoty v tabulce
        new_value = old_value + self.lr * (reward + self.discount * next_max - old_value)
        self.q_table[state, action] = new_value