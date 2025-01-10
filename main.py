from openai import OpenAI
import streamlit as st
import time
import re
import markdown


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

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Typing animation function
def type_response(content):
    message_placeholder = st.empty()
    full_response = ""
    for char in content:
        full_response += char
        message_placeholder.markdown(full_response + "▌")
        time.sleep(0.005)
    message_placeholder.markdown(full_response)


# Function to find and render LaTeX using st.markdown
def render_latex(text):
    parts = re.split(r'(\$\$[^\$]+\$\$)', text)  # Split at $$...$$ delimiters
    rendered_parts = []
    for i, part in enumerate(parts):
        if part.startswith("$$") and part.endswith("$$"):
            rendered_parts.append(f"<div style='text-align:left;'>{part[2:-2]}</div>") # This is the only change here from the previous code
        else:
           rendered_parts.append(part)
    return "".join(rendered_parts)

def display_messages(messages):
    for message in messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(markdown.markdown(render_latex(message["content"])), unsafe_allow_html=True)


# Add initial hello message if first visit
if not st.session_state.messages:
    initial_message = {
        "role": "assistant",
        "content": "Welcome to Anka-AI! I'm your dedicated math assistant, ready to help with a wide range of mathematical concepts. Let's work together to make math clear and engaging! What can I help you with today?"
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
            "You are Anka-AI, a specialized artificial intelligence for assisting with mathematics. You were created by Gal Kokalj. "
            "Your primary goal is to help users understand and solve math problems. "
            "When you provide mathematical expressions or formulas, always enclose them within double dollar signs ($$), "
            "which will be rendered as LaTeX. For example, 'The area of a circle is given by $$A = \\pi r^2$$' and 'The symbol $$x$$ represents a variable'. "
            "Use LaTeX formatting for every math symbol, equation, or expression, no matter how simple it is. Do not miss any math symbols and always put them in latex."
            "Be concise and helpful. Use clear and simple terms to help the user learn math as easily as possible"
        )
    }

    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[system_message] + st.session_state.messages
    ).choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        type_response(response)
