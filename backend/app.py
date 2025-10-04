import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gtts import gTTS
from dotenv import load_dotenv
import uuid
import json

# Load API key
load_dotenv()
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
CEREBRAS_API_URL = "https://api.cerebras.ai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {CEREBRAS_API_KEY}",
    "Content-Type": "application/json"
}

# Language map for gTTS
LANG_MAP = {
    "en": "English",
    "hi": "Hindi",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "te": "Telugu",
    "zh-CN": "Chinese"
}

app = Flask(__name__)
CORS(app)


# ---------- Cerebras expand with polite conversational tone ----------
def expand_text_with_cerebras(text, lang="en"):
    """
    Expand a short cue word (e.g., 'hungry', 'sleepy') into a short, polite,
    first-person conversational sentence in the target language + English translation.
    """

    language_name = LANG_MAP.get(lang, "English")

    system_prompt = (
        "You power an assistive communication device for someone who cannot speak. "
        "They send a very short cue word (e.g., 'hungry', 'sleepy', 'bathroom', 'help'). "
        f"Write ONE short, first-person, polite sentence in {language_name} that they would say to another person.\n"
        "Rules:\n"
        "- Keep it natural and conversational.\n"
        "- 6–12 words. No definitions, explanations, or quotations.\n"
        "- No meta text, numbering, or extra lines.\n"
        "- If the cue is ambiguous, pick the most common everyday meaning.\n"
        f"Return STRICT JSON only: {{\"expanded\": \"<sentence in {language_name}>\", "
        "\"english\": \"<English translation of the same sentence>\"}}"
    )

    # Few-shot examples to guide behavior
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "hungry"},
        {"role": "assistant", "content": "{\"expanded\":\"I'm hungry, could I have something to eat?\",\"english\":\"I'm hungry, could I have something to eat?\"}"},
        {"role": "user", "content": "sleepy"},
        {"role": "assistant", "content": "{\"expanded\":\"I'm feeling sleepy and need a short rest.\",\"english\":\"I'm feeling sleepy and need a short rest.\"}"},
        {"role": "user", "content": "bathroom"},
        {"role": "assistant", "content": "{\"expanded\":\"I need to use the bathroom, please.\",\"english\":\"I need to use the bathroom, please.\"}"},
        {"role": "user", "content": text}
    ]

    payload = {
        "model": "llama3.1-8b",
        "messages": messages,
        "temperature": 0.4,   # lower = more consistent
        "max_tokens": 120
    }

    try:
        resp = requests.post(CEREBRAS_API_URL, headers=HEADERS, json=payload)
        resp.raise_for_status()
        raw = resp.json()["choices"][0]["message"]["content"].strip()
        print("Raw Cerebras Output:", raw)

        parsed = json.loads(raw)
        expanded = parsed.get("expanded", text).strip()
        english = parsed.get("english", expanded if lang == "en" else "(translation missing)").strip()
        return expanded, english
    except Exception as e:
        print("Cerebras error:", e, "\nRaw:", locals().get("raw"))
        # Fallback: polite minimal sentence
        fallback = "I need help, please." if text.lower() == "help" else f"I need {text}, please."
        return (fallback if lang == "en" else text, fallback)


# ---------- API Routes ----------
@app.route("/speak", methods=["POST"])
def speak():
    data = request.json
    text = data.get("text", "")
    lang = data.get("lang", "en")

    expanded_text, english_translation = expand_text_with_cerebras(text, lang)

    # Generate audio file
    filename = f"speech_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join("static", filename)
    try:
        tts = gTTS(text=expanded_text, lang=lang)
        tts.save(filepath)
    except Exception as e:
        print(f"Error in gTTS: {e}")
        return jsonify({"error": "TTS failed"}), 500

    return jsonify({
        "expanded_text": expanded_text,
        "english_translation": english_translation,
        "audio_url": f"/get_audio/{filename}"
    })


@app.route("/get_audio/<filename>")
def get_audio(filename):
    return send_from_directory("static", filename)


if __name__ == "__main__":
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(host="0.0.0.0", port=5000, debug=True)
