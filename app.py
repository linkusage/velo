from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/api/trm")
def get_trm():
    try:
        url = "https://www.dolar-colombia.com/"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Selector equivalent to your XPath
        trm_span = soup.select_one(
            "body > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > "
            "div:nth-of-type(1) > div > div:nth-of-type(2) > h2 > span"
        )

        if not trm_span:
            return jsonify({"error": "TRM element not found"}), 500

        trm_value = float(
            trm_span.text.replace(",", ".").replace("$", "").replace(" ", "")
        )

        return jsonify({"trm": trm_value})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "✅ TRM API is running"

if __name__ == "__main__":
    app.run()
