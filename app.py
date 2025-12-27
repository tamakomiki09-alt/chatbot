from flask import Flask, render_template, request, jsonify
from database import save_message
import uuid

app = Flask(__name__)

# Unique session ID per visitor (simple version)
session_id = str(uuid.uuid4())


@app.route("/")
def home():
    return render_template("chat.html")



@app.route("/ask", methods=["POST"])
def ask():
    user_msg = request.json.get("message")

    # Temporary AI response (we replace with GPT later)
    ai_msg = "Thank you for your message! (AI response goes here)"

    # Save to database
    save_message(
        session_id=session_id,
        user_msg=user_msg,
        ai_msg=ai_msg,
        category=None,          # will fill this in next steps
        keywords=None,          # auto-extract later
        interest=None,          # from user preferences
        time_pref=None,         # from user
        mobility=None,          # from user
        escalated=False
    )

    return jsonify({"answer": ai_msg})


if __name__ == "__main__":
    app.run(debug=True, port=5001)

from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    # TEMPORARY: simple response (AI comes next)
    bot_reply = f"You said: {user_message}"

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True, port=5001)

