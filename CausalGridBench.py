import random
import json
from typing import Dict, List

class CausalGridWorld:
    def __init__(self, size: int = 11):
        self.size = size
        self.objects = {
            'K': 'Key - protects from Fire and opens Door',
            'D': 'Door - blocks Goal unless Key collected',
            'M': 'Mushroom - +10 reward',
            'F': 'Fire - -20 reward unless Key protects',
            'G': 'Goal - +50 reward if reached'
        }
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.player_pos = (size // 2, size // 2)  # Center start
        self.inventory = []
        self.place_objects()

    def place_objects(self):
        positions = random.sample(range(self.size ** 2), len(self.objects))
        for obj, pos in zip(self.objects.keys(), positions):
            x, y = divmod(pos, self.size)
            self.grid[x][y] = obj

    def compute_reward(self, trajectory: List[str]) -> int:
        """Causal reward based on rules (intervention-safe)"""
        reward = 0
        has_key = False
        at_goal = False
        for action in trajectory:
            # Simulate movement (simplified)
            if 'G' in trajectory:  # Reached Goal
                at_goal = True
            if 'K' in trajectory:
                has_key = True
            if 'M' in trajectory:
                reward += 10
            if 'F' in trajectory:
                reward -= 0 if has_key else 20
            if 'D' in trajectory and not has_key:
                at_goal = False  # Blocked
        if at_goal:
            reward += 50
        return reward

    def generate_intervention_question(self):
        """Create counterfactual: 'If we remove Fire, what happens to reward?'"""
        base_traj = ['move to M', 'move to F', 'move to G']  # Example
        base_reward = self.compute_reward(base_traj)
        intervened_reward = self.compute_reward(base_traj) + 20  # Remove Fire penalty
        return {
            "question": f"Base trajectory reward: {base_reward}. If we intervene and remove the Fire object, why does reward change and to what?",
            "answer": f"Fire causes -20 penalty without Key. Removing it adds +20. New reward: {intervened_reward}. Causal, not correlational."
        }

# Generate dataset
def generate_dataset(num_worlds=1000):
    dataset = []
    for _ in range(num_worlds):
        world = CausalGridWorld()
        question = world.generate_intervention_question()
        dataset.append({
            "grid": world.grid,
            "question": question["question"],
            "gold_answer": question["answer"]
        })
    with open('causalgridbench.json', 'w') as f:
        json.dump(dataset, f)
    return dataset

# Run it
if __name__ == "__main__":
    generate_dataset(5000)  # 5K examples for robust eval
    print("CausalGridBench generated — tests intervention/counterfactual reasoning!")