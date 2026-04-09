import numpy as np
import random


class IFSModel:
    def __init__(self, transformations):
        """
        Inicializuje IFS model se seznamem transformací.
        Každá transformace je slovník s klíči 'a' až 'l'.
        """
        self.transformations = transformations
        self.history = []

    def generate(self, iterations=20000):
        """
        Generuje body fraktálu v 3D prostoru[cite: 63].
        Každá transformace má stejnou pravděpodobnost p=0.25.
        """
        self.history = []
        current_point = np.array([0.0, 0.0, 0.0])

        # Iterativní generování bodů
        for _ in range(iterations):
            # Výběr náhodné transformace
            t = random.choice(self.transformations)

            x, y, z = current_point

            # Afinní transformace pro 3D prostor:
            # x' = ax + by + cz + j
            # y' = dx + ey + fz + k
            # z' = gx + hy + iz + l
            new_x = t['a'] * x + t['b'] * y + t['c'] * z + t['j']
            new_y = t['d'] * x + t['e'] * y + t['f'] * z + t['k']
            new_z = t['g'] * x + t['h'] * y + t['i'] * z + t['l']

            current_point = np.array([new_x, new_y, new_z])
            self.history.append(current_point)

        return np.array(self.history)