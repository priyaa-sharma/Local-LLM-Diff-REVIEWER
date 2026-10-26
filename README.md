# Local-LLM-Diff-REVIEWER

A lightweight, automated code review tool that uses local LLMs (via Ollama) to analyze your git diffs. Improve your code quality without sending your data to external servers.

## Features

* **Privacy-Focused:** Runs locally on your machine using Ollama.
* **Automated:** Quickly identify bugs and formatting issues before you commit.
* **Actionable Feedback:** Returns structured JSON output for easy integration.

## Setup

### Prerequisites

1. Ensure [Ollama](https://ollama.com/) is installed.
2. Pull the required model: `ollama pull qwen2.5-coder` (or your preferred model).

### Installation

Clone the repository, create a virtual environment, and install the project dependencies:

```powershell
git clone https://github.com/priyaa-sharma/Local-LLM-Diff-REVIEWER.git
cd Local-LLM-Diff-REVIEWER
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

Python 3.11 or newer is required. The desktop interface uses Tkinter, which is included with most standard Python installations.

## Usage

1. Start Ollama and pull the configured model (by default, `qwen2.5-coder:7b`):

   ```powershell
   ollama pull qwen2.5-coder:7b
   ```

2. In the project folder, launch the GUI:

   ```powershell
   python -m src
   ```

3. Choose a Git repository in the window. Stage the changes you want reviewed (`git add <files>`), then select **Refresh staged diff** and **Review staged changes**. The diff and review appear in the two panels.

To continue using the command-line reviewer, run `python -m src.main` from the project folder.

## Configuration

You can customize the review process by editing the `.git-llm-review.toml` file in the root directory.