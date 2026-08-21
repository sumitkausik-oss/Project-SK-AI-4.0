import json
import re
from datetime import datetime
from pathlib import Path

class CoralBrainSchema:
    """
    Implements the Universal Mastery Schema (Coral Brain) for dynamic AI evolution.
    Handles contextual memory recall, ranked retrieval, and self-analyzing feedback loops.
    """
    def __init__(self):
        self.brain_initialized = datetime.now()
        self.feedback_log = []
        self.core_modules = {}
        # Memory storage: dict mapping keys to memory dicts
        self.associative_memory = {} 
        print(f"[CORAL_BRAIN]: Deep Logic initialized for SKAI.")

    def integrate_core_engine(self, engine_name, engine_instance):
        self.core_modules[engine_name] = engine_instance
        print(f"[CORAL_BRAIN]: Core Engine [{engine_name}] integrated.")

    def store_memory(self, key, content, tags=None):
        """Stores a durable fact with tags for semantic indexing."""
        self.associative_memory[key] = {
            "content": content,
            "tags": tags or [],
            "timestamp": datetime.now()
        }
        print(f"[CORAL_BRAIN]: Memory durable: {key}")

    def process_task(self, task_instruction):
        # Recall contextually ranked memory
        context = self._recall_memory(task_instruction)
        
        data = f"Executed '{task_instruction}'. Context keys: {list(context.keys())[:3]}"
        result = {"status": "success", "data": data, "timestamp": datetime.now()}
        
        self._log_feedback(task_instruction, result)
        return result

    def _recall_memory(self, instruction):
        """Recall and rank memories based on contextual keyword overlap."""
        instruction_keywords = set(re.findall(r'\b\w+\b', instruction.lower()))
        potential_matches = []
        
        for key, mem_data in self.associative_memory.items():
            key_keywords = set(re.findall(r'\b\w+\b', key.lower()))
            tag_keywords = set([tag.lower() for tag in mem_data['tags']])
            combined = key_keywords.union(tag_keywords)
            
            # Intersection score
            score = len(instruction_keywords.intersection(combined))
            if score > 0:
                potential_matches.append((score, key, mem_data))
                
        # Rank by score descending
        potential_matches.sort(key=lambda x: x[0], reverse=True)
        
        # Returns top 5 scored context memories
        top_context = {item[1]: item[2] for item in potential_matches[:5]}
        if top_context:
            print(f"[CORAL_BRAIN]: {len(top_context)} ranked contextual memories recalled.")
        return top_context

    def _log_feedback(self, task, outcome):
        self.feedback_log.append({"task": task, "outcome": outcome, "timestamp": datetime.now()})
        if outcome["status"] == "failure":
            print(f"[CRITICAL]: Neural exception. Feedback logged.")

    def analyze_performance(self):
        """Analyze feedback and generate self-optimization directives."""
        recent_logs = self.feedback_log[-20:] # Last 20 tasks
        failures = [log for log in recent_logs if log['outcome']['status'] == 'failure']
        
        status = "HEALTHY"
        recommendation = "Maintain baseline operations."
        
        if failures:
            status = "NEEDS_OPTIMIZATION"
            failed_keywords = []
            for f in failures:
                failed_keywords += re.findall(r'\b\w+\b', f['task'].lower())
            
            common_failure_points = sorted(set(failed_keywords), key=failed_keywords.count, reverse=True)[:3]
            recommendation = f"Investigate core engines handling: {common_failure_points}. Failure rate: {len(failures)/len(recent_logs):.2%}"
            
        print(f"[CORAL_BRAIN]: System Report | Status: {status} | Recommendation: {recommendation}")
        return {"status": status, "recommendation": recommendation}
