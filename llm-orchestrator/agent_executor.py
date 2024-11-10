""" Set up agent executor.

This file handles setting up and running a "multi-hop React agent" with an agent executor,
using different chat model providers (e.g., Cohere, OpenAI).
"""

import logging
from typing import List

from dotenv import find_dotenv, load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_cohere.react_multi_hop.agent import create_cohere_react_agent

from src.tools import get_tools, Tool
from src.models import get_chat_model

# Load environment variables from the .env file
load_dotenv(find_dotenv())

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_react_agent_executor(
    llm: BaseChatModel,
    tools: List[Tool],
    model_provider: str
) -> AgentExecutor:
    """
    Returns an agent executor that can execute a multi-hop react agent.
    If the model_provider is 'cohere', the agent will be created using the Cohere API.

    Args:
        llm (BaseChatModel): The chat-based LLM model to use.
        tools (List[Tool]): A list of tools that can be used by the agent.
        model_provider (str): The provider of the chat-based LLM model.

    Returns:
        AgentExecutor: An agent executor that can execute a multi-hop react agent.
    """
    logger.info("Creating React agent executor with model provider: %s", model_provider)
    
    try:
        if model_provider == 'cohere':
            prompt = ChatPromptTemplate.from_template("{input}")
            logger.info("Using Cohere model with custom prompt.")
            agent = create_cohere_react_agent(
                llm=llm,
                tools=tools,
                prompt=prompt,
            )
        else:
            prompt = hub.pull('hwchase17/react')
            logger.info("Using LangChain hub model with predefined prompt.")
            agent = create_react_agent(
                llm=llm,
                tools=tools,
                prompt=prompt,
            )

        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True
        )
        logger.info("Agent executor created successfully.")
        return agent_executor
    except Exception as e:
        logger.error("Error creating agent executor: %s", e)
        raise


def run(
    model_provider: str,
    model_name: str,
    input_text: str
):
    """
    Creates an agent executor that can execute a multi-hop react agent, using the
    specified model, and runs the agent with the given input.

    Args:
        model_provider (str): The provider of the chat-based LLM model.
        model_name (str): The name of the chat-based LLM model to use.
        input_text (str): The input text to the agent.
    """
    logger.info("Running agent with model provider: %s and model name: %s", model_provider, model_name)
    
    try:
        llm = get_chat_model(model_provider, model_name)
        logger.info("Loaded chat model: %s", model_name)

        tools = get_tools()
        logger.info("Loaded tools for the agent.")

        agent_executor = get_react_agent_executor(llm, tools, model_provider)

        logger.info("Executing agent with input: %s", input_text)
        result = agent_executor.invoke({'input': input_text})
        logger.info("Execution complete. Result: %s", result)

    except Exception as e:
        logger.error("An error occurred during execution: %s", e)
        raise


if __name__ == '__main__':
    from fire import Fire
    Fire(run)
