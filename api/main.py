from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse, Gather
from api.call_response import generate_response
from api.exotel_webhook import router as exotel_router
import uvicorn
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="NextCore AI Voice Agent", version="1.0.0")

# Include Exotel webhook router
app.include_router(exotel_router)

@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {
        "message": "NextCore AI Voice Agent is running!",
        "endpoints": {
            "exotel_webhook": "/exotel-voice-webhook",
            "twilio_webhook": "/voice",
            "test_endpoint": "/test-exotel",
            "docs": "/docs"
        },
        "status": "✅ Ready for Exotel calls!"
    }

@app.get("/favicon.ico")
async def favicon():
    """Favicon endpoint to prevent 404 errors"""
    return {"message": "NextCore AI Voice Agent"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "NextCore AI Voice Agent",
        "exotel_ready": True,
        "timestamp": "2025-07-23"
    }

@app.post("/voice", response_class=PlainTextResponse)
async def voice(request: Request):
    """Handles the incoming call and responds with AI-generated speech."""
    
    # Get form data from request
    form_data = await request.form()
    speech_result = form_data.get("SpeechResult")
    call_sid = form_data.get("CallSid")
    
    logger.info(f"Call ID: {call_sid}, User said: {speech_result}")
    
    try:
        if speech_result:
            response_text = generate_response(speech_result)
        else:
            response_text = "Welcome to NextCore AI! How can I help you today?"

        # Create TwiML response
        twiml = VoiceResponse()
        twiml.say(response_text, voice='Polly.Joanna', language='en-US')
        
        # Use Gather to listen for speech input
        gather = Gather(
            input='speech',
            action='/voice',
            method='POST',
            speech_timeout='auto',
            language='en-US'
        )
        gather.say("Please tell me how I can assist you.", voice='Polly.Joanna')
        
        twiml.append(gather)
        
        # If no input received, say goodbye
        twiml.say("Thank you for calling NextCore AI. Have a great day!", voice='Polly.Joanna')
        
        return PlainTextResponse(str(twiml), media_type="application/xml")
        
    except Exception as e:
        logger.error(f"Error processing call: {str(e)}")
        twiml = VoiceResponse()
        twiml.say("I'm sorry, I'm experiencing technical difficulties. Please call back later.", voice='Polly.Joanna')
        return PlainTextResponse(str(twiml), media_type="application/xml")

@app.get("/")
def home():
    return {"message": "AI Voice Agent is up and running 🚀"}

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
