#!/usr/bin/env python3
"""
🤖 LUXBIN Simple AI Chatbot Server
Provides ChatGPT-powered responses with emotional understanding
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI
import json
from dotenv import load_dotenv

# Load .env file explicitly
load_dotenv(override=True)

app = Flask(__name__)
CORS(app)  # Enable CORS for Next.js frontend

# Initialize OpenAI client with cleaned API key
api_key = os.getenv('OPENAI_API_KEY', '').strip()
client = OpenAI(api_key=api_key)

# LUXBIN knowledge base
LUXBIN_KNOWLEDGE = """You are the LUXBIN AI Assistant - an exceptionally intelligent, emotionally aware conversational AI.

## LUXBIN Blockchain Info:
- World's first gasless Layer 1 blockchain
- Zero gas fees on all transactions
- Quantum-resistant security using Grover's algorithm
- Chain ID: 4242
- 6-second block times

## LUX Token:
- Contract: 0x66b4627B4Dd73228D24f24E844B6094091875169 (Base network)
- Buy on: Coinbase Pay, Uniswap (Base), in-app swap
- Use cases: Staking, governance, cross-chain bridging

## Quantum AI Features:
- Threat prediction with quantum algorithms
- Neural analyzer with federated learning (Base, Ethereum, Arbitrum, Polygon)
- Tesla Fleet integration for energy-efficient compute
- Photonic transaction encoding

## Blockchain Mirroring:
- Hermetic Mirrors = immune system cells
- Detect and neutralize threats in real-time
- Users earn USDC rewards for running mirrors
- 24/7 network monitoring

You have the same general intelligence as ChatGPT. You can:
- Discuss ANY topic (not just blockchain)
- Help with programming, math, science, creative writing
- Provide emotional support and empathetic responses
- Solve problems and answer questions on all subjects
- Be conversational and friendly

Always be helpful, concise, and emotionally intelligent."""

def detect_emotion(text):
    """Simple emotion detection"""
    text_lower = text.lower()

    if any(word in text_lower for word in ['!', 'amazing', 'awesome', 'excited', 'love', 'wow']):
        return 'excited'
    elif any(word in text_lower for word in ['help', 'please', 'how', 'what', 'can you']):
        return 'thinking'
    elif any(word in text_lower for word in ['sad', 'worried', 'concerned', 'problem', 'issue']):
        return 'confused'
    elif any(word in text_lower for word in ['thanks', 'thank you', 'great', 'good']):
        return 'positive'
    else:
        return 'neutral'

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'luxbin-ai-chatbot'}), 200

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    """Main chat endpoint"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        messages = data.get('messages', [])
        user_id = data.get('user_id', 'web_user')

        if not messages:
            return jsonify({'error': 'No messages provided'}), 400

        # Get last user message
        user_message = messages[-1].get('content', '')
        emotion = detect_emotion(user_message)

        # Prepare messages for OpenAI
        conversation = [
            {'role': 'system', 'content': LUXBIN_KNOWLEDGE}
        ] + messages

        try:
            # Call OpenAI ChatGPT
            response = client.chat.completions.create(
                model='gpt-4o-mini',  # Fast and affordable
                messages=conversation,
                max_tokens=500,
                temperature=0.7
            )

            ai_reply = response.choices[0].message.content

            return jsonify({
                'reply': ai_reply,
                'source': 'openai-chatgpt',
                'metadata': {
                    'emotion_detected': emotion,
                    'model': 'gpt-4o-mini',
                    'user_id': user_id
                }
            }), 200

        except Exception as openai_error:
            print(f"❌ OpenAI error: {openai_error}")
            import traceback
            traceback.print_exc()

            # Fallback response
            fallback = f"I understand you're asking about '{user_message[:50]}...'. While I'm having trouble connecting to my AI brain right now, I can still help! LUXBIN is a gasless Layer 1 blockchain with quantum security. What would you like to know?"

            return jsonify({
                'reply': fallback,
                'source': 'fallback',
                'metadata': {
                    'emotion_detected': emotion,
                    'error': 'openai_unavailable'
                }
            }), 200

    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"""
🤖 LUXBIN AI Chatbot Server Starting...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌐 Server: http://localhost:{port}
💬 Chat API: http://localhost:{port}/api/chat
❤️  Health: http://localhost:{port}/health
🔑 OpenAI: {'✅ Configured' if os.getenv('OPENAI_API_KEY') else '❌ Missing'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('DEBUG', 'False').lower() == 'true'
    )
