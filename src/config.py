# src/config.py
import tomllib
from pathlib import Path

class Config:
    def __init__(self, config_path=".git-llm-review.toml"):
        with open(config_path, "rb") as f:
            self.data = tomllib.load(f)
            
    @property
    def model(self):
        return self.data.get("model", "qwen2.5-coder:7b")
        
    @property
    def api_base(self):
        return self.data.get("api_base", "http://localhost:11434")

    @property
    def system_prompt(self):
        return self.data.get("system_prompt", "")