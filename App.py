from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import joblib
import numpy as np
import requests
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
# CORS allow karta hai ki tera frontend (HTML) backend se aaram se baat kar sake
CORS(app)

# Paths setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(SCRIPT_DIR, 'Models')
JOBLIB_PATH = os.path.join(MODELS_DIR, 'rag_embeddings_data.joblib')

# Start hote hi database aur model load kar lo taaki baad mein time na lage
print("🚀 Loading Vector Database & AI Model...")
df = joblib.load(JOBLIB_PATH)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device=DEVICE)
print("✅ Enterprise Video Copilot Backend is Live!")

@app.route('/api/chat', methods=['POST'])
def chat():
    user_query = request.json.get('message')
    if not user_query:
        return jsonify({"response": "Please ask a valid question."}), 400

    # 1. Cosine Similarity se best chunk dhoondna
    query_vector = embedding_model.encode([user_query])
    document_vectors = np.array(df['embedding'].tolist())
    similarities = cosine_similarity(query_vector, document_vectors)[0]
    
    best_match_index = np.argmax(similarities)
    best_context = df.iloc[best_match_index]['text']
    video_title = df.iloc[best_match_index]['video_title']
    start_t = df.iloc[best_match_index]['start_time']
    end_t = df.iloc[best_match_index]['end_time']

    # 2. Ollama LLaMA 3.2 ko bhejna
    OLLAMA_API_URL = "http://localhost:11434/api/generate"
    prompt = f"""You are an expert AI assistant for a System Design and OOPs YouTube playlist. 
    Answer the User's Question STRICTLY based on the provided Video Transcript. Do not use outside knowledge.
    Format your answer professionally in bullet points if necessary.
    At the absolute end of your response, you MUST cite the source exactly in this format: 
    "Source: [{video_title}] (Timestamp: {start_t}s - {end_t}s)"

    Video Transcript: {best_context}

    [User Question]
    {user_query}

    [Your Answer]"""

    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1}
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        if response.status_code == 200:
            return jsonify({"response": response.json()['response']})
        else:
            return jsonify({"response": "❌ Server Error: Failed to generate answer."}), 500
    except Exception as e:
        return jsonify({"response": "❌ Error: Make sure Ollama is running in the background!"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)