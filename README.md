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

1. Clone this repository:
```bash
git clone https://github.com/priyaa-sharma/Local-LLM-Diff-REVIEWER.git
cd Local-LLM-Diff-REVIEWER

```



```
2. Set up your virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   # Activate it (Windows):
   .venv\Scripts\activate
   pip install -r requirements.txt

```

## Usage

Run the reviewer manually in your terminal:

```bash
python -m src

```

## Configuration

You can customize the review process by editing the `.git-llm-review.toml` file in the root directory.