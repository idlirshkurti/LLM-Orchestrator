"""Instentiate a chat-based language model from a given provider and run it with a given input text.

This file defines functions to instantiate different chat models
(e.g., OpenAI, Cohere, Ollama) based on the specified provider and model name.
"""

import logging
from dotenv import load_dotenv, find_dotenv

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_cohere.chat_models import ChatCohere
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI

# Load environment variables from the .env file
load_dotenv(find_dotenv())

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_chat_model(model_provider: str, model_name: str) -> BaseChatModel:
    """
    Returns a chat-based LLM model based on the specified provider and model name.

    Args:
        model_provider (str): The provider of the chat-based LLM model ('ollama', 'cohere', or 'openai').
        model_name (str): The name of the chat-based LLM model to use.

    Returns:
        BaseChatModel: An instance of the chat-based LLM model.
    """
    supported_providers = {
        'ollama': ChatOllama,
        'cohere': ChatCohere,
        'openai': ChatOpenAI
    }

    if model_provider not in supported_providers:
        logger.error("Invalid model provider: %s", model_provider)
        raise ValueError(f"Invalid model provider: {model_provider}")

    logger.info("Loading model: %s from provider: %s", model_name, model_provider)

    try:
        llm_class = supported_providers[model_provider]
        llm = llm_class(model=model_name, temperature=0.0)
        logger.info("Model loaded successfully.")
        return llm
    except Exception as e:
        logger.error("Failed to load model %s from provider %s: %s", model_name, model_provider, e)
        raise


def run(model_provider: str, model_name: str, input_text: str):
    """
    Loads a chat-based LLM model from the specified provider and runs it with the given input.

    Args:
        model_provider (str): The provider of the chat-based LLM model.
        model_name (str): The name of the chat-based LLM model to use.
        input_text (str): The input text to the model.
    """
    logger.info("Running model %s from provider %s with input: %s", model_name, model_provider, input_text)

    try:
        llm = get_chat_model(model_provider, model_name)
        output = llm.invoke(input_text)
        logger.info("Model output: %s", output.content)
        print(output.content)
    except Exception as e:
        logger.error("Error running model %s from provider %s: %s", model_name, model_provider, e)
        raise


if __name__ == '__main__':
    from fire import Fire
    Fire(run)
