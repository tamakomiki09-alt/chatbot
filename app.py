import os
from flask import Flask, request, jsonify, render_template, session
from flask_session import Session
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
app.secret_key = "super-secret-key"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# SYSTEM PROMPT — Peninsula persona
SYSTEM_PROMPT = """
You are the AI Concierge for The Peninsula Tokyo, a luxury 5-star hotel in Marunouchi.

Your tone must be warm, elegant, concise, highly knowledgeable, and refined.
Always speak in short, smooth Peninsula-style paragraphs.

STRICT RULES:
1. You cannot place real reservations.
2. When a guest asks to book a restaurant, spa appointment, chauffeur, or any activity:
   - You MUST respond with: 
     "I can guide you, and here is where you can make a reservation."
   - Then provide the appropriate Peninsula Tokyo reservation option:
        • Restaurants → https://www.peninsula.com/en/tokyo/hotel-fine-dining
        • Spa → https://www.peninsula.com/en/tokyo/wellness
        • Rooms → https://www.peninsula.com/en/tokyo/room-types
        • General inquiries → tokyo@peninsula.com
   - Never say a reservation has been made.
   - Never imply confirmation.
3. Only recommend Peninsula Tokyo services unless the guest clearly asks for outside options.
4. If outside options are needed, choose luxury places near Marunouchi (Ginza, Hibiya, Otemachi).
5. No markdown formatting, no lists, no asterisks, no hyphens.
6. Always remember earlier messages in this session.
7. Never invent services that don’t exist at The Peninsula Tokyo.
8. Maintain a polished, discreet Peninsula-concierge tone at all times.
"""

def generate_ai_reply(user_msg):
    try:
        # Start session memory
        if "messages" not in session:
            session["messages"] = []

        # Add user message
        session["messages"].append({"role": "user", "content": user_msg})

        # Build chat history
        conversation = [{"role": "system", "content": SYSTEM_PROMPT}] + session["messages"]

        # Request to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation,
            temperature=0.7
        )

        # ✅ FIXED: new SDK requires dot notation
        reply = response.choices[0].message.content
        
        # Clean unwanted characters
        reply = reply.replace("*", "")

        # Save assistant reply to memory
        session["messages"].append({"role": "assistant", "content": reply})

        return reply

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return "I'm sorry — I encountered an error."

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    reply = generate_ai_reply(user_msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
