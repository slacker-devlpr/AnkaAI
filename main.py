from openai import OpenAI
import streamlit as st
import shelve
import time

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
        background: linear-gradient(45deg, #ffffff, #000000);
        background-size: 100% 150%;
        -webkit-background-clip: text;
        color: transparent;
        text-align: center;
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
        time.sleep(0.005)
    message_placeholder.markdown(full_response)

# Function to render LaTeX using st.latex
def render_latex(text):
    parts = text.split("$$")
    for i, part in enumerate(parts):
        if i % 2 == 1:
            st.latex(part)
        else:
            st.markdown(part)

def display_messages(messages):
    for message in messages:
      avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
      with st.chat_message(message["role"], avatar=avatar):
          render_latex(message["content"])

# Load chat history if not already in session
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Add initial hello message if first visit
if not st.session_state.messages:
    initial_message = {
        "role": "assistant",
        "content": "Welcome to Anka-AI! As your dedicated math assistant, I'm here to provide expert guidance and support on a wide range of mathematical concepts. Whether you're solving complex equations or seeking to enhance your skills, let's work together to make math clear and engaging. Your journey to mathematical mastery starts here!"
    }
    st.toast("Anka-AI is still in Beta. Expect mistakes!", icon="👨‍💻")
    st.toast("You are currently running Anka-AI 1.0.4.", icon="⚙️")
    st.session_state.messages.append(initial_message)


# Display chat messages
display_messages(st.session_state.messages)
    

# Main chat interface
if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    system_message = {
        "role": "system",
        "content": (
            "You are an artificial intelligence that helps with math named Anka-AI. You were created by Gal Kokalj. "
            "When you respond with a mathematical formula, please enclose it in double dollar signs ($$). "
            "This will render the formula as LaTeX. For example, if you want to show the Pythagorean theorem "
            "you would write: '$$c^2 = a^2 + b^2$$'"
            "Make sure that only the mathematical formulas are surrounded by $$ and that you don't surround other text with it. "
            "Make sure to put the correct latex code around the math equation."
            "Do not use ( in anything from now on if you want to display anything latex(math for example) you surround the latex with $$. DO NOT USE ANY ( ANYWHERE THAT ISNT LATEX!!!"
        )
    }


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[system_message] + st.session_state.messages
    ).choices[0].message.content
    print(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        type_response(response)
    #save_chat_history(st.session_state.messages)

