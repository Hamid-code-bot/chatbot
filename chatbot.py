import streamlit as st
from litellm import completion
# import os  # No longer strictly needed if not using os.getenv

# --- Set your API key directly in the code (NOT RECOMMENDED FOR PRODUCTION) ---
GOOGLE_API_KEY = "AIzaSyAIN0ZmIiSkRkb0h2y0PIp3YBM0p_N9lV8"

if not GOOGLE_API_KEY:
    st.error("Please set your Google API key in the code!")
    st.stop()

# --- Initialize Streamlit session state for conversation ---
st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("🤖 Hamid's Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display chat messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User input ---
user_prompt = st.chat_input("Say something...")

if user_prompt:
    # Add user's message to session
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # --- Generate Gemini response ---
    try:
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=st.session_state.messages,
            api_key=GOOGLE_API_KEY
        )
        bot_reply = response['choices'][0]['message']['content']
    except Exception as e:
        bot_reply = f"❌ Error: {e}"

    # Display and save bot's response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
