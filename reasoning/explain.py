
# persona_graph_memory/reasoning/explain.py

class ExplanationEngine:
    def __init__(self, tracer):
        self.tracer = tracer

    def from_trace(self):
        explanations = []
        for trace in self.tracer.get_traces():
            reason = trace["reason"]
            context = trace["context"]
            explanation = f"Because {context}, we conclude: {reason}."
            explanations.append(explanation)
        return explanations
