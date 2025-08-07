# 🎙️ NextCore AI Voice Agent

A real-time AI voice agent that answers customer calls, understands queries, and responds like a human support agent using company-specific knowledge.

## 🎯 Features

- **Real-time Voice Conversations**: Handles phone calls via Twilio
- **Speech-to-Text**: Converts customer speech to text using OpenAI Whisper
- **AI-Powered Responses**: Uses RAG (Retrieval-Augmented Generation) with company knowledge
- **Text-to-Speech**: Converts AI responses back to natural speech
- **Company Knowledge Base**: Trained on NextCore AI services and information
- **Scalable Architecture**: Built with FastAPI for high performance

## 📁 Project Structure

```
AI-Agent/
├── .env                         # API keys and configuration
├── requirements.txt             # Python dependencies
├── setup.py                     # Setup and initialization script
├── README.md                    # This file
│
├── agent/                       # RAG (Knowledge Base) System
│   ├── config.py                # Configuration and environment variables
│   ├── load_documents.py        # Document loading and embedding
│   ├── query_agent.py           # Query processing and response generation
│   └── knowledge_base/
│       └── services.md          # Company services documentation
│
├── api/                         # Twilio API and Server
│   ├── main.py                  # FastAPI server and Twilio webhook
│   ├── twilio_webhook.py        # Twilio-specific webhook handlers
│   └── call_response.py         # Core response generation logic
│
├── voice/                       # Audio Processing
│   ├── audio_utils.py           # Audio file utilities
│   ├── speech_to_text.py        # Speech-to-text conversion
│   └── text_to_speech.py        # Text-to-speech conversion
│
└── data/
    ├── call_logs/               # Call conversation logs
    └── recordings/              # Audio recordings (optional)
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

Create/update your `.env` file:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Optional
ELEVENLABS_API_KEY=your_elevenlabs_key
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
```

### 3. Initialize Knowledge Base

```bash
python setup.py
```

### 4. Start the Server

```bash
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Setup Twilio Webhook

1. Use ngrok for local testing:
   ```bash
   ngrok http 8000
   ```

2. In Twilio Console, set webhook URL to:
   ```
   https://your-ngrok-url.ngrok.io/voice
   ```

## 🔧 How It Works

1. **Call Received** → Twilio forwards to `/voice` endpoint
2. **Speech Recognition** → OpenAI Whisper converts speech to text  
3. **Knowledge Query** → Vector search finds relevant company info
4. **AI Response** → GPT generates contextual answer
5. **Speech Output** → TwiML converts response to speech
6. **Conversation Loop** → Continues until call ends

## 📞 Testing

```bash
# Test knowledge base
python agent/query_agent.py

# Test API endpoint
curl -X POST http://localhost:8000/voice -d "SpeechResult=What services do you offer?"
```

## 🛠️ Customization

### Adding New Knowledge
1. Edit `agent/knowledge_base/services.md`
2. Re-run: `python agent/load_documents.py`

### Changing Voice Settings
Edit `api/main.py`:
```python
twiml.say(response_text, voice='Polly.Matthew', language='en-US')
```

## 🚀 Deployment

Ready for deployment on:
- Heroku
- AWS ECS/Lambda
- Google Cloud Run
- DigitalOcean App Platform

## 🆘 Troubleshooting

**Knowledge base errors**: Run `python agent/load_documents.py`
**Webhook issues**: Check ngrok tunnel and Twilio configuration
**API errors**: Verify all API keys in `.env` file

---

**Built with ❤️ by NextCore AI Team**