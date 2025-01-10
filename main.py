from openai import OpenAI
import streamlit as st
import time
import re
import markdown
import matplotlib.pyplot as plt
import numpy as np
import tempfile
import os
import sympy
from sympy import symbols, Eq

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


def plot_function(plot_code):
    """Generates a plot using matplotlib."""
    try:
        # Extract the equation from the plot code, this can be a function of one variable or an implicit function
        equation = plot_code.split(":", 1)[1].strip()

        # Attempt to parse for a single variable, if so treat it as f(x)
        if "=" in equation:
            x, y = symbols('x y')
            eq_parts = equation.split("=")
            if len(eq_parts) == 2:
                left_side, right_side = eq_parts[0].strip(), eq_parts[1].strip()
                eq = Eq(sympy.sympify(left_side), sympy.sympify(right_side))
                #implicit function plot
                p = sympy.plotting.plot_implicit(eq, (x, -10, 10), (y, -10, 10), show=False)
                fig = p.save_data()
            else:
                return None
        else:
            # single function plot
            x = np.linspace(-10, 10, 400)
            y = sympy.sympify(equation, locals={'x':x})
            fig, ax = plt.subplots()
            ax.plot(x, y)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.grid(True)

        
        #save the figure
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            plt.savefig(tmp_file.name)
            plt.close(fig) #close the plot
            return tmp_file.name
    except Exception as e:
        st.error(f"Error plotting function: {e}")
        return None

def render_response(response):
    """Handles both text, latex and plot rendering."""
    plot_pattern = r'(\&\&plot:([^\&]+)\&\&)'
    parts = re.split(plot_pattern, response)
    rendered_parts = []
    for i, part in enumerate(parts):
      if i % 3 == 1:
        image_path = plot_function(part)
        if image_path:
          st.image(image_path)
          os.unlink(image_path) #clean up the temp file
      elif i % 3 == 0:
        rendered_parts.append(render_latex(part))
      
    return "".join(rendered_parts)

def display_messages(messages):
    for message in messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(render_response(message["content"]), unsafe_allow_html = True)


# Add initial hello message if first visit
if not st.session_state.messages:
    initial_message = {
        "role": "assistant",
        "content": "Welcome to Anka-AI! I'm your dedicated math assistant, ready to help with a wide range of mathematical concepts. Let's work together to make math clear and engaging! What can I help you with today?"
    }
    st.toast("Anka-AI is still in Beta. Expect mistakes!", icon="👨‍💻")
    st.toast("You are currently running Anka-AI 1.0.4.", icon="⚙️")
    st.session_state.messages.append(initial_message)


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
            "If the user askes to plot a function in any form, generate a python code that does that function. Enclose the whole function plot code between &&plot: and &&, for example: &&plot:y=x^2+3x+5&&. For implicit functions, use sympys implicit plotter"
            "Try to be as descriptive as possible."
        )
    }

    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[system_message] + st.session_state.messages
    ).choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        type_response(render_response(response))
