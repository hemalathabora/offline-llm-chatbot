# streamlit_app.py

import streamlit as st
from callollama import callOLLAMA

# ---- Page Config ----
st.set_page_config(page_title="Offline Chatbot", layout="centered")

# ---- Session Initialization ----
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, I am your personal assistant. How can I help you today?"}
    ]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "new_chat_started" not in st.session_state:
    st.session_state.new_chat_started = False

# ---- Sidebar UI ----
st.sidebar.title("💬 Offline Chatbot")

# Theme Toggle
theme_choice = st.sidebar.radio("🌓 Theme", ["light", "dark"], index=0 if st.session_state.theme == "light" else 1)
st.session_state.theme = theme_choice

# New Chat Button
if st.sidebar.button("➕ New Chat"):
    if st.session_state.messages and len(st.session_state.messages) > 1:
        chat_title = st.session_state.messages[1]["content"][:30].strip()
        existing_titles = [chat["title"] for chat in st.session_state.chat_history]
        if chat_title and chat_title not in existing_titles:
            st.session_state.chat_history.append({
                "title": chat_title,
                "messages": st.session_state.messages.copy()
            })

    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, I am your personal assistant. How can I help you today?"}
    ]
    st.session_state.current_chat = "New Chat"
    st.session_state.new_chat_started = True

# Chat Search
search_query = st.sidebar.text_input("🔍 Search chats")

# Display Recent Chats
filtered_chats = [
    chat for chat in reversed(st.session_state.chat_history[-5:])
    if search_query.lower() in chat["title"].lower()
]

if filtered_chats:
    st.sidebar.markdown("### 📁 Recent Chats")
    for i, chat in enumerate(filtered_chats):
        title = chat["title"]
        if st.sidebar.button(title, key=f"chat_button_{i}"):
            st.session_state.messages = chat["messages"].copy()
            st.session_state.current_chat = title
            st.session_state.new_chat_started = False

# ---- Styles ----
light_styles = """
    <style>
    .chat-container {
    background: #F7F9FC;
    padding: 1rem;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
}
.user-msg, .bot-msg {
    max-width: 80%;
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 18px;
    font-size: 16px;
    line-height: 1.5;
    box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.1);
}
.user-msg {
    background-color: #D4F8CB;
    color: #333;
    align-self: flex-end;
    text-align: left;
}
.bot-msg {
    background-color: #F1F0F0;
    color: #333;
    align-self: flex-start;
    text-align: left;
}
.center-text {
    text-align: center;
    margin-top: 10px;
}</style>
"""
dark_styles = """
    <style>
.chat-container {
    background: #1E1E1E;
    padding: 1rem;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
}
.user-msg, .bot-msg {
    max-width: 80%;
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 18px;
    font-size: 16px;
    line-height: 1.5;
    box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.3);
}
.user-msg {
    background-color: #3A3F41;
    color: #fff;
    align-self: flex-end;
    text-align: left;
}
.bot-msg {
    background-color: #2D2D2D;
    color: #fff;
    align-self: flex-start;
    text-align: left;
}
.center-text {
    text-align: center;
    margin-top: 10px;
}
</style
"""

st.markdown(dark_styles if st.session_state.theme == "dark" else light_styles, unsafe_allow_html=True)

# ---- Main UI Title + Subtitle (Centered) ----
st.markdown('<h1 class="center-text">💡 Offline LLM Chat</h1>', unsafe_allow_html=True)
st.markdown('<p class="center-text">Built with <b>Streamlit</b> + <b>OLLAMA</b></p>', unsafe_allow_html=True)

# ---- Chat Display ----
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    role_class = "user-msg" if msg["role"] == "user" else "bot-msg"
    st.markdown(f'<div class="{role_class}">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---- Chat Input Box ----
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Set chat title only once from first message
    if st.session_state.current_chat == "New Chat" and st.session_state.new_chat_started:
        st.session_state.current_chat = user_input[:30].strip()
        st.session_state.new_chat_started = False

    # Get OLLAMA response
    with st.spinner("Bot is typing..."):
        bot_response = callOLLAMA(user_input)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

    st.rerun()
