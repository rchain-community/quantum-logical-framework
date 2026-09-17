"""Spacetime latency grid for the QuCalc engine. Write-up: SpaceTime.md."""
import math


class QuCalcNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w_zfa = 1.0  # Base ZFA degeneracy (flat space)
        self.latency = 1.0 # Base time delay

    def update_latency(self):
        # Latency is inversely proportional to degeneracy
        self.latency = 1.0 / max(0.1, self.w_zfa)

class SpacetimeGrid:
    def __init__(self, size):
        self.size = size
        self.grid = [[QuCalcNode(x, y) for y in range(size)] for x in range(size)]
        self.masses = []

    def add_mass(self, x, y, mass_value):
        self.masses.append((x, y, mass_value))
        self.calculate_zfa_field()

    def calculate_zfa_field(self):
        # A mass acts as a Markov Blanket, restricting W_ZFA (degeneracy) nearby
        for x in range(self.size):
            for y in range(self.size):
                node = self.grid[x][y]
                # Default high degeneracy in empty space
                node.w_zfa = 100.0 
                
                for mx, my, mass_value in self.masses:
                    distance = math.sqrt((x - mx)**2 + (y - my)**2)
                    if distance == 0: distance = 0.1
                    
                    # Mass reduces the number of available ZFA paths
                    # This represents the "possibilist constraint"
                    zfa_penalty = mass_value / (distance ** 2)
                    node.w_zfa = max(1.0, node.w_zfa - zfa_penalty)
                
                node.update_latency()

    def step_particle(self, px, py):
        # Particle moves toward the highest latency (lowest W_ZFA)
        # This models Gravity as a Possibilist Gradient
        neighbors = [
            (px+1, py), (px-1, py), (px, py+1), (px, py-1)
        ]
        
        best_latency = -1
        best_pos = (px, py)
        
        for nx, ny in neighbors:
            if 0 <= nx < self.size and 0 <= ny < self.size:
                latency = self.grid[nx][ny].latency
                if latency > best_latency:
                    best_latency = latency
                    best_pos = (nx, ny)
                    
        return best_pos

# --- Demonstration ---
if __name__ == "__main__":
    print("Initializing QLF Spacetime Substrate...")
    universe = SpacetimeGrid(size=20)
    
    # Place a massive object (e.g., a planet or dense ZFA cluster)
    planet_pos = (10, 10)
    universe.add_mass(*planet_pos, mass_value=500.0)
    print(f"Massive cluster added at {planet_pos}")
    
    # Spawn a particle
    particle_pos = (2, 2)
    print(f"Particle spawned at {particle_pos}")
    
    # Simulate logical ticks
    print("\nSimulating Logical Resolution (Gravity as Latency Gradient):")
    for tick in range(15):
        particle_pos = universe.step_particle(*particle_pos)
        current_latency = universe.grid[particle_pos[0]][particle_pos[1]].latency
        print(f"Tick {tick+1:02d}: Particle at {particle_pos} | Local Latency (Time Dilation): {current_latency:.3f}")
        
        if particle_pos == planet_pos:
            print("Particle has merged with the massive ZFA cluster.")
            break
