"""
Antigravity Artifacts Manager:
Handles creation, parsing, diff rendering, and markdown visualization for implementation plans and walkthroughs.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List

class Artifact:
    """Represents an Antigravity Structured Markdown Artifact."""
    
    def __init__(
        self,
        filename: str,
        title: str,
        content: str,
        user_facing: bool = True,
        request_feedback: bool = True,
        summary: str = ""
    ):
        self.filename = filename
        self.title = title
        self.content = content
        self.user_facing = user_facing
        self.request_feedback = request_feedback
        self.summary = summary

    def to_dict(self) -> Dict[str, Any]:
        return {
            "filename": self.filename,
            "title": self.title,
            "content": self.content,
            "user_facing": self.user_facing,
            "request_feedback": self.request_feedback,
            "summary": self.summary
        }

class ArtifactManager:
    """Manager for conversation artifacts in apta AI."""

    def __init__(self, storage_dir: str = ".artifacts"):
        self.storage_dir = Path(storage_dir).resolve()
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.artifacts: Dict[str, Artifact] = {}

    def create_artifact(
        self,
        filename: str,
        title: str,
        content: str,
        user_facing: bool = True,
        request_feedback: bool = True,
        summary: str = ""
    ) -> Artifact:
        artifact = Artifact(filename, title, content, user_facing, request_feedback, summary)
        self.artifacts[filename] = artifact
        
        # Save to disk
        file_path = self.storage_dir / filename
        file_path.write_text(content, encoding="utf-8")
        return artifact

    def get_artifact(self, filename: str) -> Optional[Artifact]:
        if filename in self.artifacts:
            return self.artifacts[filename]
        file_path = self.storage_dir / filename
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8", errors="replace")
            artifact = Artifact(filename, filename, content)
            self.artifacts[filename] = artifact
            return artifact
        return None

    def list_artifacts(self) -> List[Dict[str, Any]]:
        return [art.to_dict() for art in self.artifacts.values()]
