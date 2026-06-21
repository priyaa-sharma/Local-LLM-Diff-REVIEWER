# src/main.py
from .config import Config
from .git_client import get_staged_diff
from .ollama_client import OllamaClient
from .prompt import build_prompt
from .response_parser import parse_response

def main():
    # 1. Setup
    config = Config()
    client = OllamaClient(config)
    
    diff = get_staged_diff()
    if not diff:
        print("No staged changes found.")
        return

    # 3. Build prompt and get review
    prompt = build_prompt(diff, "Review this code for bugs and style.")
    print("Sending request to Ollama...")
    raw_response = client.generate_review(prompt)
    
    # 4. Parse and display result
    print("--- Review Results ---")
    print(raw_response)

if __name__ == "__main__":
    main()