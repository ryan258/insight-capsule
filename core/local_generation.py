# core/local_generation.py
import requests
import json
from typing import Optional, Literal
from core.exceptions import GPTGenerationError

RoleType = Literal["writing", "fact_check", "expander"]

class LocalGenerator:
    """Local LLM generator using Ollama or other local inference."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2"):
        self.base_url = base_url
        self.model = model
        self.session = requests.Session()
        
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
                print(f"[Local LLM] Generating with {self.model} (attempt {attempt + 1})")
                
                response = self._call_ollama(prompt, system_prompt, temperature)
                return response.strip()
                
            except Exception as e:
                print(f"[Local LLM Error] Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries:
                    raise GPTGenerationError(f"Local LLM failed after {max_retries + 1} attempts: {str(e)}")
    
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
        
        response = self.session.post(url, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "")
    
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
            return response.status_code == 200
        except:
            return False

class HybridGenerator:
    """Generator that can switch between local and external models."""
    
    def __init__(self, prefer_local: bool = True):
        self.prefer_local = prefer_local
        self.local_generator = None
        self.external_generator = None
        
        # Try to initialize local generator
        try:
            self.local_generator = LocalGenerator()
            if not self.local_generator.is_available():
                print("[Hybrid] Local LLM not available, will fall back to external")
                self.local_generator = None
        except Exception as e:
            print(f"[Hybrid] Could not initialize local generator: {e}")
        
        # Initialize external generator if needed
        if not self.local_generator or not self.prefer_local:
            try:
                from core.generation import GPTGenerator
                self.external_generator = GPTGenerator()
            except Exception as e:
                print(f"[Hybrid] Could not initialize external generator: {e}")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate using preferred method with fallback."""
        # Try local first if preferred and available
        if self.prefer_local and self.local_generator:
            try:
                return self.local_generator.generate(prompt, **kwargs)
            except Exception as e:
                print(f"[Hybrid] Local generation failed, trying external: {e}")
        
        # Fall back to external
        if self.external_generator:
            return self.external_generator.generate(prompt, **kwargs)
        
        raise GPTGenerationError("No working generators available")