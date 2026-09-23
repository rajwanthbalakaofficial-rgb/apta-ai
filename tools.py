"""
Universal Tool Suite for apta AI:
File system, code search, text editing, terminal execution, web content fetching, and biofeedback telemetry.
"""

import os
import re
import fnmatch
import subprocess
import urllib.request
from pathlib import Path
from typing import List, Dict, Any

def read_file(file_path: str) -> str:
    """
    Read contents of a file at the specified file_path.
    
    Args:
        file_path: Absolute or relative path to the file.
    """
    try:
        path = Path(file_path).resolve()
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        if not path.is_file():
            return f"Error: '{file_path}' is a directory, not a file."
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"Error reading file '{file_path}': {str(e)}"

def write_file(file_path: str, content: str) -> str:
    """
    Write content to a file at the specified file_path. Creates parent directories if missing.
    
    Args:
        file_path: Absolute or relative path to the target file.
        content: Text content to write into the file.
    """
    try:
        path = Path(file_path).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Successfully wrote {len(content)} characters to '{file_path}'."
    except Exception as e:
        return f"Error writing file '{file_path}': {str(e)}"

def replace_in_file(file_path: str, target_text: str, replacement_text: str) -> str:
    """
    Replace precise text inside a file.
    
    Args:
        file_path: Absolute or relative path to target file.
        target_text: Exact string content to find and replace.
        replacement_text: New string content to place instead.
    """
    try:
        path = Path(file_path).resolve()
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        
        content = path.read_text(encoding="utf-8", errors="replace")
        if target_text not in content:
            return f"Error: Target text not found in '{file_path}'."
            
        new_content = content.replace(target_text, replacement_text, 1)
        path.write_text(new_content, encoding="utf-8")
        return f"Successfully updated '{file_path}'."
    except Exception as e:
        return f"Error modifying file '{file_path}': {str(e)}"

def list_dir(directory_path: str = ".") -> str:
    """
    List contents of a directory with file types and sizes.
    
    Args:
        directory_path: Directory path to list. Defaults to current directory.
    """
    try:
        path = Path(directory_path).resolve()
        if not path.exists():
            return f"Error: Directory '{directory_path}' does not exist."
        if not path.is_dir():
            return f"Error: '{directory_path}' is a file, not a directory."
        
        items = list(path.iterdir())
        output = [f"Contents of {path}:"]
        for item in sorted(items, key=lambda x: (not x.is_dir(), x.name.lower())):
            kind = "[DIR] " if item.is_dir() else "[FILE]"
            size = f" ({item.stat().st_size} bytes)" if item.is_file() else ""
            output.append(f"  {kind} {item.name}{size}")
        return "\n".join(output)
    except Exception as e:
        return f"Error listing directory '{directory_path}': {str(e)}"

def find_files(pattern: str, search_directory: str = ".") -> str:
    """
    Search for files matching a glob pattern (e.g. *.py, *.js, *.ino) within search_directory.
    
    Args:
        pattern: Glob search pattern (e.g. '*.py' or '*eeg*').
        search_directory: Directory to search inside. Defaults to '.'.
    """
    try:
        root = Path(search_directory).resolve()
        if not root.exists():
            return f"Error: Directory '{search_directory}' does not exist."
            
        matches = []
        for path in root.rglob(pattern):
            rel_path = path.relative_to(root)
            if not any(part.startswith(".") for part in rel_path.parts):
                matches.append(str(path))
                if len(matches) >= 50:
                    break
                
        if not matches:
            return f"No files matching '{pattern}' found in '{search_directory}'."
            
        return f"Found {len(matches)} matching files:\n" + "\n".join(matches)
    except Exception as e:
        return f"Error searching files: {str(e)}"

def search_files(query: str, search_directory: str = ".") -> str:
    """
    Search for exact text query across files in a directory (like grep).
    
    Args:
        query: String text pattern to search for inside file contents.
        search_directory: Root directory path to search.
    """
    try:
        root = Path(search_directory).resolve()
        results = []
        
        for path in root.rglob("*"):
            if path.is_file():
                rel_path = path.relative_to(root)
                if not any(part.startswith(".") for part in rel_path.parts):
                    try:
                        text = path.read_text(encoding="utf-8", errors="ignore")
                        for i, line in enumerate(text.splitlines(), start=1):
                            if query.lower() in line.lower():
                                results.append(f"{path.name} (Line {i}): {line.strip()}")
                                if len(results) >= 50:
                                    break
                    except Exception:
                        continue
            if len(results) >= 50:
                break
                
        if not results:
            return f"No occurrences of '{query}' found."
            
        return f"Found {len(results)} matches for '{query}':\n" + "\n".join(results)
    except Exception as e:
        return f"Error searching text in files: {str(e)}"

def fetch_web_content(url: str) -> str:
    """
    Fetch public web page content or API text from a URL via HTTP GET.
    
    Args:
        url: Public Web URL (e.g. https://api.github.com or documentation URL).
    """
    try:
        req = urllib.request.Request(
            url, 
            headers={"User-Agent": "AptaAI-UniversalAgent/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode("utf-8", errors="replace")
            if len(content) > 4000:
                content = content[:4000] + "\n...[Content Truncated]"
            return content
    except Exception as e:
        return f"Error fetching web URL '{url}': {str(e)}"

def execute_command(command: str) -> str:
    """
    Execute a shell/terminal command and return stdout and stderr.
    
    Args:
        command: The shell command line string to execute.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        
        out = []
        if stdout:
            out.append(f"STDOUT:\n{stdout}")
        if stderr:
            out.append(f"STDERR:\n{stderr}")
        if not stdout and not stderr:
            out.append(f"Command executed with return code {result.returncode}.")
        return "\n".join(out)
    except subprocess.TimeoutExpired:
        return "Error: Command execution timed out after 30 seconds."
    except Exception as e:
        return f"Error executing command: {str(e)}"

def get_stress_recommendation(stress_score: float, primary_state: str = "Normal") -> str:
    """
    Generate biofeedback recommendation based on Udvegadarshini EEG stress score.
    
    Args:
        stress_score: Numerical stress score from 0.0 to 100.0%.
        primary_state: Detected mental state (e.g. Deep Relaxation, Relaxed, Focused, Elevated, High Stress).
    """
    score = float(stress_score)
    if score <= 20.0:
        return "State: Deep Meditation (Delta/Theta dominance). Recommendation: Continue session; brainwave coherence is optimal."
    elif score <= 40.0:
        return "State: Relaxed Calm (Alpha dominance). Recommendation: Play 432Hz Solfeggio soundscape for sustained tranquility."
    elif score <= 60.0:
        return "State: Active Cognition (Beta presence). Recommendation: 2-minute light breathing break."
    elif score <= 80.0:
        return "State: High Stress / Anxiety. Recommendation: Activate 4-7-8 Breathing Guide & 528Hz Transformation Frequency."
    else:
        return "State: Severe Stress Spike. Recommendation: Trigger immediate 6Hz Theta Binaural Beats & Tactile Stress Relief Game."

# Full Universal Tool Registry
UNIVERSAL_TOOLS = [
    read_file,
    write_file,
    replace_in_file,
    list_dir,
    find_files,
    search_files,
    fetch_web_content,
    execute_command,
    get_stress_recommendation
]
