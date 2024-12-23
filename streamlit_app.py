import os
from groq import Groq
import streamlit as st


def set_page_config() -> None:
    st.set_page_config(page_title="چت بات داریوش تصدیقی", page_icon="👋")

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


def initial_session_state() -> None:
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    if "model_name" not in st.session_state:
        st.session_state.model_name = "llama-3.3-70b-versatile"

    if "messages" not in st.session_state:
        message_system = {
            "role": "system",
            "content": "you are a helpful assistant. answer similar a human.",
        }

        message_assistant = {
            "role": "assistant",
            "content": "سلام، وقت به خیر. من داریوش هستم، چه کمکی می‌تونم به شما بکنم؟",
        }

        st.session_state.messages = [message_system, message_assistant]


def get_response() -> str:
    client = Groq(api_key=st.session_state.api_key)

    chat_completion = client.chat.completions.create(
        model=st.session_state.model_name, messages=st.session_state.messages
    )

    response = chat_completion.choices[0].message.content
    return response


os.system(command="cls")

models = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]

set_page_config()
initial_session_state()

with st.sidebar:
    st.subheader(body="تنظیمات", divider="rainbow")

    st.session_state.model_name = st.radio(
        label="لطفا مدل خود را انتخاب نمایید:",
        options=models,
        index=1,
    ).strip()
    st.divider()

    st.write(st.session_state.model_name)
    st.divider()

    st.session_state.api_key = st.text_input(label="API Key", type="password").strip()
    st.divider()

    st.write(
        "👋 دوست گرامی، شما می‌توانید در سایت https://groq.com ثبت‌نام کرده و پس از ورود، به طور کاملا رایگان، نسبت به دریافت یک کد API Key اقدام نمایید."
    )
    st.divider()

st.header(body="👋 به Chatbot داریوش تصدیقی خوش آمدید!", divider="rainbow")

if not st.session_state.model_name:
    st.error(body="لطفا برای انجام عملیات، مدل خود را انتخاب نمایید!")

if not st.session_state.api_key:
    st.error(body="لطفا برای انجام عملیات، API Key خود را وارد نمایید!")

if st.session_state.api_key and st.session_state.model_name:
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
