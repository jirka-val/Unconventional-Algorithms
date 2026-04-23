import math
import random


class FractalTerrain:
    @staticmethod
    def generate_2d_terrain(start_x, start_y, end_x, end_y, iterations, offset_factor):
        """
        Generuje 2D terén algoritmem Midpoint Displacement.
        Kombinuje Gaussovský šum se zmenšováním posunu
        striktně podle délky úsečky .
        """
        points = [(start_x, start_y), (end_x, end_y)]

        for _ in range(iterations):
            new_points = []
            for i in range(len(points) - 1):
                p1 = points[i]
                p2 = points[i + 1]

                # Nalezení geometrického středu na ose X a Y
                mid_x = (p1[0] + p2[0]) / 2.0
                mid_y = (p1[1] + p2[1]) / 2.0

                # Změříme aktuální délku úsečky pomocí Pythagorovy věty
                line_length = math.hypot(p2[0] - p1[0], p2[1] - p1[1])

                # Gaussovo rozdělení
                # ale velikost výchylky odvodíme z délky aktuální úsečky a offsetu
                displacement = random.gauss(0, 1) * (line_length / offset_factor)

                mid_y += displacement

                # Přidáme levý bod a nový střed
                new_points.append(p1)
                new_points.append((mid_x, mid_y))

            # Přidáme koncový bod
            new_points.append(points[-1])
            points = new_points

        return points