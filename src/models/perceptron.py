import numpy as np

class Perceptron:
    def __init__(self, input_size, lr=0.1, epochs=100):
        # Inicializace vah
        self.weights = np.random.randn(input_size + 1) * 0.01
        self.lr = lr
        self.epochs = epochs

    def activation(self, x):
        # Signum funkce: 1 pokud x >= 0, jinak -1
        return 1 if x >= 0 else -1

    def predict(self, x):
        # Výpočet dot productu vstupů a vah
        z = np.dot(x, self.weights[1:]) + self.weights[0]
        return self.activation(z)

    def train(self, X, y):
        for _ in range(self.epochs):
            for inputs, label in zip(X, y):
                prediction = self.predict(inputs)
                # Pokud je předpověď špatná, upravíme váhy
                if prediction != label:
                    update = self.lr * (label - prediction)
                    self.weights[1:] += update * inputs
                    self.weights[0] += update # Update biasu