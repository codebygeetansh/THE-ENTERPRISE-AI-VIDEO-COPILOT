import json
import pandas as pd
from sentence_transformers import SentenceTransformer
import joblib
import os
import torch

# Folders ka sahi rasta
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'Models'))

# File paths
JSON_PATH = os.path.join(MODELS_DIR, 'updated_merged_chunks.json')
SAVE_PATH = os.path.join(MODELS_DIR, 'rag_embeddings_data.joblib')

def generate_and_save_embeddings():
    print("🚀 JSON data load ho raha hai...")
    if not os.path.exists(JSON_PATH):
        print(f"❌ Error: JSON file nahi mili at {JSON_PATH}")
        return
        
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        chunks_data = json.load(f)

    # JSON ko Pandas DataFrame mein convert karna
    df = pd.DataFrame(chunks_data)
    print(f"✅ Total {len(df)} chunks load ho gaye!")

    # GPU Check karna
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\n🔥 System using {DEVICE.upper()} for super-fast embeddings! 🔥")

    # Free Open-Source Model Load karna
    print("Loading all-MiniLM-L6-v2 embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2', device=DEVICE)

    # Embeddings Generate karna
    print("⏳ Embeddings ban rahi hain... (GPU par yeh bohot fast hoga!)")
    text_list = df['text'].tolist()
    
    # Encode function text ko vectors (numbers) mein badal dega
    embeddings = model.encode(text_list, show_progress_bar=True)

    # Embeddings ko DataFrame mein ek naye column ki tarah add karna
    df['embedding'] = embeddings.tolist()

    # Joblib ka use karke DataFrame ko save karna (Bina kisi Vector DB ke!)
    print("\n💾 Data Joblib file mein save ho raha hai...")
    joblib.dump(df, SAVE_PATH)
    
    print(f"🎉 BOOM! Teri Embeddings successfully yahan save ho gayi: {SAVE_PATH}")

if __name__ == "__main__":
    generate_and_save_embeddings()