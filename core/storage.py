import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from config.settings import LOGS_DIR, BRIEFS_DIR
from core.exceptions import StorageError

class StorageManager:
    def __init__(self, logs_dir: Path = LOGS_DIR, briefs_dir: Path = BRIEFS_DIR):
        self.logs_dir = Path(logs_dir)
        self.briefs_dir = Path(briefs_dir)
        self.index_file = self.logs_dir / "index.md"
        
        # Ensure directories exist
        try:
            self.logs_dir.mkdir(parents=True, exist_ok=True)
            self.briefs_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise StorageError(f"Failed to create storage directories: {e}")
    
    def save_brief(self, brief_data: Dict[str, Any], title: str, timestamp: Optional[datetime] = None) -> Path:
        """Save creative brief to JSON file."""
        if timestamp is None:
            timestamp = datetime.now()
        
        safe_title = self._sanitize_filename(title)
        filename = f"{timestamp.strftime('%Y-%m-%d-%H%M%S')}-{safe_title}-brief.json"
        filepath = self.briefs_dir / filename
        
        try:
            if isinstance(brief_data, dict):
                json_content = json.dumps(brief_data, indent=2, ensure_ascii=False)
            else:
                json.loads(brief_data)  # Validate
                json_content = brief_data
            
            filepath.write_text(json_content, encoding='utf-8')
            return filepath
            
        except Exception as e:
            raise StorageError(f"Failed to save brief to {filepath}: {e}")
    
    def save_log(self, 
                 title: str,
                 transcript: str,
                 brief: str,
                 capsule: str,
                 tags: List[str] = None,
                 timestamp: Optional[datetime] = None) -> Path:
        """Save complete session log."""
        if timestamp is None:
            timestamp = datetime.now()
        if tags is None:
            tags = []
        
        safe_title = self._sanitize_filename(title)
        filename = f"{timestamp.strftime('%Y-%m-%d-%H%M%S')}-{safe_title}.md"
        filepath = self.logs_dir / filename
        
        # Format log content
        content = f"""# Insight Capsule Log — {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
**Title:** {title}
**Tags:** {' '.join(['#' + tag for tag in tags]) if tags else 'None'}

**Transcript:** {transcript if transcript.strip() else 'Transcript was empty.'}

**Creative Brief:** {brief if brief else '{}'}

**Capsule:** {capsule if capsule.strip() else 'Capsule was empty.'}

**Insight Capsule** {capsule if capsule else 'Capsule generation failed or was empty.'}
"""
        filepath.write_text(content, encoding='utf-8')
        
        # Update index
        self._update_index(title, filename, timestamp, tags)
        
        return filepath

    def _update_index(self, title: str, filename: str, timestamp: datetime, tags: List[str]):
        """Update the index file with new entry."""
        entry_tags = ' '.join(['#' + tag for tag in tags]) if tags else ''
        entry = f"- [{title}](./{filename}) — {timestamp.strftime('%Y-%m-%d %H:%M:%S')} {entry_tags}\n"
        
        header = "# Capsule Log Index\n\n"
        
        try:
            if self.index_file.exists():
                content = self.index_file.read_text(encoding='utf-8')
                if content.startswith(header):
                    new_content = header + entry + content[len(header):]
                else:
                    new_content = header + entry + content
                self.index_file.write_text(new_content, encoding='utf-8')
            else:
                self.index_file.write_text(header + entry, encoding='utf-8')
                
        except Exception as e:
            print(f"[Storage Error] Failed to update index: {e}")

    def _sanitize_filename(self, name: str) -> str:
        """Convert string to safe filename."""
        safe = re.sub(r'[^\w\s-]', '', name.lower())
        safe = re.sub(r'[\s-]+', '-', safe).strip('-_')
        return safe or 'untitled'

    def extract_tags_from_text(self, text: str) -> List[str]:
        """Extract hashtags from text."""
        return re.findall(r'#(\w+)', text)
