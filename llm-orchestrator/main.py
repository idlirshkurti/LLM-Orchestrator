"""Run the agent with chatgpt-3.5 and a specific query.

Usage: nox -s run_agent
"""

import sys
import logging
from live_llm.chat_model_factory import get_chat_model
from live_llm.agent_executor import get_react_agent_executor
from live_llm.tools_initializer import get_tools
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main(query: str):
    """
    Runs the LLM agent with the given query and outputs the result.

    Args:
        query (str): The input query to run through the agent.
    """
    # Define model provider and model name
    model_provider = "openai"   # Example: 'openai' for ChatGPT
    model_name = "gpt-3.5-turbo"  # Example: ChatGPT-3.5 model

    logger.info("Initializing chat model...")
    llm = get_chat_model(model_provider, model_name)

    logger.info("Initializing tools...")
    tools = get_tools()

    logger.info("Setting up the agent executor...")
    agent_executor = get_react_agent_executor(llm, tools, model_provider)

    logger.info(f"Running query: {query}")
    response = agent_executor.invoke({'input': query})
    print("Agent Response:", response.content)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_model.py '<your query here>'")
        sys.exit(1)

    # Retrieve the query from the command-line arguments
    query = sys.argv[1]
    main(query)
