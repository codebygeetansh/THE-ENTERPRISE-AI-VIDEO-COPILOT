import os
import json
import whisper
import torch
import gc  # RAM saaf karne ke liye library

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'data'))
MODELS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'Models'))

def process_and_merge_chunks():
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\n🔥 System Check: Using {DEVICE.upper()} with RAM Optimization! 🔥\n")
    
    print("Loading Whisper model (base)... please wait.")
    model = whisper.load_model("base", device=DEVICE)
    
    all_merged_chunks = []
    save_path = os.path.join(MODELS_DIR, 'updated_merged_chunks.json')
    
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)
        
    audio_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.mp3')]
    
    if not audio_files:
        print("❌ Error: Data folder mein koi MP3 files nahi hain!")
        return

    print(f"Total {len(audio_files)} videos processing shuru ho rahi hai...\n")

    for filename in audio_files:
        filepath = os.path.join(DATA_DIR, filename)
        print(f"🎧 Processing: {filename} ...")
        
        # Audio ko transcribe karna
        result = model.transcribe(filepath, task="translate")
        video_title = filename.replace('.mp3', '')
        
        current_chunk_text = ""
        start_time = 0.0
        word_count = 0
        
        for i, segment in enumerate(result['segments']):
            if word_count == 0:
                start_time = segment['start']
            
            current_chunk_text += segment['text'] + " "
            word_count += len(segment['text'].split())
            
            if word_count >= 100 or i == len(result['segments']) - 1:
                all_merged_chunks.append({
                    "video_title": video_title,
                    "start_time": round(start_time, 2),
                    "end_time": round(segment['end'], 2),
                    "text": current_chunk_text.strip()
                })
                current_chunk_text = ""
                word_count = 0
                
        # --- NEW: HAR VIDEO KE BAAD SAVE KARNA ---
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(all_merged_chunks, f, ensure_ascii=False, indent=4)
            
        print(f"✅ {filename} done and progress saved!")

        # --- NEW: RAM AUR GPU MEMORY SAAF KARNA ---
        del result
        gc.collect()
        if DEVICE == "cuda":
            torch.cuda.empty_cache()

    print(f"\n🎉 BOOM! Saara data safely complete ho gaya: {save_path}")

if __name__ == "__main__":
    process_and_merge_chunks()