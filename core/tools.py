"""
Antigravity Core Tool Primitives:
view_file, replace_file_content, write_to_file, grep_search, find_by_name, list_dir, run_command.
"""

import os
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

def view_file(file_path: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> str:
    """
    View contents of a file with line-number slicing support (1-indexed).
    
    Args:
        file_path: Absolute or relative path to target file.
        start_line: Optional 1-indexed starting line number.
        end_line: Optional 1-indexed ending line number.
    """
    try:
        path = Path(file_path).resolve()
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        if not path.is_file():
            return f"Error: '{file_path}' is a directory, not a file."
            
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        total_lines = len(lines)
        
        s_line = start_line if start_line and start_line > 0 else 1
        e_line = end_line if end_line and end_line <= total_lines else total_lines
        
        s_idx = max(0, s_line - 1)
        e_idx = min(total_lines, e_line)
        
        selected_lines = lines[s_idx:e_idx]
        output = [f"File Path: {path}", f"Total Lines: {total_lines}", f"Showing lines {s_line} to {e_line}:\n"]
        
        for i, line in enumerate(selected_lines, start=s_line):
            output.append(f"{i:4d}: {line}")
            
        return "\n".join(output)
    except Exception as e:
        return f"Error viewing file '{file_path}': {str(e)}"

def replace_file_content(file_path: str, target_content: str, replacement_content: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> str:
    """
    Perform precise single contiguous block substitution inside a file.
    
    Args:
        file_path: Path to target file.
        target_content: Exact character sequence to search for and replace.
        replacement_content: Drop-in replacement string.
        start_line: Optional search range start line.
        end_line: Optional search range end line.
    """
    try:
        path = Path(file_path).resolve()
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
            
        text = path.read_text(encoding="utf-8", errors="replace")
        if target_content not in text:
            return f"Error: Target content not found in '{file_path}'."
            
        new_text = text.replace(target_content, replacement_content, 1)
        path.write_text(new_text, encoding="utf-8")
        return f"Successfully updated '{file_path}'."
    except Exception as e:
        return f"Error modifying file '{file_path}': {str(e)}"

def write_to_file(target_file: str, code_content: str, overwrite: bool = True, artifact_metadata: Optional[Dict[str, Any]] = None) -> str:
    """
    Create or overwrite a file. Supports artifact metadata tagging.
    
    Args:
        target_file: File path to write into.
        code_content: Code/text content.
        overwrite: Overwrite existing file flag.
        artifact_metadata: Optional dictionary with artifact metadata (Summary, UserFacing, RequestFeedback).
    """
    try:
        path = Path(target_file).resolve()
        if path.exists() and not overwrite:
            return f"Error: File '{target_file}' already exists and overwrite is set to False."
            
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(code_content, encoding="utf-8")
        
        artifact_msg = ""
        if artifact_metadata:
            summary = artifact_metadata.get("Summary", "Artifact created.")
            artifact_msg = f" (Artifact tagged: {summary})"
            
        return f"Successfully wrote {len(code_content)} bytes to '{target_file}'{artifact_msg}."
    except Exception as e:
        return f"Error writing file '{target_file}': {str(e)}"

def grep_search(query: str, search_path: str = ".", case_insensitive: bool = True) -> str:
    """
    Search for regex/text pattern matches across files in a directory.
    
    Args:
        query: String text pattern to search.
        search_path: Directory path to search inside.
        case_insensitive: Perform case-insensitive search.
    """
    try:
        root = Path(search_path).resolve()
        if not root.exists():
            return f"Error: Search path '{search_path}' does not exist."
            
        results = []
        flags = re.IGNORECASE if case_insensitive else 0
        pattern = re.compile(query, flags)
        
        for path in root.rglob("*"):
            if path.is_file():
                rel_path = path.relative_to(root)
                if not any(part.startswith(".") for part in rel_path.parts):
                    try:
                        text = path.read_text(encoding="utf-8", errors="ignore")
                        for i, line in enumerate(text.splitlines(), start=1):
                            if pattern.search(line):
                                results.append(f"{rel_path}:{i}: {line.strip()}")
                                if len(results) >= 50:
                                    break
                    except Exception:
                        continue
            if len(results) >= 50:
                break
                
        if not results:
            return f"No matches found for query '{query}' in '{search_path}'."
            
        return f"Found {len(results)} matches for '{query}':\n" + "\n".join(results)
    except Exception as e:
        return f"Error performing grep search: {str(e)}"

def find_by_name(pattern: str, search_directory: str = ".") -> str:
    """
    Search for files matching a glob pattern (e.g. *.py, *.md, *.js).
    
    Args:
        pattern: Glob pattern string.
        search_directory: Directory to search inside.
    """
    try:
        root = Path(search_directory).resolve()
        if not root.exists():
            return f"Error: Search directory '{search_directory}' does not exist."
            
        matches = []
        for path in root.rglob(pattern):
            rel = path.relative_to(root)
            if not any(part.startswith(".") for part in rel.parts):
                matches.append(str(rel))
                if len(matches) >= 50:
                    break
                    
        if not matches:
            return f"No files matching pattern '{pattern}' found."
            
        return f"Found {len(matches)} matching files:\n" + "\n".join(matches)
    except Exception as e:
        return f"Error searching files by name: {str(e)}"

def list_dir(directory_path: str = ".") -> str:
    """
    List contents of a directory.
    
    Args:
        directory_path: Target directory path.
    """
    try:
        path = Path(directory_path).resolve()
        if not path.exists():
            return f"Error: Directory '{directory_path}' does not exist."
        if not path.is_dir():
            return f"Error: '{directory_path}' is a file, not a directory."
            
        output = [f"Contents of {path}:"]
        for item in sorted(list(path.iterdir()), key=lambda x: (not x.is_dir(), x.name.lower())):
            kind = "[DIR] " if item.is_dir() else "[FILE]"
            size = f" ({item.stat().st_size} bytes)" if item.is_file() else ""
            output.append(f"  {kind} {item.name}{size}")
        return "\n".join(output)
    except Exception as e:
        return f"Error listing directory '{directory_path}': {str(e)}"

def run_command(command_line: str, cwd: str = ".") -> str:
    """
    Execute terminal/shell commands with working directory support.
    
    Args:
        command_line: Shell command string to execute.
        cwd: Current working directory for execution.
    """
    try:
        work_dir = Path(cwd).resolve()
        result = subprocess.run(
            command_line,
            cwd=work_dir,
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
        return f"Error running command: {str(e)}"

ANTIGRAVITY_TOOLS = [
    view_file,
    replace_file_content,
    write_to_file,
    grep_search,
    find_by_name,
    list_dir,
    run_command
]
