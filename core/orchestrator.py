from core.dectector_engine import IsolationForestDectector, LOFDectector, PCADectector
from intelligence.threat_rules import PatternMatcher

class DectectionOrchestrator:
    def __init__(self):
        self.algorithms = {
            "network_traffic" : [IsolationForestDectector(), LOFDectector()],
            "log_analysis" : [PCADectector()],
            "behavioral" : [IsolationForestDectector(max_samples=200)],
            "signature_based" : [PatternMatcher()]
        }

    def select_algorithms(self, data_type):
        return self.algorithms.get(data_type, [IsolationForestDectector()])
    