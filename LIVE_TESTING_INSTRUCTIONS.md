# 🎯 NextCore AI Voice Agent - LIVE TESTING

## 🚀 Step-by-Step Live Testing Instructions

### ✅ Your System Status: READY FOR LIVE TESTING!

---

## 🎬 STEP 1: Start Your Server

**Command:**
```bash
python start_exotel.py
```

**Expected Output:**
```
🎙️ NextCore AI Voice Agent - Exotel Edition
🚀 Starting production server...
📞 Exotel webhook: /exotel-voice-webhook
🌐 Server: http://localhost:8000
✅ Ready for Exotel integration!
```

---

## 🌐 STEP 2: Start ngrok Tunnel

**Command:**
```bash
ngrok http 8000
```

**Expected Output:**
```
Forwarding    https://abc123.ngrok.io -> http://localhost:8000
```

**📝 Action:** Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

---

## 📱 STEP 3: Configure Exotel Dashboard

### 🔧 Exotel Setup (CRITICAL STEPS):

1. **Login** to your Exotel account
2. **Go to** Numbers → Your ExoPhone
3. **Find** Flow/Passthru settings
4. **Set Passthru URL:** 
   ```
   https://your-ngrok-url.ngrok.io/exotel-voice-webhook
   ```
5. **Set Method:** POST
6. **🚨 DISABLE PIN Authentication** (CRITICAL!)
7. **Save** settings

### ⚠️ Common Issues:
- If PIN is enabled → Call will ask for PIN and disconnect
- If URL is wrong → Call will not reach your server
- If method is GET → May not work properly

---

## 📞 STEP 4: Test Live Call

### 🎯 Call Your Exotel Number

**Expected Call Flow:**
```
📞 You call: Your Exotel number
🤖 AI says: "Hello! Welcome to NextCore AI. How can I help you today?"
👤 You say: "What services do you offer?"
🤖 AI responds: Professional response about NextCore AI services
📞 Conversation continues...
```

### ✅ Success Indicators:
- ✅ NO PIN is asked
- ✅ AI greeting plays immediately
- ✅ You can speak your question
- ✅ AI responds professionally
- ✅ Call doesn't disconnect

### ❌ Failure Indicators:
- ❌ PIN is asked
- ❌ Call disconnects immediately
- ❌ No AI response
- ❌ Error messages

---

## 🔍 STEP 5: Monitor & Debug

### 📊 Check System Status:
```bash
# Verify all components
python verify_system.py

# Diagnose any issues
python diagnose_exotel.py

# Check server logs in terminal
```

### 🌐 Test Endpoints Manually:
```bash
# Test main endpoint
curl http://localhost:8000/

# Test webhook
curl "http://localhost:8000/exotel-voice-webhook?From=test&CallSid=123"
```

---

## 🔧 TROUBLESHOOTING

### ❌ If Call Asks for PIN:
```
Problem: Call asks "Please enter your PIN"
Solution: 
1. Go to Exotel Dashboard
2. Numbers → Settings
3. DISABLE PIN authentication
4. Save and test again
```

### ❌ If Call Disconnects:
```
Problem: Call connects but disconnects immediately
Solutions:
1. Check ngrok URL is correct in Exotel
2. Restart ngrok: ngrok http 8000
3. Update new URL in Exotel dashboard
4. Verify server is running
```

### ❌ If No AI Response:
```
Problem: AI doesn't speak
Solutions:
1. Check server logs for errors
2. Verify webhook URL format
3. Test endpoint manually
4. Check Exotel logs in dashboard
```

---

## 🎉 SUCCESS CRITERIA

### ✅ Live Testing is Successful When:
- [ ] Call connects without PIN prompt
- [ ] AI greeting plays: "Hello! Welcome to NextCore AI..."
- [ ] Customer can speak questions
- [ ] AI responds with relevant information
- [ ] Conversation flows naturally
- [ ] Call doesn't disconnect unexpectedly

---

## 📞 QUICK TEST COMMANDS

```bash
# 1. Start everything
python start_exotel.py
# (In another terminal)
ngrok http 8000

# 2. Quick server test
curl http://localhost:8000/

# 3. Quick webhook test  
curl "http://localhost:8000/exotel-voice-webhook?From=test123&CallSid=abc"

# 4. Call your Exotel number!
```

---

## 🆘 If Still Having Issues:

1. **Share Exotel flow screenshot**
2. **Check Exotel dashboard logs**
3. **Share server terminal output**
4. **Test with different phone numbers**
5. **Contact Exotel support if needed**

---

## 🎯 आपका AI Voice Agent Live Testing के लिए तैयार है!

**अब बस यह करें:**
1. ✅ Server start करें
2. ✅ ngrok start करें  
3. ✅ Exotel में URL update करें
4. ✅ PIN disable करें
5. ✅ Test call करें!

**🎉 Success होने पर आपको सुनाई देगा:**
*"Hello! Welcome to NextCore AI. How can I help you today?"*
