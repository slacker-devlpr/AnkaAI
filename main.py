from openai import OpenAI
import streamlit as st
import shelve
import time  # For simulating typing animation

st.set_page_config(
    page_title="Anka-AI, artificial inteligence for math",
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
        message_placeholder.markdown(full_response + "/")
        time.sleep(0.005)  # Adjust typing speed as needed
    message_placeholder.markdown(full_response)  # Finalize the response

# Load chat history if not already in session
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Add initial hello message if first visit
if not st.session_state.messages:
    initial_message = {
        "role": "assistant",
        "content": "Hello! Welcome to **Petra-AI**. Please note that **Petra-AI** can make mistakes. **Petra-AI** is powered by **OpenAI**, ensuring that it provides comprehensive answers, but it's always a good idea to double-check."
    }
    st.toast("Petra-AI is still in Beta. Expect mistakes!", icon="👨‍💻")
    st.toast("You are currently running Petra-AI 2.3.", icon="⚙️")
    st.session_state.messages.append(initial_message)

# Display chat messages
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Main chat interface
if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    # Direct response without search functionality
    system_message = {
        "role": "system",
        "content": (
            "You are Petra-AI, a helpful chatbot. All people described are from Slovenia, so conjugate the names as they would be in Slovenia. Anka Katrasnik was a computer science teacher of Gal Kokalj in 6th and 7th grade in the school OŠ Koseze. She is very smart and intelligent. You are running version 2.3. You were designed by Gal Kokalj, also known as Slacker. Your job is to provide helpful and accurate responses."
        )
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[system_message] + st.session_state.messages
    ).choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        type_response(response)
