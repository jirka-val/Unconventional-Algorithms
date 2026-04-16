import numpy as np


class FractalModel:
    def __init__(self, width=800, height=800, max_iter=100):
        self.width = width
        self.height = height
        self.max_iter = max_iter

    def generate_mandelbrot(self, x_min=-2.0, x_max=1.0, y_min=-1.0, y_max=1.0):
        """Generuje Mandelbrotovu množinu podle zadaných rozsahů."""
        x = np.linspace(x_min, x_max, self.width)
        y = np.linspace(y_min, y_max, self.height)
        X, Y = np.meshgrid(x, y)

        c = X + 1j * Y
        z = np.zeros_like(c)  # z_0 = 0
        fractal_img = np.zeros(c.shape, dtype=int)

        for i in range(self.max_iter):
            # Podmínka pro omezení sekvence: |z_n| <= m, kde m = 2
            mask = np.abs(z) <= 2
            # z_{n+1} = z_n^2 + c
            z[mask] = z[mask] ** 2 + c[mask]
            # Uložení čísla iterace pro obarvení
            fractal_img[mask] = i

        return x, y, fractal_img

    def generate_julia(self, c_complex, x_min=-1.5, x_max=1.5, y_min=-1.5, y_max=1.5):
        """Generuje Juliovu množinu pro danou komplexní konstantu c."""
        x = np.linspace(x_min, x_max, self.width)
        y = np.linspace(y_min, y_max, self.height)
        X, Y = np.meshgrid(x, y)

        z = X + 1j * Y  # U Julie je počátečním bodem souřadnice
        fractal_img = np.zeros(z.shape, dtype=int)

        for i in range(self.max_iter):
            # Podmínka pro omezení sekvence: |z_n| <= m, kde m = 2
            mask = np.abs(z) <= 2
            # z_{n+1} = z_n^2 + c
            z[mask] = z[mask] ** 2 + c_complex
            # Uložení čísla iterace pro obarvení
            fractal_img[mask] = i

        return x, y, fractal_img