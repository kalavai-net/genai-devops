import json

from audiorecorder import audiorecorder
import streamlit as st
from openai import OpenAI

import genie.tools.autopilot_tools as tools

from audio_utils import speech_to_text


def get_audio_input():
    audio = audiorecorder("Click to record", "Click to stop recording")

    if len(audio) > 0:
        st.session_state.audio = audio.export().read()

    if st.session_state.audio is not None:
        text = speech_to_text(st.session_state.audio, st.session_state.openai_config["base_url"], st.session_state.openai_config["api_key"])
        st.session_state.audio = None
        return text
    return None

AVATAR_IMAGE = "img/iPhone.png"

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": (
                "You are a helpful assistant. "
                "You have access to tools and must never guess or assume values for tool parameters. "
                "If a required parameter is missing, ask the user for it explicitly before using the tool."
            )}
        ]
    
    # Initialize OpenAI configuration in session state
    if "openai_config" not in st.session_state:
        st.session_state.openai_config = {
            "base_url": "https://api.cogenai.kalavai.net",
            "api_key": "sk--BnVfdA8bKzGPjr-JWYlzw",
            "model": "qwen-qwen2-5-7b-instruct-awq"
        }
    # Initialize tool call state
    if "pending_tool_call" not in st.session_state:
        st.session_state.pending_tool_call = None

    if "audio" not in st.session_state:
        st.session_state.audio = None

def get_openai_client():
    return OpenAI(
        base_url=st.session_state.openai_config["base_url"],
        api_key=st.session_state.openai_config["api_key"]
    )

def get_tool_params(name):
    for tool in tools.TOOLS:
        if tool['function']['name'] == name:
            return tool['function']['parameters']['required']
    return []


def process_tool_call(tool_call):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    
    # Check if all required arguments are present
    missing_params = []
    for param in get_tool_params(name):
        if param not in args or not args[param]:
            missing_params.append(param)
    
    if missing_params:
        return None, missing_params
    
    # Call the tool
    fn = getattr(tools, name)
    result = fn(**args)
    return result, None

def clear_chat_history():
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are a helpful assistant. "
            "You have access to tools and must never guess or assume values for tool parameters. "
            "If a required parameter is missing, ask the user for it explicitly before using the tool."
        )}
    ]

def main():
    # Add banner with logo
    st.image("img/logo.png", width=1500)
    
    st.title(":female_genie: I'm Genie, how can I help you?")
    badges = [
        ("Online", ":material/thumb_up:")
    ]
    cols = st.columns(len(badges))
    for i in range(len(badges)):
        with cols[i]:
            st.badge(badges[i][0], icon=badges[i][1])
    st.markdown("_Get GenAI-ops out of the way. Just say __'deploy a new model'__ or __'add 2 GPUs to my pool'__ to get Genie work for you_")
    st.markdown("---")
    
    initialize_session_state()
    
    # Sidebar configuration
    with st.sidebar:
        st.header("OpenAI Configuration")
        
        # Base URL configuration
        base_url = st.text_input(
            "Base URL",
            value=st.session_state.openai_config["base_url"],
            help="The base URL for the OpenAI API"
        )
        
        # API Key configuration
        api_key = st.text_input(
            "API Key",
            value=st.session_state.openai_config["api_key"],
            type="password",
            help="Your OpenAI API key"
        )
        
        # Model selection
        model = st.text_input(
            "Model",
            value=st.session_state.openai_config["model"],
            help="The model to use for completions"
        )
        
        # Update configuration if changed
        if (base_url != st.session_state.openai_config["base_url"] or
            api_key != st.session_state.openai_config["api_key"] or
            model != st.session_state.openai_config["model"]):
            st.session_state.openai_config.update({
                "base_url": base_url,
                "api_key": api_key,
                "model": model
            })
        
        # Add a separator
        st.divider()
        
        # Clear history button
        if st.button("Clear Chat History", type="primary"):
            clear_chat_history()
            st.rerun()
        
        st.divider()

        st.markdown("# Models by CoGen AI")
        st.image("img/qrcode.png")
        st.markdown("## Sign up for unlimited inference")
        
    client = get_openai_client()
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] != "system":
            avatar = AVATAR_IMAGE if message["role"] == "assistant" else None
            with st.chat_message(message["role"], avatar=avatar):
                st.write(message["content"])
    
    # Handle pending tool call if exists
    if st.session_state.pending_tool_call:
        tool_call = st.session_state.pending_tool_call
        st.write(f"I'm about to call the tool: {tool_call.function.name}")
        st.write("Arguments:", json.loads(tool_call.function.arguments))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirm", type="primary"):
                result, missing_params = process_tool_call(tool_call)
                if missing_params:
                    for param in missing_params:
                        st.write(f"Can you please provide the {param}?")
                else:
                    #st.write(result)
                    response = client.chat.completions.create(
                        model=st.session_state.openai_config["model"],
                        messages=[
                            {"role": "system", "content": (
                                "Given the following context:"
                                f"{result}"
                                "Address the user query: "
                                f"{st.session_state.messages[-1]['content']}"
                            )}
                        ]
                    )
                    st.session_state.messages.append({"role": "assistant", "content": result})
                    #st.write(response.choices[0].message.content)
                    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
                    #
                st.session_state.pending_tool_call = None
                st.rerun()
        
        with col2:
            if st.button("Cancel"):
                st.session_state.pending_tool_call = None
                st.rerun()
    
    # Chat input
    prompt = None
    if text_input:= st.chat_input("What would you like to know?"):
        prompt = text_input
    # if audio_input := get_audio_input():
    #     prompt = audio_input
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get assistant response
        with st.chat_message("assistant", avatar=AVATAR_IMAGE):
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model=st.session_state.openai_config["model"],
                    messages=st.session_state.messages,
                    tools=tools.TOOLS,
                    tool_choice="auto"
                )
                
                reply = response.choices[0].message
                
                if reply.tool_calls:
                    # Store the first tool call for confirmation
                    print("-->", reply.tool_calls)
                    st.session_state.pending_tool_call = reply.tool_calls[0]
                    st.rerun()
                else:
                    st.write(reply.content)
                    st.session_state.messages.append({"role": "assistant", "content": reply.content})

if __name__ == "__main__":
    main() 