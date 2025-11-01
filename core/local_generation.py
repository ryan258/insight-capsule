# core/local_generation.py
import requests
from typing import Optional, Literal, Union
from config.settings import LOCAL_LLM_URL, LOCAL_LLM_MODEL
from core.exceptions import GPTGenerationError
from core.logger import setup_logger

logger = setup_logger(__name__)

RoleType = Literal["writing", "fact_check", "expander"]


class LocalGenerator:
    """Local LLM generator using Ollama or other local inference."""

    def __init__(self, base_url: str = LOCAL_LLM_URL, model: str = LOCAL_LLM_MODEL):
        """
        Initialize local LLM generator.

        Args:
            base_url: Ollama API base URL
            model: Model name to use (e.g., llama3.2)
        """
        self.base_url = base_url
        self.model = model
        self.session = requests.Session()
        logger.info(f"LocalGenerator initialized: {base_url}, model={model}")
        
    def generate(self, 
                 prompt: str, 
                 role: RoleType = "writing",
                 temperature: float = 0.7,
                 system_prompt: Optional[str] = None,
                 max_retries: int = 2) -> str:
        """
        Generate text using local LLM.
        
        Args:
            prompt: User prompt
            role: Role (for potential model/prompt tuning)
            temperature: Sampling temperature
            system_prompt: Optional custom system prompt
            max_retries: Number of retries on failure
            
        Returns:
            Generated text
            
        Raises:
            GPTGenerationError: If generation fails after retries
        """
        if system_prompt is None:
            system_prompt = self._get_system_prompt_for_role(role)
        
        for attempt in range(max_retries + 1):
            try:
                logger.info(f"Generating with {self.model} (attempt {attempt + 1}/{max_retries + 1})")
                print(f"[Local LLM] Generating with {self.model} (attempt {attempt + 1})")

                response = self._call_ollama(prompt, system_prompt, temperature)
                logger.info(
                    f"Generation successful: {len(response)} characters, {len(response.split())} words"
                )
                return response.strip()

            except Exception as e:
                logger.warning(f"Generation attempt {attempt + 1} failed: {e}")
                print(f"[Local LLM Error] Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries:
                    error_msg = f"Local LLM failed after {max_retries + 1} attempts: {str(e)}"
                    logger.error(error_msg)
                    raise GPTGenerationError(error_msg)
    
    def _call_ollama(self, prompt: str, system_prompt: str, temperature: float) -> str:
        """Call Ollama API directly."""
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": f"{system_prompt}\n\nUser: {prompt}\nAssistant:",
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }

        response = self.session.post(url, json=payload, timeout=120)
        if response.status_code == 404:
            logger.info("Ollama /api/generate returned 404; retrying with /api/chat endpoint")
            return self._call_ollama_chat(prompt, system_prompt, temperature)
        response.raise_for_status()

        result = response.json()
        return self._extract_response_text(result)

    def _call_ollama_chat(self, prompt: str, system_prompt: str, temperature: float) -> str:
        """Fallback to the chat endpoint if /api/generate is unavailable."""
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "options": {"temperature": temperature}
        }
        response = self.session.post(url, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        return self._extract_response_text(result)

    @staticmethod
    def _extract_response_text(result: Union[dict, str]) -> str:
        """Normalize Ollama response payloads into plain text."""
        if isinstance(result, str):
            return result
        if not isinstance(result, dict):
            return ""

        if "response" in result:
            return result.get("response", "")

        message = result.get("message")
        if isinstance(message, dict):
            return message.get("content", "")

        return ""
    
    def _get_system_prompt_for_role(self, role: RoleType) -> str:
        """Get role-specific system prompts."""
        prompts = {
            "writing": "You are a concise, insightful writing assistant. Create clear, engaging content.",
            "fact_check": "You are a careful fact-checking assistant. Verify claims and note uncertainties.",
            "expander": "You are a creative assistant who helps structure and expand ideas clearly."
        }
        return prompts.get(role, prompts["writing"])
    
    def is_available(self) -> bool:
        """Check if the local LLM service is available."""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                logger.debug("Ollama availability check failed with status %s", response.status_code)
                return False

            tags = response.json().get("models", [])
            if not any(
                self.model == tag.get("name") or self.model == tag.get("model")
                for tag in tags
            ):
                logger.warning(
                    "Local LLM model '%s' is not present. Run 'ollama pull %s' or adjust LOCAL_LLM_MODEL.",
                    self.model,
                    self.model,
                )
                return False

            logger.debug("Ollama availability check succeeded and model '%s' is present", self.model)
            return True
        except Exception as e:
            logger.debug(f"Ollama not available: {e}")
            return False


class HybridGenerator:
    """Generator that can switch between local and external models."""

    def __init__(self, prefer_local: bool = True):
        """
        Initialize hybrid generator with local and/or external model support.

        Args:
            prefer_local: Whether to prefer local LLM over external
        """
        self.prefer_local = prefer_local
        self.local_generator = None
        self.external_generator = None
        logger.info(f"Initializing HybridGenerator (prefer_local={prefer_local})")

        # Try to initialize local generator
        try:
            self.local_generator = LocalGenerator()
            if not self.local_generator.is_available():
                logger.warning("Local LLM not available, will fall back to external")
                print("[Hybrid] Local LLM not available, will fall back to external")
                self.local_generator = None
            else:
                logger.info("Local LLM initialized and available")
        except Exception as e:
            logger.error(f"Could not initialize local generator: {e}")
            print(f"[Hybrid] Could not initialize local generator: {e}")

        # Initialize external generator if needed
        if not self.local_generator or not self.prefer_local:
            try:
                from core.generation import GPTGenerator

                self.external_generator = GPTGenerator()
                logger.info("External LLM (OpenAI) initialized")
            except Exception as e:
                logger.warning(f"Could not initialize external generator: {e}")
                print(f"[Hybrid] Could not initialize external generator: {e}")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate using preferred method with fallback.

        Args:
            prompt: Text prompt for generation
            **kwargs: Additional arguments passed to generator

        Returns:
            Generated text

        Raises:
            GPTGenerationError: If all generators fail
        """
        # Try local first if preferred and available
        if self.prefer_local and self.local_generator:
            try:
                logger.info("Using local LLM for generation")
                return self.local_generator.generate(prompt, **kwargs)
            except Exception as e:
                logger.warning(f"Local generation failed, trying external: {e}")
                print(f"[Hybrid] Local generation failed, trying external: {e}")

        # Fall back to external
        if self.external_generator:
            logger.info("Using external LLM (OpenAI) for generation")
            return self.external_generator.generate(prompt, **kwargs)

        error_msg = "No working generators available"
        logger.error(error_msg)
        raise GPTGenerationError(error_msg)
