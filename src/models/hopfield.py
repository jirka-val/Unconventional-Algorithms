import numpy as np


class HopfieldNetwork:
    def __init__(self, n_neurons):
        self.n_neurons = n_neurons
        # Inicializace matice vah W nulami
        self.weights = np.zeros((n_neurons, n_neurons))

    def train(self, patterns):
        """Učení pomocí skalárního součinu"""
        for p in patterns:
            p = p.flatten()
            # W = M^T * M
            self.weights += np.outer(p, p)

        # Nastavení diagonály na nulu (W = W - I)
        np.fill_diagonal(self.weights, 0)

    def predict_sync(self, pattern):
        """Synchronní obnova: V_i = sgn(sum(W_ij * V_j))"""
        v = pattern.flatten()
        new_v = np.sign(np.dot(self.weights, v))
        # Pokud je výsledek 0, nastavíme na 1
        new_v[new_v == 0] = 1
        return new_v.reshape(pattern.shape)

    def predict_async(self, pattern):
        """Asynchronní obnova: aktualizace neuronů po jednom."""
        v = pattern.flatten().astype(float)
        indices = np.arange(self.n_neurons)
        np.random.shuffle(indices)  # Náhodné pořadí pro asynchronní režim

        for i in indices:
            # Výpočet pro konkrétní neuron
            activation = np.dot(self.weights[i], v)
            v[i] = 1 if activation >= 0 else -1

        return v.reshape(pattern.shape)