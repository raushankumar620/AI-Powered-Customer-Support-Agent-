# Exotel webhook handler for NextCore AI Voice Agent
from fastapi import APIRouter, Request, Form
from fastapi.responses import Response
import logging
from api.fallback_agent import query_agent
from openai import AsyncOpenAI
from agent.config import OPENAI_API_KEY

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.post("/exotel-voice-webhook")
@router.get("/exotel-voice-webhook")
async def handle_exotel_call(request: Request):
    """Handle incoming Exotel voice calls (POST) and testing (GET)"""
    try:
        method = request.method
        logger.info(f"Received {method} request to /exotel-voice-webhook")
        
        # Get query parameters for both GET and POST
        query_params = dict(request.query_params)
        logger.info(f"Query parameters: {query_params}")
        
        if method == "GET":
            # Exotel is sending GET request - handle it like a call
            caller_number = query_params.get("From", query_params.get("CallFrom", "Unknown"))
            call_sid = query_params.get("CallSid", "")
            
            logger.info(f"GET request call - From: {caller_number}, CallSid: {call_sid}")
            logger.info(f"All query params: {query_params}")
            
            # Generate initial greeting for GET request
            ai_response = await generate_greeting(caller_number)
            exotel_response = create_exotel_response(ai_response)
            
            logger.info(f"Sending XML response for GET request: {len(exotel_response)} chars")
            logger.info(f"XML Content: {exotel_response[:200]}...")
            return Response(content=exotel_response, media_type="application/xml")
        
        # Handle POST request from Exotel
        if method == "POST":
            # Get form data from Exotel
            form = await request.form()
            form_data = dict(form)
            
            logger.info(f"POST request received with form data: {form_data}")
            
            # Extract caller information
            caller_number = form.get("From", "Unknown")
            call_sid = form.get("CallSid", "")
            speech_result = form.get("SpeechResult", "")
            digits = form.get("Digits", "")
            call_status = form.get("CallStatus", "")
            
            logger.info(f"POST request call - From: {caller_number}, CallSid: {call_sid}, Speech: '{speech_result}', Digits: {digits}, Status: {call_status}")
            
            # Generate AI response based on input
            if speech_result and speech_result.strip() and speech_result.strip().lower() not in ["", "null", "undefined"]:
                # Customer spoke something - generate contextual response
                logger.info(f"Processing speech: '{speech_result}'")
                ai_response = await generate_ai_response(caller_number, speech_result)
            elif digits and digits.strip():
                # Customer pressed digits
                logger.info(f"Processing digits: {digits}")
                ai_response = await handle_digit_input(digits)
            else:
                # Initial greeting or no speech detected
                logger.info("Generating initial greeting for POST")
                ai_response = await generate_greeting(caller_number)
            
            # Create Exotel response XML
            exotel_response = create_exotel_response(ai_response)
            logger.info(f"Sending XML response for POST: {len(exotel_response)} chars")
            logger.info(f"XML Content: {exotel_response[:200]}...")
            
            return Response(content=exotel_response, media_type="application/xml")
        
        # Fallback for any other method
        logger.warning(f"Unexpected method: {method}")
        fallback_response = create_exotel_response("Welcome to NextCore AI. How can I help you today?")
        return Response(content=fallback_response, media_type="application/xml")
        
    except Exception as e:
        logger.error(f"Error in Exotel webhook: {str(e)}")
        # Fallback response
        fallback_response = create_exotel_response(
            "I apologize, but I'm experiencing technical difficulties. Please call back later or contact us at nextcoreai.in@gmail.com"
        )
        return Response(content=fallback_response, media_type="application/xml")

async def generate_greeting(caller_number: str) -> str:
    """Generate personalized greeting for the caller"""
    
    # English greeting prompt
    prompt = f"A customer with number {caller_number} just called NextCore AI. Greet them politely and ask how we can assist with NextCore AI services. Keep it brief and professional."
    
    # Hindi greeting option (uncomment if needed)
    # prompt = f"Ek customer {caller_number} number se NextCore AI ko call kar raha hai. Use Hindi me greet karo aur NextCore AI services ke baare me kaise help kar sakte hain ye poocho. Brief aur professional rakhna."
    
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional customer service representative for NextCore AI, a Bangalore-based digital transformation company. Be warm, helpful, and concise. Respond in under 50 words."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logger.error(f"Error generating greeting: {str(e)}")
        return "Hello and welcome to NextCore AI! We are Bangalore's leading digital transformation company specializing in AI automation, web development, mobile applications, and cloud services. How may I assist you today?"

async def generate_ai_response(caller_number: str, user_speech: str) -> str:
    """Generate AI response based on user speech and company knowledge"""
    
    try:
        # Use RAG system to get contextual response
        rag_response = query_agent(user_speech)
        
        # Enhance with conversational context
        prompt = f"""
        Customer {caller_number} said: "{user_speech}"
        
        Based on NextCore AI's services, here's the relevant information: {rag_response}
        
        Please provide a conversational, helpful response that:
        1. Addresses their question directly
        2. Mentions relevant NextCore AI services
        3. Keeps it under 80 words for phone conversation
        4. Sounds natural and professional
        5. Asks if they need more information
        """
        
        response = await openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful customer service agent for NextCore AI. Provide clear, concise responses about our services. Always be professional and helpful. Keep responses under 80 words for phone calls."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logger.error(f"Error generating AI response: {str(e)}")
        return f"Thank you for asking about {user_speech}. NextCore AI provides comprehensive digital transformation services including AI automation, web development, mobile apps, and cloud solutions. For detailed information, please contact us at nextcoreai.in@gmail.com or +91 6202579799. How else can I help you?"

async def handle_digit_input(digits: str) -> str:
    """Handle digit input from customer"""
    
    try:
        if digits == "1":
            return "Great! You've chosen to speak with our AI agent. Please tell me about your requirements for NextCore AI services - whether it's AI automation, web development, mobile apps, or cloud solutions."
        elif digits == "2":
            return "Thank you for choosing to leave a message. Please speak after the beep and tell us about your requirements. We'll get back to you within 24 hours."
        elif digits == "0":
            return "Connecting you to our support team. Please hold on while we transfer your call."
        else:
            return f"You pressed {digits}. For AI services press 1, to leave a message press 2, or speak directly about your requirements."
            
    except Exception as e:
        logger.error(f"Error handling digit input: {str(e)}")
        return "Thank you for your input. Please tell me how I can help you with NextCore AI services."

def create_exotel_response(message: str) -> str:
    """Create Exotel-compatible XML response - Simple and Direct"""
    
    # Clean the message for XML safety
    clean_message = message.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    # Direct conversation - no PIN, no complex gathering
    xml_response = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="woman">{clean_message}</Say>
    <Gather input="speech" timeout="15" speechTimeout="auto" action="/exotel-voice-webhook" method="POST">
        <Say voice="woman">Please tell me how I can help you with NextCore AI services.</Say>
    </Gather>
    <Say voice="woman">Thank you for calling NextCore AI. For more information, contact us at nextcoreai.in@gmail.com. Have a great day!</Say>
</Response>'''
    
    return xml_response.strip()

# Hindi version (uncomment if needed)
def create_exotel_response_hindi(message: str) -> str:
    """Create Exotel-compatible XML response in Hindi"""
    
    clean_message = message.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    xml_response = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="woman" language="hi-IN">{clean_message}</Say>
    <Gather input="speech" timeout="8" speechTimeout="3" action="/exotel-voice-webhook" method="POST" language="hi-IN">
        <Say voice="woman" language="hi-IN">Kripaya bataiye main aapki kaise madad kar sakti hun.</Say>
    </Gather>
    <Say voice="woman" language="hi-IN">Sunai nahi diya. NextCore AI ko call karne ke liye dhanyawad!</Say>
</Response>'''
    
    return xml_response.strip()

@router.post("/simple-test")
async def simple_exotel_test():
    """Simple test endpoint that just returns basic XML"""
    xml_response = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="woman">Hello! This is NextCore AI. Your webhook is working perfectly!</Say>
</Response>'''
    
    return Response(content=xml_response.strip(), media_type="application/xml")

@router.post("/direct-voice")
@router.get("/direct-voice") 
async def direct_voice_handler(request: Request):
    """Direct voice handler - bypasses any PIN authentication"""
    
    try:
        method = request.method
        logger.info(f"Direct voice handler - {method} request received")
        
        # Simple direct response without PIN
        greeting = "Hello and welcome to NextCore AI! We are Bangalore's leading digital transformation company. We provide AI automation, web development, mobile apps, and cloud services. Please tell me how I can help you today."
        
        xml_response = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="woman">{greeting}</Say>
    <Gather input="speech" timeout="15" action="/direct-voice" method="POST">
        <Say voice="woman">I'm listening. How can NextCore AI help you?</Say>
    </Gather>
    <Say voice="woman">Thank you for calling NextCore AI. Contact us at nextcoreai.in@gmail.com. Goodbye!</Say>
</Response>'''
        
        logger.info(f"Direct voice response: {len(xml_response)} chars")
        return Response(content=xml_response.strip(), media_type="application/xml")
        
    except Exception as e:
        logger.error(f"Error in direct voice handler: {str(e)}")
        fallback = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="woman">Welcome to NextCore AI. We provide digital transformation services. Thank you for calling!</Say>
</Response>'''
        return Response(content=fallback.strip(), media_type="application/xml")

@router.get("/test-exotel")
async def test_exotel_endpoint():
    """Test endpoint to verify Exotel integration"""
    
    # Test the AI response generation
    test_response = query_agent("What services do you offer?")
    
    return {
        "status": "✅ NextCore AI Voice Agent is working!",
        "exotel_webhook": "/exotel-voice-webhook",
        "ngrok_setup": "Paste your ngrok URL in Exotel dashboard",
        "sample_response": test_response[:100] + "...",
        "contact": {
            "email": "nextcoreai.in@gmail.com",
            "phone": "+91 6202579799",
            "location": "Bangalore, India"
        }
    }

# Alternative Hindi response function
def create_exotel_response_hindi(message: str) -> str:
    """Create Exotel-compatible XML response in Hindi"""
    
    xml_response = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="woman" language="hi-IN">{message}</Say>
    <Gather input="speech" timeout="5" speechTimeout="auto" action="/exotel-voice-webhook" method="POST">
        <Say voice="woman" language="hi-IN">Kripaya bataiye main aapki aur kaise madad kar sakti hun.</Say>
    </Gather>
    <Say voice="woman" language="hi-IN">NextCore AI ko call karne ke liye dhanyawad. Aapka din shubh ho!</Say>
</Response>'''
    
    return xml_response
