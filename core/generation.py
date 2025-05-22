from openai import OpenAI
from typing import Optional, Literal
from config.settings import OPENAI_API_KEY, GPT_MODELS, DEFAULT_TEMPERATURE
from core.exceptions import GPTGenerationError

RoleType = Literal["writing", "fact_check", "expander"]

class GPTGenerator:
    def __init__(self, api_key: str = OPENAI_API_KEY):
        if not api_key:
            raise GPTGenerationError("OpenAI API key not provided")
        self.client = OpenAI(api_key=api_key)
        self.models = GPT_MODELS
    
    def generate(self, 
                 prompt: str, 
                 role: RoleType = "writing",
                 temperature: float = DEFAULT_TEMPERATURE,
                 system_prompt: Optional[str] = None,
                 max_retries: int = 2) -> str:
        """
        Generate text using GPT.
        
        Args:
            prompt: User prompt
            role: Role determining which model to use
            temperature: Sampling temperature
            system_prompt: Optional custom system prompt
            max_retries: Number of retries on failure
            
        Returns:
            Generated text
            
        Raises:
            GPTGenerationError: If generation fails after retries
        """
        model = self.models.get(role, self.models["writing"])
        
        if system_prompt is None:
            system_prompt = "You are a precise, thoughtful assistant."
        
        for attempt in range(max_retries + 1):
            try:
                print(f"[GPT] Generating with model {model} (attempt {attempt + 1})")
                
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature
                )
                
                content = response.choices[0].message.content.strip()
                return content
                
            except Exception as e:
                print(f"[GPT Error] Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries:
                    raise GPTGenerationError(f"Failed after {max_retries + 1} attempts: {str(e)}")