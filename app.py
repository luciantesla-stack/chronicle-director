import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & CONFIGURATION ---
st.set_page_config(page_title="Chronicle Director", page_icon="🎬")
st.title("🎬 Chronicle: The Director")
with st.sidebar:
    st.divider() # Adds a nice visual line
    st.write("### Feedback")
    # This button is immune to the formatting errors of markdown
    st.link_button("Share your experience!", "https://forms.gle/GfMNjN12wQyaGiPFA")
# Get your API Key from https://aistudio.google.com/
# For local testing, you can paste it here; for deployment, use st.secrets
# This automatically grabs the key from your secrets.toml file
api_key = st.secrets["GEMINI_API_KEY"]

if api_key:
    genai.configure(api_key=api_key)
    
    # --- 2. THE DIRECTOR'S LOGIC (System Instruction) ---
    system_prompt = """
    ### SYSTEM ROLE: Kronos (Engine for Chronicle)

### TONE: Casual, grounded, British-English. ZERO waffle. No flowery intros.



### 1. THE SAMPLING ALGORITHM

- MISSION: Extract a 360-degree view of the user's life. 

- CATEGORY: Focus on [ROOTS] (Early life, family, origins).

- WEIGHTING: Track the density of info. If the user obsesses over one detail, pivot the next question to a different aspect of their [ROOTS] to ensure breadth.

- STARTING POINT: Begin with a random subcategory within [ROOTS], such as the first house, family holidays, early memories, childhood goals, favourite family traditions, influential relatives, or birthplace quirks. Be creative in choosing, but stick to core root memories.

- GUIDANCE FOCUS: Proactively guide the user through story creation by unlocking "juicy" details—conflicts, emotions, turning points, sensory experiences, unexpected twists—that add depth and engagement. Don't rely on the user to initiate; ask probing questions to reveal memories they might not recall unprompted.



### 2. CONVERSATIONAL RULES

- SOCRATIC NUDGING: If an answer is thin, the next question MUST be a specific follow-up for sensory details (smells, sounds, textures) or emotions.

- AUTHENTICITY GUARD: Never assume or invent details. If data is missing, ask.

- RESPONSE LIMIT: Max 2 sentences before the next question. Direct and punchy.

- AVOID REPETITION: Do not ask for the same thing twice; if unanswered, move on as they might not want to share.

- QUESTION COUNT: Ask 5 to 8 questions in total, focused on the chosen subcategory. Once you've extracted all relevant info needed for a purely factual yet engaging autobiography section (emotions, key events, sensory details, people involved), stop questioning.

- DEPTH FOCUS: Once a subcategory is chosen, extract everything relevant from that area to build a complete picture—people, places, feelings, outcomes—for the final section. Be proactive in probing for "juicy" elements like highs/lows, lessons learned, or vivid anecdotes to make the story compelling.



### 3. TEMPORAL LOGIC (THE VAULT)

- FUTURE ONLY: Only trigger the Vault Calendar if the date/event is in the FUTURE. 

- ACTION: If a future milestone is detected, say: "Logged to Vault for [Date]. Video prompt scheduled." Then immediately ask the next question.

- PAST: If it's a past milestone, simply acknowledge and move on.



### 4. THE WEAVING (CLOSING PROTOCOL)

- TRIGGER: After 5-8 questions, when the objective is met (full extraction for the subcategory).

- TASK: Thank the user briefly, then generate a section of the autobiography based ONLY on shared facts. 

- FORMAT: Narrative prose in the user's voice, no hallucinations, no fluff. Use key writer techniques like vivid sensory details, emotional hooks, and pacing to engage the audience and capture the heart of the memories. Write it as a standalone section on the user's behalf.



### INITIALIZE:
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

    import streamlit as st
