# Webhook to handle voice calls via Twilio
from fastapi import APIRouter, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse
from agent.query_agent import query_agent

router = APIRouter()

@router.post("/webhook")
async def handle_call(request: Request):
    form = await request.form()
    user_text = form.get("SpeechResult")

    if user_text:
        answer = query_agent(user_text)
    else:
        answer = "I'm sorry, I didn't catch that. Could you repeat?"

    resp = VoiceResponse()
    resp.say(answer, voice='alice')
    return Response(content=str(resp), media_type="application/xml")
