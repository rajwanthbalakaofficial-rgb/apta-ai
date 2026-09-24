"""
Antigravity Skills Engine:
Discovers, loads, and manages SKILL.md instruction skills.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional

class Skill:
    """Represents an Antigravity Skill with YAML frontmatter metadata."""
    
    def __init__(self, name: str, description: str, instructions: str, path: str):
        self.name = name
        self.description = description
        self.instructions = instructions
        self.path = path

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "instructions": self.instructions,
            "path": self.path
        }

class SkillsLoader:
    """Discovers and parses SKILL.md files in skills directories."""

    def __init__(self, skills_dir: Optional[str] = None):
        self.skills: Dict[str, Skill] = {}
        if skills_dir:
            self.load_skills(skills_dir)

    def load_skills(self, skills_dir: str):
        root = Path(skills_dir).resolve()
        if not root.exists():
            return

        for skill_file in root.rglob("SKILL.md"):
            try:
                text = skill_file.read_text(encoding="utf-8", errors="replace")
                name, desc, instructions = self._parse_skill_md(text, skill_file.parent.name)
                skill = Skill(name, desc, instructions, str(skill_file))
                self.skills[name] = skill
            except Exception:
                continue

    def _parse_skill_md(self, content: str, default_name: str) -> (str, str, str):
        name = default_name
        description = "Antigravity Skill Instruction"
        instructions = content

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                instructions = parts[2].strip()
                
                for line in frontmatter.splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        k = k.strip().lower()
                        v = v.strip().strip("'").strip('"')
                        if k == "name":
                            name = v
                        elif k == "description":
                            description = v
        return name, description, instructions

    def get_skills_summary(self) -> str:
        if not self.skills:
            return "No skills loaded."
            
        summary = ["Available Skills:"]
        for skill in self.skills.values():
            summary.append(f"- {skill.name}: {skill.description} ({skill.path})")
        return "\n".join(summary)
