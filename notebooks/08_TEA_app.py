import sys
import os
import plotly.graph_objects as go

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.fractals import FractalModel

def plot_interactive_fractal(x, y, z_data, title):
    """Vykreslí interaktivní 2D fraktál pomocí Plotly."""
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=x,
        y=y,
        colorscale="Viridis", # "Hot"
        hoverinfo='none',
        showscale=False
    ))

    fig.update_layout(
        title=title,
        xaxis_title='Re(c) / Osa X',
        yaxis_title='Im(c) / Osa Y',
        yaxis=dict(scaleanchor="x", scaleratio=1),
        margin=dict(r=20, l=20, b=40, t=40)
    )

    fig.show()

def main():
    # Model s vysokým rozlišením
    model = FractalModel(width=1000, height=1000, max_iter=100)

    # Zobrazení Mandelbrotovy množiny
    x_m, y_m, img_m = model.generate_mandelbrot(x_min=-2, x_max=1, y_min=-1, y_max=1)
    plot_interactive_fractal(x_m, y_m, img_m, "Mandelbrot Set ")

    # Zobrazení Juliovy množiny
    c_const = complex(-0.4, 0.6)
    x_j, y_j, img_j = model.generate_julia(c_const, x_min=-1.5, x_max=1.5, y_min=-1.5, y_max=1.5)
    plot_interactive_fractal(x_j, y_j, img_j, f"Julia Set pro c = {c_const}")

if __name__ == "__main__":
    main()