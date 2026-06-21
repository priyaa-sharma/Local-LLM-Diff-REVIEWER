# src/__init__.py
from .config import Config
from .diff_parser import get_staged_diff
from .ollama_client import OllamaClient
from .prompt import build_prompt
from .response_parser import parse_response
from .formatter import print_review

def main():
    config = Config()
    diff = get_staged_diff()
    
    if not diff:
        print("No staged changes found.")
        return

    client = OllamaClient(config)
    prompt = build_prompt(diff, config.system_prompt)
    raw_response = client.generate_review(prompt)
    
    result = parse_response(raw_response)
    print_review(result)

if __name__ == "__main__":
    main()