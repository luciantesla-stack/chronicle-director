import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & CONFIGURATION ---
st.set_page_config(page_title="Chronicle Director", page_icon="🎬")
st.title("🎬 Chronicle: The Director")

# Get your API Key from https://aistudio.google.com/
# For local testing, you can paste it here; for deployment, use st.secrets
# This automatically grabs the key from your secrets.toml file
api_key = st.secrets["GEMINI_API_KEY"]

if api_key:
    genai.configure(api_key=api_key)
    
    # --- 2. THE DIRECTOR'S LOGIC (System Instruction) ---
    system_prompt = """
    You are the 'Chronicle Director.' Your goal is to unravel a user's life story 
    one sensory memory at a time. 
    1. Stay focused on ONE memory until it is cinematic.
    2. Ask about smells, sounds, and specific textures.
    3. Use the 'Director's Log' every 5 messages to summarize progress.
    4. Maintain a tone that is curious, philosophical, and slightly persistent.
    """

    # Initialize the model
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_prompt
    )

    # --- 3. SESSION MEMORY ---
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- 4. THE INTERACTION ---
    if prompt := st.chat_input("Tell me about a specific moment..."):
        # Display user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get AI response
        response = st.session_state.chat_session.send_message(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

else:
    st.warning("Please enter your Gemini API Key in the sidebar to begin.")