from flask import Flask, request
import json
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/paykassa", methods=["POST"])
def paykassa_handler():
    data = request.form.to_dict()

    if data.get("status") == "success" and data.get("order_id"):
        user_id = data.get("order_id")

        with open("users.json", "r") as f:
            users = json.load(f)

        until = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        users[user_id] = {"sub_until": until}

        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)

        return "OK"
    return "FAIL"

@app.route("/", methods=["GET"])
def index():
    return "Paykassa Webhook is running"

app.run(host="0.0.0.0", port=5000)
