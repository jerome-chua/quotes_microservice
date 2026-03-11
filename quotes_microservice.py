import zmq
import json
import random

QUOTES = [
    "Believe you can & you're halfway there.",
    "The only way to do great work is to love what you do.",
    "Act as if what you do makes a difference. It does.",
    "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "What lies behind us and what lies before us are tiny matters compared to what lies within us.",
    "In the middle of every difficulty lies opportunity.",
    "It always seems impossible until it's done.",
    "You are never too old to set another goal or to dream a new dream.",
]

def get_quote():
    return random.choice(QUOTES)

def start_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")
    print("Inspirational Quote Microservice is running on port 5556...")

    while True:
        message = socket.recv_string()
        try:
            request = json.loads(message)
            input_value = request.get("input")

            if input_value is None or input_value == "":
                quote = get_quote()
                socket.send_string(json.dumps({"quote": quote}))
            else:
                socket.send_string(json.dumps({"error": "Input must be empty/null to receive a quote."}))

        except Exception as e:
            socket.send_string(json.dumps({"error": str(e)}))


if __name__ == "__main__":
    start_server()
