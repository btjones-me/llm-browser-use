import streamlit as st
import asyncio
import pprint
from example import get_llm, Agent
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# (Optional) Configure logging to a file
logging.basicConfig(filename='debug_output.log', level=logging.INFO)

st.title("Debug Agent Output")

# Text input for task
task = st.text_input(
    "Enter your task",
    placeholder="e.g., Go to Reddit, search for 'python', and get the first post title"
)

if st.button("Run Task and Print Debug Output"):
    if not task:
        st.error("Please enter a task first!")
    else:
        try:
            # Create agent (using a default model, adjust if needed)
            agent = Agent(
                task=task,
                llm=get_llm(os.getenv("LLM_TYPE", "gemini"))
            )
            
            with st.spinner("Running task..."):
                result = asyncio.run(agent.run())
                
                # Pretty-print the result
                pp = pprint.PrettyPrinter(indent=2)
                formatted_result = pp.pformat(result)
                
                # Show the result in a text area so you can copy it
                st.text_area("Debug Output (copy and paste this)", formatted_result, height=500)
                
                # Also log it to a file for further inspection
                logging.info("Agent run result:\n" + formatted_result)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
