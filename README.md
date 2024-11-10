# LLM-Orchestrator

LLM-Orchestrator is a Python-based toolkit for running and managing interactive language model agents. It provides a flexible structure for executing multi-hop, tool-assisted language models using providers such as OpenAI's ChatGPT and Cohere's models. This repository is designed to streamline the process of configuring and deploying query-driven agents, complete with tool support for specialized functions such as code execution and internet search.

## Features

- **Multi-hop Agent Execution**: Run complex, multi-step agents with customizable reasoning paths.
- **Support for Multiple LLM Providers**: Easily switch between providers like OpenAI and Cohere.
- **Flexible Tool Integrations**: Use tools such as Python REPL for code execution and TavilySearch for web queries.
- **Modular Architecture**: Well-organized modules for agent execution, tool initialization, and model selection.
- **Nox-Powered Workflows**: Automated sessions for dependency management, code formatting, type checking, and testing.

## Repository Structure

```plaintext
LLM-Orchestrator/
├── live_llm/
│   ├── __init__.py            # Initialization file for live_llm package
│   ├── agent_executor.py      # Main script to run the agent
│   ├── chat_model_factory.py  # Factory function for creating chat models
│   └── tools_initializer.py   # Script to initialize agent tools
├── tests/                     # Unit tests for LLM-Orchestrator
├── README.md                  # Project documentation
├── pyproject.toml             # Project dependencies and configuration
└── noxfile.py                 # Nox automation script
```

## Getting Started

### Prerequisites

- **Python 3.8+**
- **Poetry** for dependency management
- **Nox** for task automation

Install Poetry and Nox if you haven't already:

```bash
pip install poetry nox
```

### Installation

Clone the repository and navigate to the project root:

```bash
git clone https://github.com/yourusername/LLM-Orchestrator.git
cd LLM-Orchestrator
```

Install the dependencies using Poetry:

```bash
poetry install
```

### Usage

The repository uses a Nox-based automation system for various tasks, including agent execution, linting, and type checking. Below are some useful commands.

#### Run the Agent with a Query

To run the agent using ChatGPT-3.5 or another specified model, use the following command:

```bash
nox -s run_agent
```

This will execute the agent with a predefined query. You can modify the query and model settings in the `noxfile.py`.

#### Code Linting and Formatting

Check types and format code with:

```bash
nox -s lint
nox -s format_code
```

#### Running All Tasks

To run all tasks sequentially:

```bash
nox
```

### Example Code

Here’s an example of how you might run the agent in a Python script directly:

```python
from live_llm.agent_executor import run

# Example query and model setup
model_provider = "openai"
model_name = "chatgpt-3.5"
query = "What is the capital of France?"

# Run the agent
run(model_provider, model_name, query)
```

### Configuring the Agent

The `agent_executor.py` script uses `get_react_agent_executor` to configure the agent’s logic based on the specified LLM provider. It also loads tools dynamically via `tools_initializer.py`, allowing for internet searches and code execution.

### Testing

Unit tests are in the `tests/` directory. To run tests, use:

```bash
pytest tests/
```

## Development

This project follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style, with `ruff` for code formatting and `mypy` for type checking.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to suggest improvements.
