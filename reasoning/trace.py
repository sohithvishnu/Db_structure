
# persona_graph_memory/reasoning/trace.py

class ThoughtTracer:
    def __init__(self):
        self.traces = []

    def log(self, reason, context):
        self.traces.append({"reason": reason, "context": context})

    def get_traces(self):
        return self.traces