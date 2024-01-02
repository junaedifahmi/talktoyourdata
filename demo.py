import streamlit as st
import time

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from agent import AgenPintarUpdate
from tools import df_tools


st.title("Talk to Your Data")
st.text("Demo apps of Techincal Test for Sr. AI Developer Job Vacancy. \nThe code is provided and developed by Junaedi Fahmi")

# Initialize agent
system_prompt = """
        use provided tools to answer the question.
"""
agen = AgenPintarUpdate(system_prompt=system_prompt, tools=[df_tools], verbose=False)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response_msg = agen(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in response_msg.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        # st.json(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_msg})