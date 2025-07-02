import streamlit as st
from datetime import datetime
import time
import requests
import json

# Set page configuration
st.set_page_config(
    page_title="Simple Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm your AI assistant. How can I help you today?",
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "phi3"  # Default model

if "available_models" not in st.session_state:
    st.session_state.available_models = []

# Function to get available Ollama models
def get_available_models():
    """
    Fetch list of available models from Ollama
    """
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = []
            for model in data.get("models", []):
                model_name = model.get("name", "").split(":")[0]  # Remove tag if present
                if model_name and model_name not in models:
                    models.append(model_name)
            return sorted(models)
        else:
            return []
    except:
        return []

# OLLAMA INTEGRATION - DYNAMIC MODEL SELECTION
def get_bot_response(user_message, model_name):
    """
    Function to get response from Ollama running locally with selected model.
    Make sure Ollama is running and the selected model is available.
    """
    
    try:
        # Ollama API endpoint (default local)
        ollama_url = "http://localhost:11434/api/generate"
        
        if model_name == 'qwen3':
            model_name = 'qwen3:0.6b'
        payload = {
            "model": model_name,
            "prompt": user_message,
            "stream": False  # Set to False to get complete response at once
        }
        print(payload)
        # Make request to Ollama
        response = requests.post(
            ollama_url, 
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=60  # 60 second timeout for larger models
        )
        
        if response.status_code == 200:
            result = response.json()
            bot_response = result.get("response", "Sorry, I couldn't generate a response.")
            return bot_response.strip()
        else:
            return f"Error: Ollama API returned status code {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        return "❌ Error: Cannot connect to Ollama. Make sure Ollama is running on localhost:11434"
    
    except requests.exceptions.Timeout:
        return "⏱️ Error: Request timed out. The model might be taking too long to respond."
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

# App Title
st.title(f"🤖 AI Chatbot ({st.session_state.selected_model.upper()})")
st.markdown("*Powered by Ollama - Multi-Model Support*")

# Main chat area
st.subheader("💬 Chat")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**You** ({message['timestamp']})")
        st.info(message["content"])
    else:
        st.markdown(f"**Bot** ({message['timestamp']})")
        st.success(message["content"])

# Show typing indicator
if st.session_state.is_typing:
    st.markdown("**Bot** is typing...")
    st.warning("🤖 Thinking...")

# Input section
st.markdown("---")
st.subheader("📝 Your Message")

# Create a form for input to handle submission properly
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Type your message:",
        placeholder="Ask me anything..."
    )
    
    # Form submit button
    send_button = st.form_submit_button("📤 Send Message", type="primary")

# Other buttons outside the form
col1, col2 = st.columns([1, 1])

with col1:
    clear_button = st.button("🗑️ Clear Chat")

with col2:
    export_button = st.button("💾 Export Chat")

# Handle send message
if send_button and user_input.strip():
    # Add user message to chat
    current_time = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({
        "role": "user",
        "content": user_input.strip(),
        "timestamp": current_time
    })
    
    # Set typing indicator
    st.session_state.is_typing = True
    st.rerun()

# Handle bot response
if st.session_state.is_typing:
    # Get bot response using selected model
    user_message = st.session_state.messages[-1]["content"]
    bot_response = get_bot_response(user_message, st.session_state.selected_model)
    
    # Add bot response to chat
    current_time = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response,
        "timestamp": current_time
    })
    
    # Remove typing indicator
    st.session_state.is_typing = False
    st.rerun()

# Handle clear chat
if clear_button:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm your AI assistant. How can I help you today?",
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    st.session_state.is_typing = False
    st.success("Chat cleared!")
    st.rerun()

# Handle export chat
if export_button:
    if len(st.session_state.messages) > 1:  # More than just welcome message
        chat_content = "CHATBOT CONVERSATION\n" + "="*50 + "\n\n"
        for msg in st.session_state.messages:
            role = "You" if msg["role"] == "user" else "Bot"
            chat_content += f"[{msg['timestamp']}] {role}: {msg['content']}\n\n"
        
        st.download_button(
            label="📄 Download Chat History",
            data=chat_content,
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    else:
        st.warning("No messages to export yet!")

# Sidebar with info
with st.sidebar:
    st.header("🤖 Model Selection")
    
    # Refresh models button
    if st.button("🔄 Refresh Models", help="Fetch latest available models"):
        st.session_state.available_models = get_available_models()
        st.rerun()
    
    # Get available models
    if not st.session_state.available_models:
        st.session_state.available_models = get_available_models()
    
    if st.session_state.available_models:
        # Model selector
        selected_model = st.selectbox(
            "Choose Model:",
            options=st.session_state.available_models,
            index=st.session_state.available_models.index(st.session_state.selected_model) 
                  if st.session_state.selected_model in st.session_state.available_models 
                  else 0,
            help="Select which AI model to use for responses"
        )
        
        # Update selected model if changed
        if selected_model != st.session_state.selected_model:
            st.session_state.selected_model = selected_model
            st.success(f"✅ Switched to {selected_model}")
            st.rerun()
        
        st.info(f"**Current Model:** {st.session_state.selected_model}")
        
        # Show model info if available
        try:
            model_info_response = requests.post(
                "http://localhost:11434/api/show",
                json={"name": st.session_state.selected_model},
                timeout=5
            )
            if model_info_response.status_code == 200:
                model_data = model_info_response.json()
                model_size = model_data.get("details", {}).get("parameter_size", "Unknown")
                st.caption(f"Parameters: {model_size}")
        except:
            pass
    else:
        st.error("❌ No models found")
        st.info("Pull a model: `ollama pull <model_name>`")
    
    st.markdown("---")
    
    st.header("🔗 Ollama Status")
    
    # Check Ollama connection
    try:
        health_check = requests.get("http://localhost:11434/api/tags", timeout=5)
        if health_check.status_code == 200:
            st.success("✅ Ollama is running")
            models_count = len(st.session_state.available_models)
            st.success(f"✅ {models_count} models available")
        else:
            st.error("❌ Ollama not responding")
    except:
        st.error("❌ Ollama not running")
        st.info("Start Ollama: `ollama serve`")
    
    st.markdown("---")
    
    st.header("📊 Chat Stats")
    total_messages = len(st.session_state.messages)
    user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
    bot_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
    
    st.metric("Total Messages", total_messages)
    st.metric("Your Messages", user_messages)
    st.metric("Bot Messages", bot_messages)
    
    st.markdown("---")
    
    st.header("📋 Available Models")
    if st.session_state.available_models:
        for i, model in enumerate(st.session_state.available_models, 1):
            if model == st.session_state.selected_model:
                st.write(f"{i}. **{model}** ← *Current*")
            else:
                st.write(f"{i}. {model}")
    else:
        st.write("No models found")
    
    st.markdown("---")
    
    st.header("⚙️ Configuration")
    st.write(f"**Active Model:** {st.session_state.selected_model}")
    st.write("**Endpoint:** http://localhost:11434")
    st.write("**Timeout:** 60 seconds")
    
    st.header("✨ Features")
    st.write("✅ Multi-model support")
    st.write("✅ Dynamic model switching")
    st.write("✅ Real-time model info")
    st.write("✅ Auto-refresh models")
    st.write("✅ Connection monitoring")

# Footer
st.markdown("---")
st.markdown("**Instructions:** Type a message and press Enter or click 'Send Message' to chat with Phi-3!")
st.markdown("*Note: Make sure Ollama is running with the Phi-3 model available.*")