"""
Verification & Automated Test Suite for apta AI Antigravity Twin Engine.
"""

import os
from pathlib import Path
from core.tools import (
    view_file,
    replace_file_content,
    write_to_file,
    grep_search,
    find_by_name,
    list_dir,
    run_command
)
from core.artifacts import ArtifactManager
from core.skills import SkillsLoader
from core.subagents import SubagentManager
from core.engine import AntigravityEngine

def test_antigravity_tools():
    print("[1/4] Testing Antigravity Tool Primitives...")
    test_file = "test_antigravity.txt"
    
    # Write to file
    res_w = write_to_file(test_file, "Line 1: Antigravity Twin\nLine 2: Test Suite")
    assert "Successfully wrote" in res_w
    
    # View file
    res_v = view_file(test_file, 1, 2)
    assert "Line 1:" in res_v
    
    # Replace file content
    res_r = replace_file_content(test_file, "Twin", "ENGINE")
    assert "Successfully updated" in res_r
    
    # Grep search
    res_g = grep_search("ENGINE", ".")
    assert "ENGINE" in res_g
    
    # Find by name
    res_f = find_by_name("*.py", ".")
    assert "test_agent.py" in res_f
    
    # List dir
    res_l = list_dir(".")
    assert "Contents of" in res_l
    
    # Run command
    res_c = run_command("echo Antigravity_OK")
    assert "Antigravity_OK" in res_c or "executed" in res_c
    
    if os.path.exists(test_file):
        os.remove(test_file)
    print("  [OK] All 7 Antigravity tools passed successfully!")

def test_antigravity_modules():
    print("[2/4] Testing Artifacts, Skills & Subagents Modules...")
    art_mgr = ArtifactManager()
    art = art_mgr.create_artifact("plan.md", "Plan Title", "# Plan Content")
    assert art.filename == "plan.md"
    
    skills = SkillsLoader()
    summary = skills.get_skills_summary()
    assert isinstance(summary, str)
    
    sub = SubagentManager()
    agent = sub.invoke_subagent("Planner", "System Planner", "Plan task")
    assert agent.role == "System Planner"
    print("  [OK] Modules test passed!")

def test_antigravity_engine():
    print("[3/4] Testing Antigravity Trajectory Engine...")
    engine = AntigravityEngine()
    step = engine.execute_step("Mama, run Antigravity test trajectory")
    assert step["step_index"] == 1
    assert "user_input" in step
    print("  [OK] Engine step execution passed!")

def test_server():
    print("[4/4] Testing App Server...")
    try:
        from app_server import app
        from fastapi.testclient import TestClient
        client = TestClient(app)
        res = client.get("/api/health")
        assert res.status_code == 200
        print("  [OK] App Server endpoints passed!")
    except ImportError:
        print("  [INFO] FastAPI testclient optional, skipping HTTP endpoint test.")

if __name__ == "__main__":
    print("==============================================")
    print(" Running apta AI Antigravity Twin Test Suite")
    print("==============================================")
    test_antigravity_tools()
    test_antigravity_modules()
    test_antigravity_engine()
    test_server()
    print("\n[SUCCESS] ALL ANTIGRAVITY TWIN TESTS PASSED!")
