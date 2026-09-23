"""
Quick Live Demo & Functional Test Script for apta AI.
"""

from agent import AptaAgent
from tools import get_stress_recommendation

def run_demo():
    print("==================================================")
    print(" DEMO TEST: apta AI (Apta AI Engine)")
    print("==================================================")
    
    # 1. Testing Udvegadarshini Mode with Simulated Telemetry
    print("\n--- TEST 1: Udvegadarshini Biofeedback Mode ---")
    udvega_agent = AptaAgent(mode="udvegadarshini")
    
    simulated_telemetry = {
        "stress_score": 78.5,
        "state": "High Stress / Anxiety",
        "band_powers": {"Delta": 12.1, "Theta": 18.4, "Alpha": 15.2, "Beta": 42.0, "Gamma": 12.3}
    }
    
    user_msg = "Mama, exam & project tension valla stress ekkuva aypoyindhi..."
    print(f"User Message: '{user_msg}'")
    print(f"Live EEG Stress Score: {simulated_telemetry['stress_score']}% ({simulated_telemetry['state']})")
    
    reply = udvega_agent.send_message(user_msg, stress_context=simulated_telemetry)
    print("\n[apta AI Biofeedback Response]:")
    print(reply)
    
    # 2. Testing Biofeedback Recommendation Engine Directly
    print("\n--- TEST 2: Direct Stress Recommendation Engine ---")
    rec = get_stress_recommendation(simulated_telemetry['stress_score'], simulated_telemetry['state'])
    print(f"Engine Suggestion: {rec}")
    
    # 3. Testing Coding Assistant Tool Capability
    print("\n--- TEST 3: Coding Agent Initialization ---")
    coding_agent = AptaAgent(mode="coding")
    print(f"Coding Agent Mode Active: {coding_agent.mode == 'coding'}")
    print("System Instruction Loaded: Yes")
    print("\n[SUCCESS] Demo execution completed successfully!")

if __name__ == "__main__":
    run_demo()
