from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables (for local dev only)
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins (or restrict to your Vercel domain)

WHOISXML_API_KEY = os.getenv("WHOISXML_API_KEY")
WHOISXML_ENDPOINT = "https://www.whoisxmlapi.com/whoisserver/WhoisService"

@app.route("/check", methods=["GET"])
def check_domain():
    """
    Check if a domain is available using WhoisXML API.
    Example: /check?domain=example.com
    """
    domain = request.args.get("domain")
    if not domain:
        return jsonify({"error": "Please provide a domain parameter"}), 400

    params = {
        "apiKey": WHOISXML_API_KEY,
        "domainName": domain,
        "outputFormat": "JSON"
    }

    try:
        response = requests.get(WHOISXML_ENDPOINT, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        whois_record = data.get("WhoisRecord")
        available = not bool(whois_record and whois_record.get("registryData"))

        return jsonify({
            "domain": domain,
            "available": available
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Important for Render: don't use app.run()
# Gunicorn will look for "app:app"
if __name__ == "__main__":
    # Use Render's PORT or default to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


