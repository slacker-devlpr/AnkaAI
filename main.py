
from openai import OpenAI
import streamlit as st
import time
import re
import markdown
import matplotlib.pyplot as plt
import numpy as np
import io
import base64


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
            rendered_parts.append(f"<div style='text-align:left;'>{part[2:-2]}</div>")
        else:
            rendered_parts.append(part)
    return "".join(rendered_parts)

def display_messages(messages):
    for message in messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            if "image" in message:
                st.markdown(f'<img src="data:image/png;base64,{message["image"]}" alt="Plot">', unsafe_allow_html=True)
            else:
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
        Use 1000 data points, x axis from -10 to 10.
        The plot should have a black background and for the axis white lines.
        The line should be blueish.
        Use a good ratio to make it look good.
        Only generate the code block no additional explanation.
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

        fig, ax = plt.subplots()

        # Set background color to black
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')

        # Set spines color to white
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')

        # Set axis tick colors to white
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        # Set axis label colors to white
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')

        exec(code_to_execute, globals(), locals())
        
        # Change plot line color to white if not set in code
        for line in ax.lines:
            if line.get_color() == 'C0':
              line.set_color('white')
        
        # Set title color to white
        ax.title.set_color('white')

        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="png", facecolor=fig.get_facecolor())
        buf.seek(0)

        # Encode to base64 for display
        image_base64 = base64.b64encode(buf.read()).decode("utf-8")
        
        plt.close()
        return image_base64
    
    except Exception as e:
        st.error(f"Error generating plot: ")
        return None
        
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
        st.session_state.messages.append({"role":"assistant", "content": f"Generating a plot of function: {function_string}"})
        with st.chat_message("assistant", avatar=BOT_AVATAR):
           type_response(f"Generating a plot of function: {function_string}")
        image_data = generate_and_display_plot(function_string)
        if image_data:
            st.session_state.messages.append({"role": "assistant", "image": image_data})
        else:
            st.session_state.messages.append({"role": "assistant", "content": "Plot could not be generated."})


    else:
        system_message = {
            "role": "system",
            "content": (
                "You are Anka-AI, a specialized artificial intelligence for assisting with mathematics. You were created by Gal Kokalj. "
                "Your primary goal is to help users understand and solve math problems. "
                "When you provide mathematical expressions or formulas, always enclose them within double dollar signs ($$), "
                "which will be rendered as LaTeX. For example, 'The area of a circle is given by $$A = \\pi r^2$$' and 'The symbol $$x$$ represents a variable'. "
                "Use LaTeX formatting for every math symbol, equation, or expression, no matter how simple it is. Do not miss any math symbols and always put them in latex."
                "You can plot any graph by using the command %%formula%% at the end of your response, for example: %%x^2%%. Do not include more formulas than the main formula."
                "Be concise and helpful. Use clear and simple terms to help the user learn math as easily as possible"
            )
        }

        response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[system_message] + st.session_state.messages
        ).choices[0].message.content

        # Check for plot command
        plot_match = re.search(r'%%(.*?)%%', response)
        if plot_match:
            function_string = plot_match.group(1)

            # Remove %%formula%% from the response
            response = re.sub(r'%%.*?%%', '', response).strip()
            
            image_data = generate_and_display_plot(function_string)
            
            if image_data:
                st.session_state.messages.append({"role": "assistant", "content": response, "image": image_data})
                with st.chat_message("assistant", avatar=BOT_AVATAR):
                    type_response(response)
                    st.markdown(f'<img src="data:image/png;base64,{image_data}" alt="Plot">', unsafe_allow_html=True)
            else:
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant", avatar=BOT_AVATAR):
                     type_response(response)
            
        else:
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant", avatar=BOT_AVATAR):
                type_response(response)
