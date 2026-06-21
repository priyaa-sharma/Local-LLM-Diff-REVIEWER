# src/prompt.py
from jinja2 import Environment, FileSystemLoader

def build_prompt(diff: str, system_prompt: str) -> str:
    env = Environment(loader=FileSystemLoader("src/templates"))
    template = env.get_template("review.j2")
    return template.render(diff=diff, system_prompt=system_prompt)