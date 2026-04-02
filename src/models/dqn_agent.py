import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
import os
from collections import deque

# Definice architektury neuronové sítě
class QNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(QNetwork, self).__init__()

        # Síť se dvěma skrytými vrstvami pro aproximaci Q-funkce
        self.fc = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim)
        )

    def forward(self, x):
        return self.fc(x)

class DQNAgent:
    def __init__(self, state_dim, action_dim):
        self.state_dim = state_dim
        self.action_dim = action_dim

        # Paměť pro ukládání předchozích zkušeností
        self.memory = deque(maxlen=2000)

        # Hyperparametry posilovaného učení
        self.gamma = 0.95  # váha budoucích odměn
        self.epsilon = 1.0  # Počáteční míra náhodného průzkumu
        self.epsilon_min = 0.01  # Minimální míra průzkumu
        self.epsilon_decay = 0.995  # Rychlost snižování náhody

        # Inicializace sítě, optimalizátoru a ztrátové funkce
        self.model = QNetwork(state_dim, action_dim)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()

    def select_action(self, state):
        """Výběr akce pomocí epsilon-greedy strategie."""
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_dim)

        # Predikce nejlepší akce pomocí neuronové sítě
        state_t = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            return torch.argmax(self.model(state_t)).item()

    def remember(self, state, action, reward, next_state, done):
        """Uložení kroku simulace do paměti."""
        self.memory.append((state, action, reward, next_state, done))

    def train(self, batch_size):
        """Trénink sítě na náhodném vzorku z paměti """
        if len(self.memory) < batch_size: return
        minibatch = random.sample(self.memory, batch_size)

        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                next_t = torch.FloatTensor(next_state).unsqueeze(0)
                target = reward + self.gamma * torch.max(self.model(next_t)).item()

            # Získání aktuální predikce a úprava hodnoty pro provedenou akci
            state_t = torch.FloatTensor(state).unsqueeze(0)
            target_f = self.model(state_t)
            target_f[0][action] = target

            # Zpětná propagace a aktualizace vah sítě
            self.optimizer.zero_grad()
            loss = self.criterion(self.model(state_t), target_f)
            loss.backward()
            self.optimizer.step()

        # Postupné snižování epsilon pro přechod od průzkumu k využití znalostí
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay