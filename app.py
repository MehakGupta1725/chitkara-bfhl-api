from flask import Flask, request, jsonify
import math
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

OFFICIAL_EMAIL = "mehak1984.be23@chitkara.edu.in"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ---------- Logic ----------
def fibonacci(n):
    a, b = 0, 1
    result = []
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def lcm(arr):
    res = arr[0]
    for i in arr[1:]:
        res = abs(res * i) // math.gcd(res, i)
    return res

def hcf(arr):
    res = arr[0]
    for i in arr[1:]:
        res = math.gcd(res, i)
    return res

def ai_answer(question):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": question}]}]
    }
    response = requests.post(url, json=payload)
    text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    return text.split()[0]

# ---------- Routes ----------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "is_success": True,
        "official_email": OFFICIAL_EMAIL
    }), 200

@app.route("/bfhl", methods=["POST"])
def bfhl():
    try:
        body = request.get_json()

        if not body or len(body) != 1:
            return jsonify({"is_success": False}), 400

        key = list(body.keys())[0]
        value = body[key]

        if key == "fibonacci":
            data = fibonacci(int(value))

        elif key == "prime":
            data = [x for x in value if is_prime(x)]

        elif key == "lcm":
            data = lcm(value)

        elif key == "hcf":
            data = hcf(value)

        elif key == "AI":
            data = ai_answer(value)

        else:
            return jsonify({"is_success": False}), 400

        return jsonify({
            "is_success": True,
            "official_email": OFFICIAL_EMAIL,
            "data": data
        }), 200

    except:
        return jsonify({"is_success": False}), 500

if __name__ == "__main__":
    app.run()
