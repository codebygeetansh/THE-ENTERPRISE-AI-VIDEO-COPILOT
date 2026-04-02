# 🚀 Enterprise Video Copilot

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![LLaMA](https://img.shields.io/badge/LLaMA_3.2-Local_AI-orange?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-Backend-green?style=for-the-badge&logo=flask)
![UI](https://img.shields.io/badge/Glassmorphism-UI-purple?style=for-the-badge)

**Enterprise Video Copilot** is a 100% offline, privacy-first Retrieval-Augmented Generation (RAG) system. It transforms hours of long video lectures and meetings into an interactive AI assistant that answers your queries strictly based on the provided video transcripts, complete with exact timestamps.

---

## 🌟 Key Features

* **🔒 100% Privacy & Local Execution:** Runs entirely on your local machine using Ollama. No API keys, no recurring costs, and zero data leaks to third-party cloud services.
* **⏱️ Exact Timestamp Citations:** Doesn't just give you an answer; it tells you exactly *where* the answer came from (e.g., `Source: [Video Title] (Timestamp: 120s - 180s)`).
* **🎯 Zero Hallucination:** Powered by strict prompt engineering and a low-temperature configuration, ensuring the AI only speaks from the provided transcript.
* **✨ Premium Perplexity-Style UI:** A dynamic, dark-mode glassmorphism interface featuring moving background particles, smart metadata chips, and smooth typing animations.

---

## 🛠️ Tech Stack

### Backend & AI Engine
* **Language:** Python
* **Web Framework:** Flask & Flask-CORS
* **LLM:** LLaMA 3.2 (via Ollama)
* **Embeddings:** `SentenceTransformers` (`all-MiniLM-L6-v2`)
* **Vector Storage:** Pandas & Joblib (Lightning-fast, in-memory mathematical cosine similarity without the overhead of heavy Vector Databases).

### Frontend
* **Core:** HTML5, CSS3, Vanilla JavaScript
* **Design System:** Custom CSS (Glassmorphism, Gradient Accents, Dynamic Hover States, and CSS Keyframe Animations).

---

## 🚀 How to Run Locally

Follow these steps to experience the Enterprise Video Copilot on your machine:

### 1. Start the AI Brain (Ollama)
Ensure you have Ollama installed and the LLaMA model pulled. Let it run in the background.
```bash
ollama run llama3.2
2. Start the Backend Server
Navigate to the project directory, activate your Python environment, and start the Flask server.

Bash
pip install -r requirements.txt
python Backend/App.py
Wait until you see * Running on http://127.0.0.1:5000 in the terminal.

3. Launch the UI
Simply open the Frontend/index.html file in any modern web browser (Chrome, Edge, Safari). No frontend build tools required!

💡 Real-World Applications
EdTech: Students can instantly search for specific concepts across 100+ hours of course material.

Corporate Onboarding: New employees can query HR training videos for immediate policy answers.

Meeting Minutes: Extract decisions and specific discussions from long recorded corporate Zoom calls.

Customer Support: Agents can instantly retrieve step-by-step guides from product tutorial videos.
