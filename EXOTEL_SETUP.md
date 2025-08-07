# 📞 Exotel Integration Guide

Complete setup instructions for integrating NextCore AI Voice Agent with Exotel telephony service.

## 🎯 Overview

This guide will help you configure Exotel to work with your AI voice agent for handling live customer calls.

## 🔧 Prerequisites

- ✅ Exotel account with phone number
- ✅ AI Voice Agent server running
- ✅ ngrok for public tunnel (development)
- ✅ HTTPS endpoint (production)

## 🚀 Quick Setup

### Step 1: Start Your Server
```bash
python start_exotel.py
```

### Step 2: Create Public Tunnel
```bash
# For development
ngrok http 8000

# Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
```

### Step 3: Configure Exotel Dashboard

1. **Login to Exotel Console**
   - Go to your Exotel dashboard
   - Navigate to Numbers section

2. **Select Your ExoPhone**
   - Choose the phone number to configure
   - Go to Settings or Flow configuration

3. **Set Passthru URL**
   ```
   URL: https://your-ngrok-url.ngrok.io/exotel-voice-webhook
   Method: POST
   ```

4. **🚨 CRITICAL: Disable PIN Authentication**
   - Find PIN/Authentication settings
   - Disable PIN verification
   - This is essential for AI to work

5. **Save Configuration**

### Step 4: Test Integration
```bash
# Call your Exotel number
# Expected: "Hello! Welcome to NextCore AI..."
```

## 🔧 Webhook Endpoints

| Endpoint | Purpose | Method |
|----------|---------|--------|
| `/exotel-voice-webhook` | Main webhook | GET/POST |
| `/direct-voice` | Alternative endpoint | GET/POST |
| `/health` | Status check | GET |

## 📞 Expected Call Flow

```
1. 📞 Customer calls Exotel number
2. 🔄 Exotel forwards to webhook
3. 🤖 AI: "Hello! Welcome to NextCore AI..."
4. 👤 Customer speaks question
5. 🧠 AI processes with knowledge base
6. 🔊 AI responds professionally
7. 🔄 Conversation continues
```

## 🛠️ Troubleshooting

### ❌ Call Asks for PIN
**Problem**: Call prompts for PIN instead of AI greeting

**Solutions**:
- Check Exotel dashboard settings
- Disable PIN authentication
- Verify flow configuration
- Contact Exotel support if needed

### ❌ Call Disconnects Immediately
**Problem**: Call connects but drops quickly

**Solutions**:
- Verify webhook URL is correct
- Check ngrok tunnel is active
- Restart ngrok: `ngrok http 8000`
- Update new URL in Exotel dashboard

### ❌ No AI Response
**Problem**: Call connects but AI doesn't speak

**Solutions**:
- Check server logs for errors
- Verify OpenAI API key
- Test webhook manually:
  ```bash
  curl "http://localhost:8000/exotel-voice-webhook?From=test&CallSid=123"
  ```

### ❌ Webhook Not Receiving Calls
**Problem**: Server not getting webhook requests

**Solutions**:
- Confirm ngrok URL matches Exotel setting
- Check Exotel logs in dashboard
- Verify POST method is selected
- Test with different endpoint: `/direct-voice`

## 🌐 Production Deployment

### Domain Setup
```bash
# Instead of ngrok, use your domain
https://yourdomain.com/exotel-voice-webhook
```

### SSL Certificate
- Exotel requires HTTPS endpoints
- Use Let's Encrypt or cloud provider SSL
- Verify certificate is valid

### Server Configuration
```bash
# Production server
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📊 Monitoring

### Health Checks
```bash
# Server health
curl https://yourdomain.com/health

# Webhook test
curl "https://yourdomain.com/exotel-voice-webhook?From=test&CallSid=123"
```

### Logs
- Monitor server logs for errors
- Check Exotel dashboard logs
- Set up alerting for failures

## 🔒 Security

- Use HTTPS for all webhooks
- Validate incoming requests
- Implement rate limiting
- Monitor for abuse

## 📞 Support

Need help with Exotel integration?

- **NextCore AI**: nextcoreai.in@gmail.com, +91 6202579799
- **Exotel Support**: Check Exotel documentation
- **Technical Issues**: See troubleshooting section above

---

**🎉 Ready to handle live customer calls with AI!**
