""" 
Module for demonstrating the use of Large Language Models (LLMs) with browser automation.

This module provides functionality to set up Google Cloud authentication and select the appropriate LLM model (either OpenAI or Gemini) based on user preferences. It includes a main function that executes a sample task using the selected LLM and prints the result.

Key Functions:
- setup_google_auth: Initializes Google Cloud credentials for Gemini model.
- get_llm: Returns the appropriate LLM instance based on the specified model type.
- main: Executes a sample browser automation task using the selected LLM.
"""

import os
from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
from google.oauth2 import service_account
import google.cloud.aiplatform as aiplatform

# Load environment variables
load_dotenv()

def setup_google_auth():
    """Initialize Google Cloud credentials"""
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    aiplatform.init(credentials=credentials)

def get_llm(model_type: Literal["openai", "gemini"] = "gemini"):
    """Factory function to get the appropriate LLM based on type"""
    if model_type == "openai":
        return ChatOpenAI(model="gpt-4o")
    elif model_type == "gemini":
        setup_google_auth()
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            convert_system_message_to_human=True
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")

async def main():
    # Get model type from environment variable, default to gemini
    model_type = os.getenv("LLM_TYPE", "gemini").lower()
    
    agent = Agent(
        task="Go to Reddit, search for 'browser-use', click on the first post and return the first comment.",
        llm=get_llm(model_type),
    )
    result = await agent.run()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())