import nox

# Paths to the files and directories we want to check
code_files = ["llm-orchestrator", "tests", "noxfile.py"]

@nox.session
def install_deps(session):
    """Install dependencies using Poetry."""
    # Install poetry itself if not available
    session.run("pip", "install", "poetry", external=True)
    # Install project dependencies
    session.run("poetry", "install", external=True)

@nox.session
def run_agent(session):
    """Run the agent with chatgpt-3.5 and a specific query."""
    # Install dependencies if needed
    session.run("poetry", "install", external=True)
    # Define the command to run the agent
    session.run(
        "poetry",
        "run",
        "python",
        "llm-orchestrator/agent_executor.py",
        "--model_provider=openai",
        "--model_name=chatgpt-3.5",
        "--input=Your query here",
        external=True
    )

@nox.session
def lint(session):
    """Run mypy for type checking."""
    # Ensure dependencies are installed
    session.run("poetry", "install", external=True)
    # Run mypy type checks
    session.run("poetry", "run", "mypy", *code_files)

@nox.session
def format_code(session):
    """Format code with ruff."""
    # Ensure dependencies are installed
    session.run("poetry", "install", external=True)
    # Run ruff to format the code
    session.run("poetry", "run", "ruff", "--fix", *code_files)
