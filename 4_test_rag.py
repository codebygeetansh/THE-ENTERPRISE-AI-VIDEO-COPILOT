import os
import joblib
import pandas as pd
import numpy as np
import requests
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --- Folders aur Paths Setup ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'Models'))
JOBLIB_PATH = os.path.join(MODELS_DIR, 'rag_embeddings_data.joblib')

def start_interactive_rag():
    # 1. Saved Embeddings Database Load Karna
    if not os.path.exists(JOBLIB_PATH):
        print(f"❌ Error: Joblib database file nahi mili at {JOBLIB_PATH}")
        return
        
    print("🚀 Vector Database load ho raha hai...")
    df = joblib.load(JOBLIB_PATH)
    print(f"✅ Database Loaded! Total {len(df)} chunks ready.\n")

    # 2. Embedding Model Setup (GPU Acceleration)
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"⚡ Using {DEVICE.upper()} for fast semantic search...")
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device=DEVICE)
    print("✅ Model Ready!\n")
    print("="*60)
    print("🤖 ENTERPRISE VIDEO COPILOT IS ONLINE!")
    print("Type your question below (or type 'exit' or 'quit' to stop).")
    print("="*60)

    # 3. User Input Loop (Continuous Chat Facility)
    while True:
        try:
            print("\n" + "-"*50)
            user_query = input("🧑‍💻 You: ").strip()
            
            # Exit condition
            if user_query.lower() in ['exit', 'quit']:
                print("👋 Bye bhai! See you next time.")
                break
                
            if not user_query:
                print("⚠️ Bhai, khali question mat bhej, kuch type kar!")
                continue

            print("🧠 Searching best context...")
            
            # Query ko vector mein badalna
            query_vector = embedding_model.encode([user_query])

            # Cosine Similarity se best chunk dhoondna
            document_vectors = np.array(df['embedding'].tolist())
            similarities = cosine_similarity(query_vector, document_vectors)[0]

            # Best match nikalna
            best_match_index = np.argmax(similarities)
            best_context = df.iloc[best_match_index]['text']
            video_title = df.iloc[best_match_index]['video_title']
            start_t = df.iloc[best_match_index]['start_time']
            end_t = df.iloc[best_match_index]['end_time']

            # 4. Strict Prompt Engineering
            OLLAMA_API_URL = "http://localhost:11434/api/generate"
            OLLAMA_MODEL = "llama3.2" 
            
            prompt = f"""You are an expert AI assistant for a System Design and OOPs YouTube playlist. 
            Your task is to answer the User's Question STRICTLY based on the provided Video Transcript. Do not use outside knowledge.
            Format your answer professionally in bullet points if necessary. Make it easy to understand.
            At the absolute end of your response, you MUST cite the source exactly in this format: 
            "Source: [Video Title] (Timestamp: [Start]s - [End]s)"

            [Source Information]
            Video Title: {video_title}
            Start Time: {start_t}
            End Time: {end_t}
            Video Transcript: {best_context}

            [User Question]
            {user_query}

            [Your Answer]"""

            payload = {
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1 # Strictly factual rahega
                }
            }

            print("🤖 LLaMA 3.2 is typing...\n")
            
            # API Call to Local Ollama
            response = requests.post(OLLAMA_API_URL, json=payload)
            if response.status_code == 200:
                result = response.json()
                print("================ FINAL ANSWER ================\n")
                print(result['response'])
                print("\n==============================================")
            else:
                print(f"❌ Ollama Error: {response.text}")
                
        except KeyboardInterrupt:
            # Agar user Ctrl+C dabaye toh gracefully exit ho jaye
            print("\n\n👋 Script stopped manually. Bye bhai!")
            break
        except requests.exceptions.ConnectionError:
            print("\n❌ Error: Ollama se connect nahi ho paya! Bhai check kar le ki Ollama app background mein chal rahi hai ya nahi.")
            break
        except Exception as e:
            print(f"\n❌ Ek unexpected error aa gaya bhai: {e}")

if __name__ == "__main__":
    start_interactive_rag()