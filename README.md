# Speech Assist Device

A simple web application that helps people who cannot speak by converting short text inputs into natural sentences and playing them as audio.

## Features

- Takes short words or phrases as input (e.g., "Hungry", "Help")
- Expands input into natural, conversational sentences using Cerebras Llama 3.1 8B model
- Supports **multiple languages** (English, Hindi, French, Spanish, German, Telugu, Chinese)
- Shows both the **expanded message in chosen language** and its **English translation**
- Converts expanded text to speech using gTTS (Google Text-to-Speech)
- **Quick buttons** for common needs (Hungry 🍔, Help 🆘, Sleepy 😴, Bathroom 🚻)
- Plays the generated audio in the browser

## Project Structure

```
speech-assist-device/
├── backend/
│   ├── app.py          # Flask application
│   ├── requirements.txt  # Python dependencies
│   └── .env           # API key configuration (not included in repo)
└── frontend/
    ├── index.html     # User interface
    └── app.js         # Client-side JavaScript
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   
   cd backend
  

2. Create a virtual environment (optional but recommended):
   
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
  

3. Install the required Python packages:
  
   pip install -r requirements.txt
  

4. Install python-dotenv for environment variable management:
  
   pip install python-dotenv
 

5. Configure your Cerebras API key:
   - Edit the `.env` file in the backend directory
   - Replace `your_cerebras_api_key_here` with your actual API key

### Running the Application

1. Start the Flask backend server:
  
   python app.py
   

2. Open the frontend interface:
   - Open `frontend/index.html` in your web browser
   - You can do this by double-clicking the file from the folder(frontend):
   

## Usage

1. Enter a word or short phrase in the text input field OR click a **quick button** (e.g., Hungry, Help, Sleepy, Bathroom)
2. Select your **language** from the dropdown
3. Click the "Speak" button
4. The backend will:
   - Send your text to the Cerebras API to expand it into a natural, polite sentence
   - Return both the **expanded message** and its **English translation**
   - Convert the expanded message to audio using gTTS
5. The frontend will display the message, show the translation, and automatically play the audio

## API Endpoints

- `POST /speak` - Takes a JSON object with "text" and "lang" fields and returns:
  ```json
  {
    "expanded_text": "...",
    "english_translation": "...",
    "audio_url": "/get_audio/speech_xxx.mp3"
  }





## Dependencies

### Backend
- Flask
- requests
- gTTS
- python-dotenv

### Frontend
- Modern web browser with JavaScript enabled
