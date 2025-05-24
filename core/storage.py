# /core/storage.py
import json # Not strictly needed now but kept for future if JSON output is desired for logs
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any # Dict, Any, Json might be less needed now
from config.settings import LOGS_DIR 
from core.exceptions import StorageError

class StorageManager:
    def __init__(self, logs_dir: Path = LOGS_DIR):
        """
        Initializes the StorageManager.
        Args:
            logs_dir: The directory where log files will be stored.
        """
        self.logs_dir = Path(logs_dir)
        self.index_file = self.logs_dir / "index.md"
        
        try:
            self.logs_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise StorageError(f"Failed to create storage directories: {e}")
    
    # save_brief method is removed as the creative brief step is eliminated.

    def save_log(self, 
                 title: str,
                 transcript: str,
                 capsule: str,
                 tags: Optional[List[str]] = None, # Made Optional for clarity
                 timestamp: Optional[datetime] = None) -> Path:
        """
        Saves the complete session log (transcript and capsule) to a Markdown file.
        The creative brief step has been removed from this workflow.

        Args:
            title: The title for the log entry.
            transcript: The transcribed text from the audio.
            capsule: The generated insight capsule.
            tags: Optional list of tags associated with the entry.
            timestamp: Optional timestamp for the log entry; defaults to now.

        Returns:
            Path to the saved log file.
        
        Raises:
            StorageError: If saving the log file fails.
        """
        if timestamp is None:
            timestamp = datetime.now()
        if tags is None:
            tags = []
        
        # Sanitize the title for use in a filename.
        safe_title = self._sanitize_filename(title)
        filename = f"{timestamp.strftime('%Y-%m-%d-%H%M%S')}-{safe_title}.md"
        filepath = self.logs_dir / filename
        
        # Format log content - Creative Brief section is removed.
        # Using ```text ... ``` for better multiline formatting of transcript.
        content = f"""# Insight Capsule Log — {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
**Title:** {title}
**Tags:** {' '.join(['#' + tag for tag in tags]) if tags else 'None'}

**Transcript:** ```text
{transcript.strip() if transcript and transcript.strip() else 'Transcript was empty.'}
```

**Insight Capsule:**
{capsule.strip() if capsule and capsule.strip() else 'Capsule was empty or generation failed.'}
"""
        try:
            filepath.write_text(content, encoding='utf-8')
        except Exception as e:
            raise StorageError(f"Failed to save log to {filepath}: {e}")
        
        # Update the main index file with this new log entry.
        # Ensure a valid title is passed for the index link.
        self._update_index(title if title and title.strip() else "Untitled Entry", filename, timestamp, tags)
        
        return filepath

    def _update_index(self, title: str, filename: str, timestamp: datetime, tags: List[str]):
        """
        Updates the main index.md file with a link to the newly created log.
        Entries are prepended to keep the newest at the top.

        Args:
            title: The title of the log entry (used for the link text).
            filename: The filename of the log file.
            timestamp: The timestamp of the log entry.
            tags: A list of tags associated with the log.
        """
        entry_tags_str = ' '.join(['#' + tag for tag in tags]) if tags else ''
        # Ensure title for link is not empty
        entry_link_text = title if title and title.strip() else "Untitled Entry"
        entry = f"- [{entry_link_text}](./{filename}) — {timestamp.strftime('%Y-%m-%d %H:%M:%S')} {entry_tags_str}\n"
        
        header = "# Capsule Log Index\n\n"
        
        try:
            if self.index_file.exists():
                current_content = self.index_file.read_text(encoding='utf-8')
                # Prepend new entry after header, ensuring header exists
                if current_content.startswith(header):
                    new_content = header + entry + current_content[len(header):]
                else: # If header is missing, or file is not empty but lacks header
                    new_content = header + entry + current_content 
                self.index_file.write_text(new_content, encoding='utf-8')
            else: # File does not exist, create with header and entry
                self.index_file.write_text(header + entry, encoding='utf-8')
                
        except Exception as e:
            print(f"[Storage Error] Failed to update index {self.index_file}: {e}. Attempting to append as fallback.")
            try:
                # Fallback: Append to the file.
                with self.index_file.open("a", encoding='utf-8') as f:
                    # Check if the file is empty (e.g., just created by open("a")) to write the header only once.
                    if f.tell() == 0: 
                        f.write(header)
                    f.write(entry)
            except Exception as e_append:
                print(f"[Storage Error] Fallback append to index also failed for {filename}: {e_append}")


    def _sanitize_filename(self, name: Optional[str]) -> str:
        """
        Converts a string to a safe format for use as a filename.
        Replaces spaces with hyphens, removes unsafe characters, and converts to lowercase.

        Args:
            name: The string to sanitize.

        Returns:
            A sanitized string suitable for a filename.
        """
        if not name or not name.strip(): 
            return "untitled" 
        
        # Remove characters that are not alphanumeric, whitespace, or hyphen
        safe_name = re.sub(r'[^\w\s-]', '', name)
        # Replace whitespace sequences with a single hyphen
        safe_name = re.sub(r'\s+', '-', safe_name)
        # Convert to lowercase
        safe_name = safe_name.lower()
        # Remove leading/trailing hyphens
        safe_name = safe_name.strip('-_')
        
        return safe_name if safe_name else 'untitled'

    def extract_tags_from_text(self, text: Optional[str]) -> List[str]:
        """
        Extracts hashtag-style tags (e.g., #example) from a given text.

        Args:
            text: The text to search for tags.

        Returns:
            A list of extracted tags (without the # symbol).
        """
        if not text: 
            return []
        return re.findall(r'#(\w+)', text)

