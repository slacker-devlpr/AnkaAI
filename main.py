import streamlit as st
import shelve
import time  # For simulating typing animation
from openai import OpenAI

st.set_page_config(
    page_title="Anka-AI, artificial intelligence for math",
    page_icon=r"Anka (1).png"
)
st.latex("\documentclass{article}
\usepackage{amsmath}

\begin{document}

\title{Derivation of the Quadratic Formula}
\author{Anka-AI}
\date{\today}
\maketitle

The quadratic formula is used to find the solutions of a quadratic equation of the form:

\[
ax^2 + bx + c = 0
\]

where \(a \neq 0\). To derive the quadratic formula, we start by completing the square:

1. Divide the entire equation by \(a\):

\[
x^2 + \frac{b}{a} x + \frac{c}{a} = 0
\]

2. Rearranging gives:

\[
x^2 + \frac{b}{a} x = -\frac{c}{a}
\]

3. Next, we complete the square on the left side:

\[
x^2 + \frac{b}{a} x + \left(\frac{b}{2a}\right)^2 = -\frac{c}{a} + \left(\frac{b}{2a}\right)^2
\]

4. This simplifies to:

\[
\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}
\]

5. Taking the square root of both sides, we have:

\[
x + \frac{b}{2a} = \pm \frac{\sqrt{b^2 - 4ac}}{2a}
\]

6. Finally, isolating \(x\) gives us the quadratic formula:

\[
x = -\frac{b}{2a} \pm \frac{\sqrt{b^2 - 4ac}}{2a}
\]

Thus, the solutions for \(x\) are:

\[
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
\]

\end{document}")
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
        message_placeholder.markdown(full_response + "_")
        time.sleep(0.005)  # Adjust typing speed as needed
    message_placeholder.markdown(full_response)  # Finalize the response

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
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        if "LaTeX:" in message["content"]:
            st.latex(message["content"].replace("LaTeX:", ""))
        else:
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
            "You are an artificial intelligence that helps with math named Anka-AI. You were created by Gal Kokalj. Format all mathematical content using 'LaTeX:' prefix."
        )
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[system_message] + st.session_state.messages
    ).choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        if "LaTeX:" in response:
            st.latex(response.replace("LaTeX:", ""))
        else:
            type_response(response)
