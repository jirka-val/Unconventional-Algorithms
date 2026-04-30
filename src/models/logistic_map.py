import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class LogisticNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x)

class LogisticMapModel:
    @staticmethod
    def generate_data(a_min, a_max, n_samples, n_iterations, n_transients):
        a = np.linspace(a_min, a_max, n_samples)
        x = np.random.rand(n_samples)

        for _ in range(n_transients):
            x = a * x * (1 - x)

        a_out = []
        x_out = []

        for _ in range(n_iterations):
            x = a * x * (1 - x)
            a_out.extend(a)
            x_out.extend(x)

        return np.array(a_out), np.array(x_out)

    @staticmethod
    def train_nn(epochs=10000):
        # Generování trénovacích dat
        a = np.random.uniform(0, 4.0, 10000)
        x = np.random.uniform(0, 1.0, 10000)
        y = a * x * (1 - x)

        inputs = np.column_stack((a, x))
        targets = y.reshape(-1, 1)

        inputs_tensor = torch.tensor(inputs, dtype=torch.float32)
        targets_tensor = torch.tensor(targets, dtype=torch.float32)

        model = LogisticNet()
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.01)

        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = model(inputs_tensor)
            loss = criterion(outputs, targets_tensor)
            loss.backward()
            optimizer.step()

        return model

    @staticmethod
    def predict_bifurcation(model, a_actual, x_actual):

        model.eval()
        with torch.no_grad():
            inputs = torch.tensor(np.column_stack((a_actual, x_actual)), dtype=torch.float32)
            predicted_x = model(inputs).numpy().flatten()

        return a_actual, predicted_x