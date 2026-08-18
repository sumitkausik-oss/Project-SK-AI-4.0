from memory_manager import MemoryManager
import json
import os

# Initialize Manager
manager = MemoryManager()

# Add test data
print("Adding test data...")
manager.add_fact("JarvisCore", "feature", "AssociativeMemory")
manager.add_fact("System", "status", "Testing")

# Verify data saved to file
file_path = r"D:\Project SK AI 4.0\dynamic_memory.json"
print(f"Checking file: {file_path}")

if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print("Data in file:")
        print(json.dumps(data, indent=2))
else:
    print("Error: Memory file not found.")
