import streamlit as st
st.set_page_config(
    page_title="Anka-AI, artificial intelligence for math",
    page_icon=r"Anka (1).png"
)
hide_streamlit_style = """
<style>
.css-hi6a2p {padding-top: 0rem;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
st.markdown('''
<style>
.stApp [data-testid="stToolbar"]{
    display:none;
}
</style>
''', unsafe_allow_html=True)
enable_scroll = """
<style>
.main {
    overflow: auto;
}
</style>
"""

st.markdown(enable_scroll, unsafe_allow_html=True)
st.title("Dear Valued Users,")
st.text("We regret to inform you that Anka AI will be temporarily shutting down as we transition from OpenAI to Deepseek which achieves a significant breakthrough in inference speed over previous models.")
st.text("While this marks the end of an era, it is also the beginning of a fresh chapter with enhanced capabilities and features to better serve your needs. ")
st.text("We deeply appreciate your support and understanding during this change. This decision was made with the goal of providing you with an even more innovative and robust AI experience. ")
st.text("Thank you for being part of this journey, and we look forward to continuing to support you with our new platform.")
