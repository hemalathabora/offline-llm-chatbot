
# 💬 Offline ChatGPT Clone with `phi3` + Ollama + Streamlit

A sleek, fully offline chatbot app using Microsoft's **phi3** model and the **Ollama** LLM runtime. Styled like ChatGPT, this app supports:

- ✅ Local chat with LLM (`phi3`)
- ✅ New chat sessions with memory
- ✅ Sidebar for recent chats
- ✅ Light/Dark mode toggle
- ✅ Beautiful Streamlit UI

---

## ⚙️ Features

- 🔁 Offline conversations powered by `phi3` running via Ollama
- 🧠 Chat history and conversation tracking
- 🎨 Toggle between Light & Dark themes
- 🗂️ Recent chat list with auto-titles
- ✅ Fully responsive UI inspired by ChatGPT
- 🚀 Easily extensible to other models (Mistral, LLaMA3, etc.)

---

## 🧠 Powered By

| Component     | Description                     |
|---------------|----------------------------------|
| `phi3`        | Microsoft’s efficient LLM        |
| `Ollama`      | Lightweight LLM runtime locally  |
| `Streamlit`   | UI framework for Python apps     |

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/offline-chatgpt-ollama.git
cd offline-chatgpt-ollama
````

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Ollama

Download from: [https://ollama.com/download](https://ollama.com/download)

### 4. Pull the `phi3` Model

```bash
ollama run phi3
```

This command downloads and starts the `phi3` model.

---

## ▶️ Run the App

```bash
streamlit run app.py
```

App runs locally on:
👉 [http://localhost:8501](http://localhost:8501)

---

## 📬 Using Postman (Optional)

You can also test the model manually via API:

* **Endpoint:** `POST http://localhost:11434/api/generate`
* **Headers:**

  * `Content-Type: application/json`
* **Body (raw/JSON):**

```json
{
  "model": "phi3",
  "prompt": "What is the capital of France?",
  "stream": false
}
```

### ✅ Expected Response:

```json
{
  "response": "The capital of France is Paris."
}
```

---

## 📁 Project Structure

```
offline-chatgpt-ollama/
├── app.py               # Streamlit app
├── callollama.py        # API call to local phi3 model
├── requirements.txt     # Python dependencies
├── README.md            # You are here
```

---

## 🌈 Customization Ideas

* Add voice input/output with `speech_recognition`
* Save chat history to file or database
* Support for other models (`llama3`, `mistral`, `gemma`, etc.)
* Add Markdown support or code highlighting



