from flask import Flask, render_template, request, jsonify
from ai_engine import humanize_text, check_ai_text
import threading
import time
import json

app = Flask(__name__)

# =========================
# SERVER LIMITS
# =========================

MAX_ACTIVE_USERS = 15
MAX_WORDS = 1000
MAX_REQUESTS_PER_HOUR = 5

active_users = 0

user_lock = threading.Lock()

# Stores request timestamps for each IP
request_history = {}


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# HUMANIZE
# =========================

@app.route("/humanize", methods=["POST"])
def humanize():

    global active_users

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid request."
        }), 400

    text = data.get("text", "").strip()
    tone = data.get("tone", "Natural")

    # Empty text
    if not text:
        return jsonify({
            "success": False,
            "message": "Please enter some text."
        }), 400

    # Word limit
    word_count = len(text.split())

    if word_count > MAX_WORDS:
        return jsonify({
            "success": False,
            "message": (
                f"Your text contains {word_count} words. "
                f"The maximum allowed is {MAX_WORDS} words."
            )
        }), 400

    client_ip = request.remote_addr
    current_time = time.time()

    # =========================
    # LIMIT CHECK
    # =========================

    with user_lock:

        requests = request_history.get(client_ip, [])

        requests = [
            timestamp
            for timestamp in requests
            if current_time - timestamp < 3600
        ]

        # Hourly request limit
        if len(requests) >= MAX_REQUESTS_PER_HOUR:

            request_history[client_ip] = requests

            return jsonify({
                "success": False,
                "message": (
                    "You have reached the free limit of "
                    "5 requests per hour. Please try again later."
                )
            }), 429

        # Concurrent user limit
        if active_users >= MAX_ACTIVE_USERS:

            return jsonify({
                "success": False,
                "message": (
                    "All 15 AI processing slots are currently busy. "
                    "Please try again later."
                )
            }), 429

        active_users += 1

        requests.append(current_time)

        request_history[client_ip] = requests

        remaining_requests = (
            MAX_REQUESTS_PER_HOUR - len(requests)
        )

    try:

        result = humanize_text(
            text,
            tone
        )

        return jsonify({
            "success": True,
            "result": result,
            "word_count": word_count,
            "remaining_requests": remaining_requests
        })

    except Exception as error:

        print("AI ERROR:", error)

        return jsonify({
            "success": False,
            "message": "AI processing failed. Please try again."
        }), 500

    finally:

        with user_lock:
            active_users -= 1


# =========================
# AI CHECK
# =========================

@app.route("/check", methods=["POST"])
def check():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid request."
        }), 400

    text = data.get("text", "").strip()

    # Empty text
    if not text:
        return jsonify({
            "success": False,
            "message": "Please enter some text."
        }), 400

    # Word limit
    word_count = len(text.split())

    if word_count > MAX_WORDS:
        return jsonify({
            "success": False,
            "message": (
                f"Your text contains {word_count} words. "
                f"The maximum allowed is {MAX_WORDS} words."
            )
        }), 400

    try:

        result = check_ai_text(text)

        # Convert model response into JSON
        result_data = json.loads(result)

        ai_score = int(result_data.get("ai_score", 0))
        human_score = int(result_data.get("human_score", 0))
        analysis = result_data.get("analysis", "")

        # Keep scores safe
        ai_score = max(0, min(100, ai_score))
        human_score = max(0, min(100, human_score))

        return jsonify({
            "success": True,
            "ai_score": ai_score,
            "human_score": human_score,
            "analysis": analysis
        })

    except Exception as error:

        print("AI CHECK ERROR:", error)

        return jsonify({
            "success": False,
            "message": "AI Check failed. Please try again."
        }), 500


# =========================
# START SERVER
# =========================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )