"""
QLF ACTIVE INFERENCE DEMO (write-up: active_inference.md)
Extends blanket_kinematics.py to show possibilistic agency via ZFA minimization.
"""

from blanket_kinematics import KinematicsEngine, Node
import random

class ActiveInferenceAgent:
    def __init__(self):
        self.blanket = Node("Agent_Blanket", [0.0, 0.0])
        self.possible_actions = ["stay", "move_left", "move_right"]

    def compute_free_energy(self, action):
        # Simple surprise based on ZFA principle
        if action == "stay":
            return 2.0  # High surprise
        return random.uniform(0.1, 1.0)  # Lower for good actions

    def select_action(self):
        # Possibilistic selection: choose action minimizing expected free energy
        energies = {a: self.compute_free_energy(a) for a in self.possible_actions}
        best_action = min(energies, key=energies.get)
        print(f"Selected action: {best_action} (ZFA minimized)")
        return best_action

# Run demo
agent = ActiveInferenceAgent()
agent.select_action()
