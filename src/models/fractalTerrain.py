import random
import math


class FractalTerrain:
    @staticmethod
    def generate_2d_terrain(start_x, start_y, end_x, end_y, iterations, offset_input, hurst=0.8):
        """
        Generuje 2D terén s využitím Gaussova šumu a Hurstova exponentu
        podle teorie Paula Bourkeho.
        """
        points = [(start_x, start_y), (end_x, end_y)]

        roughness = math.pow(2.0, -hurst)
        current_offset = offset_input * 15.0

        for _ in range(iterations):
            new_points = []
            for i in range(len(points) - 1):
                p1 = points[i]
                p2 = points[i + 1]

                mid_x = (p1[0] + p2[0]) / 2.0

                displacement = random.gauss(0, 1) * current_offset
                mid_y = (p1[1] + p2[1]) / 2.0 + displacement

                new_points.append(p1)
                new_points.append((mid_x, mid_y))

            new_points.append(points[-1])
            points = new_points

            current_offset *= roughness

        return points