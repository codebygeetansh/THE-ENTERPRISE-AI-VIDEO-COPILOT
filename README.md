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






