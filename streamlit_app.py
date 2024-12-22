import os
from groq import Groq
import streamlit as st


def get_response() -> str:
    client = Groq(api_key=st.session_state.api_key)

    chat_completion = client.chat.completions.create(
        model=model_name, messages=st.session_state.messages
    )

    response = chat_completion.choices[0].message.content
    return response


os.system(command="cls")

model_name = "llama-3.1-8b-instant"

st.set_page_config(page_title="پشتیبانی شرکت ما", page_icon="👋")

streamlit_style = """
<style>
    @import url('https://fonts.cdnfonts.com/css/iransansx');

    html, body, p, h1, h2, h3, h4, h5, h6, input, textarea {
        font-family: 'IRANSansX', tahoma !important;
    }

    .block-container, section, input, textarea {
        direction: rtl;
        text-align: justify;
    }
</style>
"""

st.markdown(body=streamlit_style, unsafe_allow_html=True)

st.header(body="تیم پشتیبانی شرکت ما، در خدمت شما می‌باشد", divider="rainbow")

if "api_key" not in st.session_state:
    st.session_state.api_key = ""
    st.error(body="لطفا برای انجام عملیات، API Key را وارد نمایید!")

if "messages" not in st.session_state:
    message_system = {"role": "system", "content": "you are a helpful assistant."}
    message_assistant = {
        "role": "assistant",
        "content": "سلام، وقت به خیر. من داریوش تصدیقی هستیم، چه کمکی می‌تونم به شما بکنم؟",
    }

    st.session_state.messages = [message_system, message_assistant]

with st.sidebar:
    st.subheader(body="تنظیمات")
    st.text_input(label="نام مدل", value=model_name)
    st.session_state.api_key = st.text_input(label="API Key", type="password")

if st.session_state.api_key:
    prompt = st.chat_input(placeholder="لطفا سوال خودتان را اینجا بنویسید...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = get_response()
        st.session_state.messages.append({"role": "assistant", "content": response})

    for index, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            with st.chat_message(name="Human"):
                st.write(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message(name="AI"):
                st.write(message["content"])
