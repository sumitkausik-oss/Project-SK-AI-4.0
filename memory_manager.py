import json
import os

class KnowledgeNode:
    def __init__(self, entity, relation, value, context=None):
        self.entity = entity
        self.relation = relation
        self.value = value
        self.context = context

    def to_dict(self):
        return {
            "entity": self.entity,
            "relation": self.relation,
            "value": self.value,
            "context": self.context
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["entity"], data["relation"], data["value"], data["context"])

class MemoryManager:
    def __init__(self, file_path=r"D:\Project SK AI 4.0\dynamic_memory.json"):
        self.file_path = file_path
        self.memory = []
        self.load_memory()

    def add_fact(self, entity, relation, value, context=None):
        node = KnowledgeNode(entity, relation, value, context)
        self.memory.append(node)
        self.save_memory()

    def save_memory(self):
        data = [node.to_dict() for node in self.memory]
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def load_memory(self):
        if not os.path.exists(self.file_path):
            self.memory = []
            return
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.memory = [KnowledgeNode.from_dict(item) for item in data]

# Initialization example
# manager = MemoryManager()
