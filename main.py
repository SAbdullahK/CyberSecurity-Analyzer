import os
import json
import ast
import pandas as pd
from pprint import pprint
from dotenv import load_dotenv
import google.generativeai as genai
from core.orchestrator import DectectionOrchestrator
from response.severity import calculate_severity
from response.coordinator import ResponseCordinator
from intelligence.context_analyzer import ContextualAnalyzer
from simulation.traffic_generator import TrafficSimulator
from simulation.log_generator import LogSimulator
from core.pretty_printer import pretty_print_analysis

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

import json, ast, os

import json, ast, os
import google.generativeai as genai

class GeminiClient:
    def __init__(self, model_name="gemini-2.5-pro"):
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(model_name)

    def generate(self, prompt: str) -> dict:
        structured_prompt = f"""
        You are a CyberSecurity assistant. Always respond in JSON format like this:

        {{
          "threat_type": "Brute-Force Attack",
          "known_attack": "Yes",
          "recommended_actions": [
            "Lock accounts after multiple failed login attempts",
            "Enable multi-factor authentication (2FA)",
            "Monitor and block suspicious IP addresses"
          ]
        }}

        Input:
        {prompt}
        """

        response = self.model.generate_content(structured_prompt)
        text = response.text.strip()

        # 1️⃣ Clean markdown wrappers if present
        if text.startswith("```"):
            text = text.strip("` \n")
            text = text.replace("json\n", "").replace("json", "")

        # 2️⃣ Try JSON parsing
        try:
            return json.loads(text)
        except Exception:
            pass

        # 3️⃣ Try Python dict parsing (handles single quotes ✅)
        try:
            return ast.literal_eval(text)
        except Exception:
            pass

        # 4️⃣ Fallback
        return {"error": "Invalid Gemini response", "raw": text}

    
def main():
    print("\n🚀  Starting Cybersecurity Analyzer with Simulation + RAG + Gemini")

    # ---Simulation---
    traffic_sim = TrafficSimulator(n_samples=100, anomaly_ratio=0.15)
    log_sim = LogSimulator(n_entries=20)
    df_network = traffic_sim.generate()
    df_logs = log_sim.generate()

    # ---Dectection---
    orchestrator  = DectectionOrchestrator()
    algorithms = orchestrator.select_algorithms("network_traffic")
    results = []

    for algo in algorithms:
        try:
            y_pred = algo.fit_predict(df_network)
            results.extend(y_pred)
        except Exception as e:
            print("Skipping algorithm: ", {str(e)}) 
    
    anomaly_result = results[0] if results else 1
    severity = calculate_severity(anomaly_result)
    print(f"Anomaly Result: {anomaly_result}, Severity: {severity}")


    # ===Intelligence (RAG + GEMINI)=== 
    analyzer = ContextualAnalyzer(gemini_client = GeminiClient())
    explaination = analyzer.enhenced_explaination(anomaly_result, severity, {"system": "simulated-auth"})
    print("\n🧠 RAG + Gemini Explanation:")
    pretty_print_analysis(explaination, severity)

    # ---Response---
    coordinator = ResponseCordinator()
    coordinator.coordinate_response(anomaly_result, severity)

if __name__ == "__main__":
    main()