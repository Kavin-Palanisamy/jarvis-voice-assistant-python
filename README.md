# JARVIS AI System

A fully locally-integrated, production-grade AI assistant running natively on Windows.

## Overview
J.A.R.V.I.S. is built with Python handling intent classification, system automation, file management, web search, and OS manipulation locally.

## Setup Requirements

1. **Python 3.11+**
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment:
   Copy `.env.example` to `.env` and fill in your API keys (Gemini, OpenWeather).

## How to Run

1. **Main Loop (Interactive CLI):**
   ```bash
   python main.py
   ```
2. **Automated Test Suite:**
   ```bash
   python test_runner.py
   ```

## Architecture Map
- `main.py`: The async loop orchestrator.
- `ai_brain.py`: LLM intent parsing with J.A.R.V.I.S. persona injection.
- `command_parser.py`: Routing NLP output to actionable system task chains.
- `task_engine.py`: Executing the task chain steps safely.
- `memory_engine.py`: SQLite long-term storage and preferences.
