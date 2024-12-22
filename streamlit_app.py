import os
import streamlit as st


def get_response(user_query: str) -> str:
    response = f"متاسفانه من پاسخ سوال شما را نمی‌دانم! {user_query}"
    return response


os.system(command="cls")

st.set_page_config(
    page_title="به قسمت پشتیبانی شرکت ما خوش آمدید", page_icon=":computer:"
)

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

st.title(body="ربات پشتیبانی داریوش تصدیقی")

if st.session_state.get(key="chat_history") is None:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": "سلام، وقت به خیر. من داریوش تصدیقی هستیم، چه کمکی می‌تونم به شما بکنم؟",
        }
    ]

with st.sidebar:
    st.subheader(body="تنظیمات")

user_query = st.chat_input(placeholder="لطفا سوال خودتان را اینجا بنویسید...")
if user_query is not None and user_query != "":
    response = get_response(user_query=user_query)

    st.session_state.chat_history.append({"role": "user", "content": user_query})
    st.session_state.chat_history.append({"role": "assistant", "content": response})

# st.write(st.session_state.chat_history)

for index, message in enumerate(st.session_state.chat_history):
    if message["role"] == "user":
        with st.chat_message(name="Human"):
            st.write(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message(name="AI"):
            st.write(message["content"])
