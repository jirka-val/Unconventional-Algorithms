import numpy as np


class ForestFireModel:
    EMPTY = 0
    TREE = 1
    FIRE = 2

    @staticmethod
    def initialize_grid(size, density):
        """
        Inicializuje mřížku s danou hustotou stromů.
        """
        # Vygenerujeme náhodnou mřížku podle hustoty
        grid = np.random.choice(
            [ForestFireModel.EMPTY, ForestFireModel.TREE],
            size=(size, size),
            p=[1.0 - density, density]
        )
        return grid

    @staticmethod
    def step(grid, p, f):
        """
        Provede jeden krok celulárního automatu podle 4 pravidel.
        Používá plně vektorizované numpy operace pro rychlost.
        """
        new_grid = grid.copy()

        # Masky pro aktuální stavy buněk
        empty = (grid == ForestFireModel.EMPTY)
        tree = (grid == ForestFireModel.TREE)
        fire = (grid == ForestFireModel.FIRE)

        # Spočítáme hořící sousedy (Von Neumannovo okolí - 4 směry)
        # Posuneme matici 'fire' do 4 stran a sečteme
        burning_neighbors = np.zeros_like(grid, dtype=int)
        burning_neighbors[:-1, :] += fire[1:, :]  # Soused dole
        burning_neighbors[1:, :] += fire[:-1, :]  # Soused nahoře
        burning_neighbors[:, :-1] += fire[:, 1:]  # Soused vpravo
        burning_neighbors[:, 1:] += fire[:, :-1]  # Soused vlevo

        # Pravidlo 1: Prázdné místo vyroste ve strom s pravděpodobností 'p'
        grow_mask = empty & (np.random.random(grid.shape) < p)
        new_grid[grow_mask] = ForestFireModel.TREE

        # Pravidlo 2: Strom chytne, pokud hoří některý z jeho sousedů
        ignite_from_neighbor = tree & (burning_neighbors > 0)

        # Pravidlo 3: Strom chytne sám od sebe (blesk) s pravděpodobností 'f'
        ignite_randomly = tree & (np.random.random(grid.shape) < f)

        new_grid[ignite_from_neighbor | ignite_randomly] = ForestFireModel.FIRE

        # Pravidlo 4: Hořící strom vyhoří a stane se prázdným místem
        new_grid[fire] = ForestFireModel.EMPTY

        return new_grid