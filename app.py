from flask import Flask, render_template, request, jsonify
from ai_engine import humanize_text, get_installed_models
import threading


app = Flask(__name__)


# =========================
# SERVER LIMITS
# =========================

MAX_ACTIVE_USERS = 15
MAX_WORDS = 1000

active_users = 0
user_lock = threading.Lock()


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# GET INSTALLED OLLAMA MODELS
# =========================

@app.route("/models", methods=["GET"])
def models():

    try:

        installed_models = get_installed_models()

        return jsonify({
            "success": True,
            "models": installed_models
        })

    except Exception as error:

        print("MODEL ERROR:", error)

        return jsonify({
            "success": False,
            "models": [],
            "message": "Could not load Ollama models."
        }), 500


# =========================
# HUMANIZE TEXT
# =========================

@app.route("/humanize", methods=["POST"])
def humanize():

    global active_users

    # =========================
    # ACTIVE USER LIMIT
    # =========================

    with user_lock:

        if active_users >= MAX_ACTIVE_USERS:

            return jsonify({
                "success": False,
                "message": (
                    "All 15 AI processing slots are currently busy. "
                    "Please try again later."
                )
            }), 429

        active_users += 1

    try:

        # =========================
        # READ REQUEST
        # =========================

        data = request.get_json(silent=True)

        if not data:

            return jsonify({
                "success": False,
                "message": "Invalid request."
            }), 400

        text = data.get(
            "text",
            ""
        ).strip()

        tone = data.get(
            "tone",
            "Natural"
        )

        model = data.get(
            "model",
            ""
        ).strip()


        # =========================
        # EMPTY TEXT CHECK
        # =========================

        if not text:

            return jsonify({
                "success": False,
                "message": "Please enter some text."
            }), 400


        # =========================
        # WORD COUNT
        # =========================

        word_count = len(
            text.split()
        )

        if word_count > MAX_WORDS:

            return jsonify({
                "success": False,
                "message": (
                    f"Your text contains {word_count} words. "
                    f"The maximum allowed is {MAX_WORDS} words."
                )
            }), 400


        # =========================
        # GET INSTALLED MODELS
        # =========================

        installed_models = get_installed_models()

        if not installed_models:

            return jsonify({
                "success": False,
                "message": (
                    "No Ollama models were found. "
                    "Please install a model using Ollama."
                )
            }), 400


        # =========================
        # DEFAULT MODEL
        # =========================

        if not model:

            model = installed_models[0]


        # =========================
        # CHECK SELECTED MODEL
        # =========================

        if model not in installed_models:

            return jsonify({
                "success": False,
                "message": (
                    f"The selected model '{model}' "
                    "is not installed."
                )
            }), 400


        # =========================
        # HUMANIZE
        # =========================

        result = humanize_text(
            text,
            tone,
            model
        )


        # =========================
        # RESPONSE
        # =========================

        return jsonify({
            "success": True,
            "result": result,
            "word_count": word_count,
            "model": model
        })


    except Exception as error:

        print("AI ERROR:", error)

        return jsonify({
            "success": False,
            "message": (
                "AI processing failed. "
                "Please make sure Ollama is installed "
                "and running."
            )
        }), 500


    finally:

        # Always release processing slot

        with user_lock:

            active_users -= 1


# =========================
# AI CHECK
# =========================

@app.route("/check", methods=["POST"])
def check():

    try:

        data = request.get_json(silent=True)

        if not data:

            return jsonify({
                "success": False,
                "message": "Invalid request."
            }), 400


        text = data.get(
            "text",
            ""
        ).strip()


        if not text:

            return jsonify({
                "success": False,
                "message": "Please enter some text."
            }), 400


        # =========================
        # WORD COUNT
        # =========================

        word_count = len(
            text.split()
        )


        if word_count > MAX_WORDS:

            return jsonify({
                "success": False,
                "message": (
                    f"Your text contains {word_count} words. "
                    f"The maximum allowed is {MAX_WORDS} words."
                )
            }), 400


        # =========================
        # SENTENCE SPLITTING
        # =========================

        sentences = [
            sentence.strip()
            for sentence in (
                text
                .replace("!", ".")
                .replace("?", ".")
                .split(".")
            )
            if sentence.strip()
        ]


        sentence_count = len(sentences)


        # =========================
        # SENTENCE LENGTH
        # =========================

        if sentence_count > 0:

            sentence_lengths = [
                len(sentence.split())
                for sentence in sentences
            ]

            average_length = (
                sum(sentence_lengths)
                / len(sentence_lengths)
            )

        else:

            average_length = 0


        # =========================
        # SENTENCE VARIATION
        # =========================

        if sentence_count >= 3:

            unique_lengths = len(
                set(sentence_lengths)
            )

            variation = (
                unique_lengths
                / sentence_count
            ) * 100

        else:

            variation = 50


        # =========================
        # AI-LIKENESS SCORE
        # =========================
        #
        # This is a simple writing-pattern
        # estimate, not a real AI detector.
        #
        # Lower score = more natural patterns.
        # =========================

        ai_score = 8


        # Natural variation
        if variation >= 70:

            ai_score -= 2

        elif variation >= 55:

            ai_score -= 1


        # Moderate sentence length
        if 10 <= average_length <= 24:

            ai_score -= 1


        # Very uniform sentence lengths
        if variation < 30:

            ai_score += 3


        # Extremely long sentences
        if average_length > 35:

            ai_score += 2


        # Extremely short sentences
        if 0 < average_length < 7:

            ai_score += 1


        # =========================
        # LIMIT SCORE
        # =========================

        ai_score = max(
            3,
            min(
                9,
                int(ai_score)
            )
        )


        human_score = 100 - ai_score


        # =========================
        # ANALYSIS MESSAGE
        # =========================

        if ai_score <= 5:

            analysis = (
                "The text shows strong natural variation "
                "in sentence structure and length. "
                "Few of the patterns checked by this tool "
                "appear AI-like."
            )

        elif ai_score <= 7:

            analysis = (
                "The text shows mostly natural sentence "
                "variation and structure. Only a small "
                "number of AI-like patterns were detected."
            )

        else:

            analysis = (
                "The text shows generally natural writing "
                "patterns, although some structured patterns "
                "were detected."
            )


        # =========================
        # RESPONSE
        # =========================

        return jsonify({

            "success": True,

            "ai_score": ai_score,

            "human_score": human_score,

            "analysis": analysis,

            "word_count": word_count,

            "variation": round(
                variation,
                1
            )

        })


    except Exception as error:

        print(
            "AI CHECK ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "message": (
                "AI Check failed. "
                "Please try again."
            )

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