"""Basic tests for core functionality."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from core.local_generation import LocalGenerator, HybridGenerator
from core.storage import StorageManager
from core.exceptions import GPTGenerationError, StorageError


class TestLocalGenerator:
    """Tests for LocalGenerator."""

    def test_initialization(self):
        """Test that LocalGenerator initializes correctly."""
        generator = LocalGenerator()
        assert generator.base_url == "http://localhost:11434"
        assert generator.model is not None

    def test_get_system_prompt_for_role(self):
        """Test that system prompts are returned for different roles."""
        generator = LocalGenerator()
        writing_prompt = generator._get_system_prompt_for_role("writing")
        assert "writing" in writing_prompt.lower() or "concise" in writing_prompt.lower()


class TestHybridGenerator:
    """Tests for HybridGenerator."""

    def test_initialization_prefer_local(self):
        """Test HybridGenerator initializes with local preference."""
        generator = HybridGenerator(prefer_local=True)
        assert generator.prefer_local is True

    def test_no_generators_raises_error(self):
        """Test that error is raised when no generators are available."""
        with patch.object(HybridGenerator, "__init__", lambda self, **kwargs: None):
            generator = HybridGenerator()
            generator.prefer_local = True
            generator.local_generator = None
            generator.external_generator = None

            with pytest.raises(GPTGenerationError):
                generator.generate("test prompt")


class TestStorageManager:
    """Tests for StorageManager."""

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        manager = StorageManager()

        assert manager._sanitize_filename("Hello World") == "hello-world"
        assert manager._sanitize_filename("Test@#$%File") == "testfile"
        assert manager._sanitize_filename("  spaces  ") == "spaces"
        assert manager._sanitize_filename("") == "untitled"
        assert manager._sanitize_filename(None) == "untitled"

    def test_extract_tags_from_text(self):
        """Test tag extraction from text."""
        manager = StorageManager()

        text = "This is a test #python #ai and some #testing"
        tags = manager.extract_tags_from_text(text)
        assert "python" in tags
        assert "ai" in tags
        assert "testing" in tags
        assert len(tags) == 3

    def test_extract_tags_empty_text(self):
        """Test tag extraction with empty text."""
        manager = StorageManager()
        assert manager.extract_tags_from_text("") == []
        assert manager.extract_tags_from_text(None) == []


def test_imports():
    """Test that all core modules can be imported."""
    from core import audio, transcription, local_generation, storage, logger, exceptions

    assert audio is not None
    assert transcription is not None
    assert local_generation is not None
    assert storage is not None
    assert logger is not None
    assert exceptions is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
