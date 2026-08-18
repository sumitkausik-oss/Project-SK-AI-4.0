
import sys
import json
from pathlib import Path
from datetime import datetime

# Add the project root to sys.path to allow importing from core
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from core.coral_brain_logic import CoralBrainSchema

def run_advanced_test():
    print("--- Testing Advanced Ranked Memory & Feedback Analysis ---")
    brain = CoralBrainSchema()

    # 1. Store Memories with overlapping tags for ranking test
    print("\n[TEST]: Storing ranked test memories...")
    # Matches 'visuals', 'status' (Score 2 for 'visual status')
    brain.store_memory("visual status direct", "UI is operational.", ["visuals", "status"])
    # Matches 'visuals', 'status', 'project' (Score 3 for 'visual status project')
    brain.store_memory("project visual overview", "Showing Project Overview Panel.", ["visuals", "status", "project"])
    # Matches 'project' (Score 1 for 'project')
    brain.store_memory("general data", "Random context.", ["project"])

    # 2. Test Ranked Selection
    print("\n[TEST]: Processing query: 'Check visual status project'...")
    # Instruction has 'check', 'visual', 'status', 'project'
    task = "Check visual status project" 
    result = brain.process_task(task)
    # Output expected: data should refer to 'project visual overview' as top memory
    print(f"[RESULT]: {result['data']}")

    # 3. Force direct log entry for failure testing
    print("\n[TEST]: Simulating module failures...")
    brain._log_feedback("Arduino engine activation", {"status": "failure", "error": "port busy"})
    brain._log_feedback("Arduino sensor read", {"status": "failure", "error": "timeout"})

    # 4. Test Performance Analysis Directive
    print("\n[TEST]: Analyzing system performance...")
    brain.analyze_performance()

    print("\n--- Advanced Test Completed ---")

if __name__ == "__main__":
    run_advanced_test()
