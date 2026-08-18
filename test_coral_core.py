
import sys
from pathlib import Path

# Add the project root to sys.path to allow importing from core
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from core.coral_brain_logic import CoralBrainSchema

def run_test():
    print("--- Testing Enhanced Coral Brain Core ---")
    brain = CoralBrainSchema()

    # Test Storing Memory
    print("\n[TEST]: Storing test memories...")
    brain.store_memory("project jarvis status", "Working on Visual Hub v2", ["jarvis", "visuals", "status"])
    brain.store_memory("owner preference", "Inventor Usman prefers Hindi for voice chat.", ["preference", "owner", "language"])

    # Test Task Processing with Recall
    print("\n[TEST]: Processing task that should recall memory...")
    # 'visuals' should trigger the first memory
    task = "Update the visuals for Jarvis project" 
    result = brain.process_task(task)
    print(f"[RESULT]: {result['data']}")

    # Test Performance Analysis
    print("\n[TEST]: Analyzing performance...")
    brain.analyze_performance()

    print("\n--- Test Completed ---")

if __name__ == "__main__":
    run_test()
