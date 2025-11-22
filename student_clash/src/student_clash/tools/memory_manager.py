import json
from pathlib import Path

MEMORY_FILE = Path(__file__).parent.parent / "memory.json"

class MemoryManager:
    def __init__(self):
        self.memory = self.load_memory()

    def load_memory(self):
        if MEMORY_FILE.exists():
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
            
        # Memoria iniziale vuota
        return {
            "fitness_level": None,
            "diet_pref": None,
            "stress_level": None,
            "time_available": None,
            "last_workout": None,
            "last_meal_plan": None
        }

    def save_memory(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=4)

    def update(self, key, value):
        self.memory[key] = value
        self.save_memory()

    def get(self, key):
        return self.memory.get(key)
