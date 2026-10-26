from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def build_prompt(diff: str, system_prompt: str) -> str:
    template_dir = Path(__file__).resolve().parent / "templates"
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("review.j2")
    return template.render(diff=diff, system_prompt=system_prompt)