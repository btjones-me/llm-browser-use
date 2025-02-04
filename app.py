"""
# Browser Use Agent

A Streamlit-based web application that demonstrates autonomous browser automation using LLMs (Large Language Models). This application allows users to input natural language tasks, which are executed by a browser automation agent powered by either Google's Gemini or OpenAI's GPT-4.

## Key Features:
- User-friendly interface for entering tasks.
- Real-time feedback and visualization of browser actions.
- Support for both Gemini and OpenAI models.
- Debugging information available in an expander for detailed execution tracking.

## Main Components:
- `update_logs`: Function to update log messages in real-time.
- `speed_up_gif`: Function to speed up GIFs generated during browser actions.
- The main Streamlit application logic to handle user interactions and display results.
"""

import streamlit as st
from example import get_llm
from browser_use import Agent, Browser, BrowserConfig
import asyncio
from dotenv import load_dotenv
import os
import logging
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Set page config
st.set_page_config(
    page_title="Browser Use Agent",
    page_icon="🌐",
    layout="wide"
)

# Title
st.title("🌐 Browser Use Agent")

# Sidebar for settings
st.sidebar.title("Settings")

# Model selection in sidebar
model_type = st.sidebar.radio(
    "Select Model",
    options=["gemini", "openai"],
    format_func=lambda x: "Gemini 2.0 Flash " if x == "gemini" else "GPT-4 Turbo",
    index=0 if os.getenv("LLM_TYPE", "gemini").lower() == "gemini" else 1,
)

# Flag to indicate whether to use a browser instance in sidebar
USE_PERSONAL_çBROWSER = st.sidebar.checkbox("Use Browser Instance", value=False)

# Flag to indicate whether to use vision in sidebar
USE_VISION = st.sidebar.checkbox("Use Vision", value=False)

# Text input for task
task = st.text_input(
    "Enter your task",
    placeholder="e.g., Go to Reddit, search for 'python', and get the first post title"
)

# Containers for displaying output
final_result_container = st.empty()
agent_history_container = st.empty()
gif_container = st.empty()

def speed_up_gif(gif_path: str, speed_factor: int = 2):
    """Speed up GIF by reducing frame duration."""
    with Image.open(gif_path) as img:
        durations = []
        for frame in range(img.n_frames):
            img.seek(frame)
            durations.append(img.info.get('duration', 100))
        frames = []
        for frame in range(img.n_frames):
            img.seek(frame)
            frames.append(img.copy())
        output = io.BytesIO()
        frames[0].save(
            output,
            format='GIF',
            append_images=frames[1:],
            save_all=True,
            duration=[d // speed_factor for d in durations],
            loop=0
        )
        return output.getvalue()



if USE_PERSONAL_çBROWSER:
    # Configure the browser to connect to your Chrome instance
    browser = Browser(
        config=BrowserConfig(
            # Specify the path to your Chrome executable
            chrome_instance_path=os.getenv('CHROME_INSTANCE_PATH', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'),  # macOS path
        )
    )
else:
    browser = None

if st.button("Run Task", type="primary"):
    if not task:
        st.error("Please enter a task first!")
    else:
        # Clear previous outputs
        final_result_container.empty()
        agent_history_container.empty()
        gif_container.empty()

        # Create the agent with the selected model
        agent = Agent(
            task=task,
            llm=get_llm(model_type),
            use_vision=USE_VISION,
            browser=browser,
        )

        with st.spinner("Running task..."):
            try:
                # Run the agent and get its history object
                history = asyncio.run(agent.run())

                # Use the provided API methods to get details:
                urls = history.urls()  # List of visited URLs
                screenshots = history.screenshots()  # List of screenshot paths
                action_names = history.action_names()  # Names of executed actions
                extracted_content_list = history.extracted_content()  # Extracted content during execution
                errors = history.errors()  # Any errors that occurred
                model_actions = history.model_actions()  # All actions with their parameters

                # Use the last extracted content as the final result (if any)
                final_extracted = extracted_content_list[-1] if extracted_content_list else "No result"

                # Determine overall status: if there are errors, treat it as failure
                if errors and "done" not in action_names:
                    final_result_container.error(f"❌ Task Failed: {final_extracted}")
                else:
                    final_result_container.success(f"✅ Task Completed Successfully: {final_extracted}")

                # Display step-by-step details
                st.markdown("### Steps")
                # Determine the number of steps to display
                steps_count = max(
                    len(action_names),
                    len(extracted_content_list),
                    len(model_actions),
                    len(urls)
                )
                for i in range(steps_count):
                    st.markdown(f"#### Step {i+1}")
                    action = action_names[i] if i < len(action_names) else "N/A"
                    url = urls[i] if i < len(urls) else "N/A"
                    extracted = extracted_content_list[i] if i < len(extracted_content_list) else "N/A"
                    model_action = model_actions[i] if i < len(model_actions) else "N/A"
                    st.markdown(f"**Action:** {action}")
                    st.markdown(f"**URL:** {url}")
                    st.markdown(f"**Extracted Content:** {extracted}")
                    st.markdown(f"**Model Action:** {model_action}")
                    st.divider()

                # Full debug view in an expander
                with st.expander("Debug View"):
                    st.json({
                        "urls": urls,
                        "screenshots": screenshots,
                        "action_names": action_names,
                        "extracted_content": extracted_content_list,
                        "errors": errors,
                        "model_actions": model_actions,
                    })

                # Display the generated GIF if available
                if os.path.exists("agent_history.gif"):
                    gif_container.markdown("### Task Execution")
                    gif_bytes = speed_up_gif("agent_history.gif", speed_factor=2)
                    gif_container.image(gif_bytes, caption="Task execution steps (2x speed)")

            except Exception as e:
                final_result_container.error(f"❌ Task Failed: {str(e)}")
                if os.path.exists("agent_history.gif"):
                    gif_container.markdown("### Task Execution (Failed)")
                    gif_bytes = speed_up_gif("agent_history.gif", speed_factor=2)
                    gif_container.image(gif_bytes, caption="Task execution steps before failure (2x speed)")
                with st.expander("Debug View"):
                    st.error(str(e))
