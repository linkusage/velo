from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/api/trm")
def get_trm():
    try:
        url = "https://www.dolar-colombia.com/"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # CSS selector equivalent to your XPath
        trm_span = soup.select_one(
            "body > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > "
            "div:nth-of-type(1) > div > div:nth-of-type(2) > h2 > span"
        )

        if not trm_span:
            return jsonify({"error": "TRM element not found"}), 500

        raw = trm_span.text.strip()

        # Remove currency symbol or spaces
        raw = raw.replace("$", "").replace(" ", "")

        # Fix formatting like 3.872.47 → 3872.47
        if raw.count(".") > 1:
            parts = raw.split(".")
            corrected = "".join(parts[:-1]) + "." + parts[-1]
        else:
            corrected = raw

        trm_value = float(corrected)

        return jsonify({"trm": trm_value})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "✅ TRM API is running"


if __name__ == "__main__":
    # For local testing (Render uses gunicorn instead)
    app.run(host="0.0.0.0", port=5000)
