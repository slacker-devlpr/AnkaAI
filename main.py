from openai import OpenAI
import streamlit as st
import shelve
import time  # For simulating typing animation
from streamlit_katex import st_katex

st.set_page_config(
    page_title="Anka-AI, artificial intelligence for math",
    page_icon=r"Anka (1).png"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;700&display=swap');
    .custom-title {
        font-size: 36px;
        font-weight: bold;
        font-family: 'Raleway', sans-serif;
        background: linear-gradient(45deg, #ffffff, #000000); /* Gradient colors */
        background-size: 100% 150%;
        -webkit-background-clip: text;
        color: transparent; /* Make text transparent so the gradient shows */
        text-align: center; /* Align to the center */
    }
    </style>
    <div class="custom-title">Anka-AI</div>
    """,
    unsafe_allow_html=True,
)

st.text(" ")
st.text(" ")
st.text(" ")

USER_AVATAR = "👤"
BOT_AVATAR = r"Anka (1).png"
client = OpenAI(api_key='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')

with shelve.open("chat_history") as db:
    if "messages" in db:
        del db["messages"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Load or initialize chat history
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

# Typing animation function
def type_response(content):
    message_placeholder = st.empty()
    full_response = ""
    for char in content:
        full_response += char
        message_placeholder.markdown(full_response + "▌")
        time.sleep(0.005)  # Adjust typing speed as needed
    message_placeholder.markdown(full_response)  # Finalize the response

# Render Markdown and KaTeX for LaTeX support
def render_latex_and_text(content):
    st.markdown(content, unsafe_allow_html=True)
    if "$$" in content or r"\(" in content or r"\[" in content:
        st_katex(content)

# Load chat history if not already in session
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Add initial hello message if first visit
if not st.session_state.messages:
    initial_message = {
        "role": "assistant",
        "content": "Welcome to Anka-AI! As your dedicated math assistant, I'm here to provide expert guidance and support on a wide range of mathematical concepts. Whether
