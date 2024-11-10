"""Initializes tools that can be used by an agent.

This file defines and initializes tools (like the Python REPL and Tavily search)
that can be used by the agent for various actions, like searching the internet or running code snippets.
"""

import logging
from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.agents import Tool
from langchain_experimental.utilities import PythonREPL
from langchain_community.tools.tavily_search import TavilySearchResults

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_tools() -> List[Tool]:
    """
    Returns a list of tools that can be used by an agent.

    Returns:
        List[Tool]: List containing initialized tools.
    """
    tools = []

    try:
        internet_search = get_tabily_search_tool()
        repl_tool = get_python_interpreter_tool()

        tools.extend([internet_search, repl_tool])
        logger.info("Successfully initialized tools: %s", [tool.name for tool in tools])
    except Exception as e:
        logger.error("Error initializing tools: %s", e)
        raise

    return tools

def get_tabily_search_tool() -> Tool:
    """
    Returns a tool that performs internet search using the Tavily API.

    Returns:
        Tool: A TavilySearchResults tool for internet search.
    """
    try:
        internet_search = TavilySearchResults()
        internet_search.name = 'internet_search'
        internet_search.description = (
            'Returns a list of relevant document snippets for a textual query retrieved from the internet.'
        )

        class TavilySearchInput(BaseModel):
            query: str = Field(description='Query to search the internet with')

        internet_search.args_schema = TavilySearchInput
        logger.info("Initialized Tavily internet search tool.")
        return internet_search
    except Exception as e:
        logger.error("Failed to initialize Tavily search tool: %s", e)
        raise

def get_python_interpreter_tool() -> Tool:
    """
    Returns a tool that executes Python code and returns the result.

    Returns:
        Tool: A Python REPL tool for executing Python code.
    """
    try:
        python_repl = PythonREPL()
        repl_tool = Tool(
            name='python_interpreter',
            description=(
                'Executes Python code and returns the result. The code runs in a static sandbox without interactive mode.'
            ),
            func=python_repl.run,
        )

        class ToolInput(BaseModel):
            code: str = Field(description='Python code to execute.')

        repl_tool.args_schema = ToolInput
        logger.info("Initialized Python interpreter tool.")
        return repl_tool
    except Exception as e:
        logger.error("Failed to initialize Python interpreter tool: %s", e)
        raise
