from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from queue import Empty, Queue
import threading
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter.scrolledtext import ScrolledText

from .config import Config
from .git_client import get_staged_diff
from .ollama_client import OllamaClient
from .prompt import build_prompt


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / ".git-llm-review.toml"


@dataclass
class TaskResult:
    status: str
    diff: str | None = None
    output: str | None = None


class DiffReviewerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Local LLM Diff Reviewer")
        self.root.geometry("900x700")
        self.root.minsize(650, 450)

        self.repo_path = tk.StringVar(value=str(PROJECT_ROOT))
        self.status = tk.StringVar(value="Choose a repository and load its staged changes.")
        self.events: Queue[TaskResult] = Queue()
        self.busy = False

        self._build_ui()
        self.root.after(100, self._check_events)
        self.refresh_diff()

    def _build_ui(self):
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(container, text="Repository").pack(anchor=tk.W)
        repo_row = ttk.Frame(container)
        repo_row.pack(fill=tk.X, pady=(4, 10))

        self.repo_entry = ttk.Entry(repo_row, textvariable=self.repo_path)
        self.repo_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.browse_button = ttk.Button(repo_row, text="Browse...", command=self.choose_repository)
        self.browse_button.pack(side=tk.LEFT, padx=(8, 0))

        actions = ttk.Frame(container)
        actions.pack(fill=tk.X, pady=(0, 10))
        self.refresh_button = ttk.Button(actions, text="Refresh staged diff", command=self.refresh_diff)
        self.refresh_button.pack(side=tk.LEFT)
        self.review_button = ttk.Button(actions, text="Review staged changes", command=self.review_diff)
        self.review_button.pack(side=tk.LEFT, padx=(8, 0))

        panels = ttk.Panedwindow(container, orient=tk.VERTICAL)
        panels.pack(fill=tk.BOTH, expand=True)

        diff_panel = ttk.LabelFrame(panels, text="Staged diff")
        self.diff_text = ScrolledText(diff_panel, wrap=tk.NONE, height=12, state=tk.DISABLED)
        self.diff_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        panels.add(diff_panel, weight=1)

        result_panel = ttk.LabelFrame(panels, text="Review output")
        self.result_text = ScrolledText(result_panel, wrap=tk.WORD, height=12, state=tk.DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        panels.add(result_panel, weight=1)

        ttk.Label(container, textvariable=self.status, anchor=tk.W).pack(fill=tk.X, pady=(8, 0))

    def _set_text(self, widget: ScrolledText, text: str):
        widget.configure(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, text)
        widget.configure(state=tk.DISABLED)

    def choose_repository(self):
        selected = filedialog.askdirectory(
            title="Select a Git repository",
            initialdir=self.repo_path.get() or str(PROJECT_ROOT),
        )
        if selected:
            self.repo_path.set(selected)
            self.refresh_diff()

    def refresh_diff(self):
        self._start_task(self._load_diff, "Loading staged diff...")

    def review_diff(self):
        self._start_task(self._review_diff, "Sending request to Ollama...")

    def _load_diff(self, repo_path: str) -> TaskResult:
        diff = get_staged_diff(repo_path)
        if not diff:
            return TaskResult("No staged changes found. Stage files with git add, then refresh.", diff="")
        return TaskResult(f"Staged diff loaded ({len(diff):,} characters).", diff=diff)

    def _review_diff(self, repo_path: str) -> TaskResult:
        diff = get_staged_diff(repo_path)
        if not diff:
            return TaskResult("No staged changes found. Stage files with git add, then try again.", diff="")

        config = Config(CONFIG_PATH)
        prompt = build_prompt(diff, config.system_prompt)
        result = OllamaClient(config).generate_review(prompt)
        return TaskResult("Review complete.", diff=diff, output=result)

    def _start_task(self, operation: Callable[[str], TaskResult], running_status: str):
        if self.busy:
            return

        repo_path = self.repo_path.get()
        self.busy = True
        self._set_controls_enabled(False)
        self.status.set(running_status)

        def run():
            try:
                self.events.put(operation(repo_path))
            except Exception as exc:
                self.events.put(TaskResult(f"Error: {exc}", output=f"Operation failed:\n{exc}"))

        threading.Thread(target=run, daemon=True).start()

    def _set_controls_enabled(self, enabled: bool):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.refresh_button.configure(state=state)
        self.review_button.configure(state=state)
        self.browse_button.configure(state=state)
        self.repo_entry.configure(state=state)

    def _check_events(self):
        try:
            while True:
                result = self.events.get_nowait()
                self.busy = False
                self._set_controls_enabled(True)
                self.status.set(result.status)
                if result.diff is not None:
                    self._set_text(self.diff_text, result.diff or "No staged changes found.")
                if result.output is not None:
                    self._set_text(self.result_text, result.output)
        except Empty:
            pass
        self.root.after(100, self._check_events)


def main():
    root = tk.Tk()
    DiffReviewerApp(root)
    root.mainloop()
