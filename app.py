from flask import Flask, jsonify, request
from flask_cors import CORS
import random

from dotenv import load_dotenv
load_dotenv()

from groq import Groq

app = Flask(__name__)
CORS(app)

QUOTES = [
    "Believe you can & you're halfway there. (No pressure though.)",
    "The only way to do great work is to love what you do. Or at least tolerate it with coffee.",
    "Act as if what you do makes a difference. It does. Probably.",
    "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "What lies behind us and what lies before us are tiny matters compared to what lies within us.",
    "In the middle of every difficulty lies opportunity. Also snacks. Don't forget snacks.",
    "It always seems impossible until it's done. Then it seems obvious.",
    "You are never too old to set another goal or to dream a new dream.",
    "The best time to plant a tree was 20 years ago. The second best time is now. The third best time is after lunch.",
    "Everything you've ever wanted is on the other side of fear. And maybe a nap.",
]

last_quote = None

groq_client = Groq()


def get_quote_from_pool():
    """Select a random quote from the pool, ensuring no consecutive repeats."""
    global last_quote
    available = [q for q in QUOTES if q != last_quote] if last_quote else QUOTES
    quote = random.choice(available)
    last_quote = quote
    return quote


def get_quote_from_llm():
    """Generate a playful inspirational quote using Groq LLM."""
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an inspirational quote generator with a playful, "
                    "humorous twist. Return only a single short inspirational quote "
                    "with a touch of humor. No extra commentary, no quotation marks."
                ),
            },
            {
                "role": "user",
                "content": "Give me one unique inspirational quote with a playful twist.",
            },
        ],
    )
    return response.choices[0].message.content.strip()


def get_quote():
    """Try LLM first, fall back to the local quote pool."""
    global last_quote
    used_fallback = False
    try:
        quote = get_quote_from_llm()
        if quote == last_quote:
            quote = get_quote_from_pool()
            used_fallback = True
        else:
            last_quote = quote
    except Exception as e:
        err_str = str(e)
        if "429" in err_str or "rate_limit" in err_str.lower():
            print("Groq rate limit hit. Using local quote pool.")
        else:
            print(f"LLM failed, falling back to local pool: {e}")
        quote = get_quote_from_pool()
        used_fallback = True

    return quote, used_fallback


def add_quote(new_quote):
    """Dynamically add a quote to the pool at runtime."""
    if new_quote and new_quote not in QUOTES:
        QUOTES.append(new_quote)
        return True
    return False


@app.route("/quote", methods=["GET"])
def quote_get():
    """Get a random inspirational quote."""
    try:
        quote, used_fallback = get_quote()
        return jsonify({"quote": quote, "fallback_used": used_fallback})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/quote", methods=["POST"])
def quote_add():
    """Add a new quote to the pool."""
    body = request.get_json()
    if not body or "quote" not in body:
        return jsonify({"error": "Request body must include a 'quote' field."}), 400

    if add_quote(body["quote"]):
        return jsonify({"status": "Quote added successfully."}), 201
    return jsonify({"error": "Quote is empty or already exists."}), 400


if __name__ == "__main__":
    app.run(port=5001, debug=True)
