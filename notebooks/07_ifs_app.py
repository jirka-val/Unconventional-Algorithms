import sys
import os
import plotly.graph_objects as go
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.ifs import IFSModel


def plot_interactive_fractal(points, title):
    """Vykreslí interaktivní 3D graf pomocí Plotly."""
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]

    # Vytvoření 3D scatter plotu
    fig = go.Figure(data=[go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=1,  # Velikost bodů
            color=z,  # Barva se mění podle osy Z
            colorscale='Viridis',  # Barevné schéma
            opacity=0.6  # Průhlednost
        )
    )])

    # Nastavení vzhledu grafu
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='data'
        ),
        margin=dict(r=0, l=0, b=0, t=40)
    )

    fig.show()


def main():
    # Definice parametrů pro oba modely
    model1_params = [
        {'a': 0.00, 'b': 0.00, 'c': 0.01, 'd': 0.00, 'e': 0.26, 'f': 0.00, 'g': 0.00, 'h': 0.00, 'i': 0.05, 'j': 0.00, 'k': 0.00, 'l': 0.00},
        {'a': 0.20, 'b': -0.26, 'c': -0.01, 'd': 0.23, 'e': 0.22, 'f': -0.07, 'g': 0.07, 'h': 0.00, 'i': 0.24, 'j': 0.00, 'k': 0.80, 'l': 0.00},
        {'a': -0.25, 'b': 0.28, 'c': 0.01, 'd': 0.26, 'e': 0.24, 'f': -0.07, 'g': 0.07, 'h': 0.00, 'i': 0.24, 'j': 0.00, 'k': 0.22, 'l': 0.00},
        {'a': 0.85, 'b': 0.04, 'c': -0.01, 'd': -0.04, 'e': 0.85, 'f': 0.09, 'g': 0.00, 'h': 0.08, 'i': 0.84, 'j': 0.00, 'k': 0.80, 'l': 0.00}
    ]

    model2_params = [
        {'a': 0.05, 'b': 0.00, 'c': 0.00, 'd': 0.00, 'e': 0.60, 'f': 0.00, 'g': 0.00, 'h': 0.00, 'i': 0.05, 'j': 0.00, 'k': 0.00, 'l': 0.00},
        {'a': 0.45, 'b': -0.22, 'c': 0.22, 'd': 0.22, 'e': 0.45, 'f': 0.22, 'g': -0.22, 'h': 0.22, 'i': -0.45, 'j': 0.00, 'k': 1.00, 'l': 0.00},
        {'a': -0.45, 'b': 0.22, 'c': -0.22, 'd': 0.22, 'e': 0.45, 'f': 0.22, 'g': 0.22, 'h': -0.22, 'i': 0.45, 'j': 0.00, 'k': 1.25, 'l': 0.00},
        {'a': 0.49, 'b': -0.08, 'c': 0.08, 'd': 0.08, 'e': 0.49, 'f': 0.08, 'g': 0.08, 'h': -0.08, 'i': 0.49, 'j': 0.00, 'k': 2.00, 'l': 0.00}
    ]

    # Výběr modelu a generování
    iterations = 200000

    # První model
    ifs1 = IFSModel(model1_params)
    points1 = ifs1.generate(iterations=iterations)
    print("Vykresluji první model...")
    plot_interactive_fractal(points1, "First Model (IFS)")

    # Druhý model
    ifs2 = IFSModel(model2_params)
    points2 = ifs2.generate(iterations=iterations)
    print("Vykresluji druhý model...")
    plot_interactive_fractal(points2, "Second Model (IFS)")


if __name__ == "__main__":
    main()