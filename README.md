# Browser Use Project

A Streamlit-based web application that demonstrates autonomous browser automation using LLMs (Large Language Models). The project leverages either Gemini Flash 2.0 or GPT-4 Turbo to perform browser-based tasks through natural language instructions.

## Features

- 🤖 Autonomous browser automation using natural language commands
- 🔄 Real-time visualization of browser actions through GIF generation
- 🎯 Step-by-step progress tracking with detailed goal evaluation
- 🔀 Support for both Google's Gemini Flash 2.0 and OpenAI's GPT-4 Turbo
- 📊 Debug view for detailed execution information
- 🎨 Clean and intuitive Streamlit interface

## Prerequisites

- Python 3.12 or higher
- Google Cloud credentials (for Gemini) or OpenAI API key (for GPT-4)
- Environment variables properly configured
- `uv` package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd browser-use-project
   ```

2. Create and activate a virtual environment with uv:
   ```bash
   uv venv
   ```

3. Install dependencies using uv:
   ```bash
   uv install
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your API keys and credentials
   ```bash
   cp .env.example .env
   ```

## Configuration

Create a `.env` file with the following variables:
```env
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json  # For Gemini
OPENAI_API_KEY=your-openai-key  # For GPT-4
LLM_TYPE=gemini  # or 'openai'
```

## Usage

1. Start the Streamlit application:
   ```bash
   uv run streamlit run app.py
   ```

2. Select your preferred model (Gemini Flash 2.0 or GPT-4 Turbo)

3. Enter your task in natural language (e.g., "Go to Reddit, search for 'python', and get the first post title")

4. Click "Run Task" and watch the agent perform the requested actions

## Task Execution GIF

Here's a GIF demonstrating the task execution process:

![Task Execution](agent_history.gif)

## Project Structure

- `app.py`: Main Streamlit application
- `example.py`: Example usage and LLM configuration
- `pyproject.toml`: Project dependencies and configuration
- `.env`: Environment variables (not tracked in git)
- `.env.example`: Template for environment variables

## Dependencies

- `browser-use`: Core browser automation library
- `streamlit`: Web interface
- `playwright`: Browser automation
- `google-generativeai`: Gemini API integration
- `langchain`: LLM framework integration
- `Pillow`: Image processing for GIF generation
