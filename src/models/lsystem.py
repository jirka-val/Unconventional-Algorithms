import numpy as np

class LSystem:
    def __init__(self, axiom="", rules=None, angle_degree=0):
        self.axiom = axiom
        self.rules = rules if rules else {}
        self.angle_degree = angle_degree

    def generate_path(self, iterations):
        """Vygeneruje výsledný řetězec po zadaném počtu vnoření."""
        current_state = self.axiom
        for _ in range(iterations):
            next_state = ""
            for char in current_state:
                next_state += self.rules.get(char, char)
            current_state = next_state
        return current_state