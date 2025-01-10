import streamlit as st
import time
import re
import markdown
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from openai import OpenAI

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
            st.markdown(message["content"])

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

# Function to generate and display plot
def generate_and_display_plot(function_string):
    try:
        # Generate Python code using OpenAI to plot the function
        plot_code_prompt = f"""
        Generate python code using matplotlib and numpy to plot the following mathematical function: {function_string}.
        The x-axis should range from -10 to 10, use 1000 data points.
        The plot should have a black background.
        The axes should be traditional with arrows at the end of each axis.
        Only generate the code block, no additional explanation.
        """
        plot_code_response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": "user", "content": plot_code_prompt}]
        ).choices[0].message.content

        # Execute the generated code
        # First extract the code from the string
        match = re.search(r'```python\n(.*?)\n```', plot_code_response, re.DOTALL)
        if match:
            code_to_execute = match.group(1)
        else:
            code_to_execute = plot_code_response
        
        fig, ax = plt.subplots()[[1](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AYygrcSlIT68mEkp_yb8Qg3n4gQo9jo11zWdpoF9frfivE6uiAITMqrKdH7bjy6eb_dJ1Uy1Lx-_uaZ7Ys7UHY0B1nZPjAh3bmDVzm8UsBjR-KHWhV2fiaCRJHS5sicO7B7DVtV-SsRUz8YKqQqU2XQCc1cTb9JZcpNuF_btBWJHdU8IGZVRqylsNW0iBWRB)][[2](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AYygrcTGS2W5fBTVrSouQB8ToiEEHdbTWHZIlrJMSsmB8lAyBaWp1oyk4LaOm_6apn3ZOGERSIFdb_Ym6TnXuk6eoOv89DbdM-RtUr2OBbYhJMfAW7BxLEBok4G5jWm-CbUg04XRszmbZj00KM1pkOQR77CivRTumHQqzrcer8BPfud16xE=)][[3](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AYygrcTbXt7TBQAFVlkM93UI-t8qCQLUHvTKHTplBhhUSxlxLZ8aRGAU1iiCq5A7LNmmdCBL4RGYGXtbu68vEYH68e21VhPzo5ED_OJ7yI0qsNHTymvlUGu-dKRj5vY5UNKzJ3-nUmHWtbE=)]
        
        # Set background color to black
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        
        # Set spines to be in the middle and make them black
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        
        # Make ticks black
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        
        # Add arrows to axes
        ax.plot((1), (0), ls="", marker=">", ms=10, color="white",
                transform=ax.get_yaxis_transform(), clip_on=False)
        ax.plot((0), (1), ls="", marker="^", ms=10, color="white",
                transform=ax.get_xaxis_transform(), clip_on=False)
        
        exec(code_to_execute, globals(), locals())
        
        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="png", facecolor=fig.get_facecolor())
        buf.seek(0)
        
        # Encode to base64 for display
        image_base64 = base64.b64encode(buf.read()).decode("utf-8")
        
        # Display the plot in Streamlit
        st.markdown(f'<img src="data:image/png;base64,{image_base64}" alt="Plot">', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error generating plot: {e}")
        
    plt.close()

# Main chat interface
if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    if prompt.strip().lower() == "/plot":
        st.session_state.messages.append({"role":"assistant", "content": "Please enter the function to plot after the command `/plot` such as `/plot x^2`"})
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            type_response("Please enter the function to plot after the command `/plot` such as `/plot x^2`")
    elif prompt.lower().startswith("/plot"):
        function_string = prompt[5:].strip()
        st.session_state.messages.append({"role":"assistant", "content": f"Generating a plot of function: ``"})
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            type_response(f"Generating a plot of function: ``")
        generate_and_display_plot(function_string)

    else:
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
