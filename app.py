from datetime import datetime
import random
import string

from flask import Flask, request


app = Flask(__name__)


@app.route("/whoami")
def whoami():
    client_browser = request.user_agent.string
    client_ip = request.remote_addr
    current_time = datetime.now()

    return {
        "browser": client_browser,
        "ip": client_ip,
        "server_time": current_time,
    }


@app.route("/source_code")
def source_code():
    with open(__file__, "r") as f:
        code = f.read()

    return f"<pre>{code}</pre>"


@app.route("/random")
def random_string():
    try:
        length = int(request.args.get("length", 8))
        specials = int(request.args.get("special", 0))
        digits = int(request.args.get("digits", 0))

        if length < 1 or length > 100:
            return {
                "error": "Length must be between 1 and 100",
            }, 400
        if specials not in (0, 1) or digits not in (0, 1):
            return {"error": "Specials and Digits must be 0 or 1"}, 400

        characters = string.ascii_letters
        if digits:
            characters += string.digits
        if specials:
            characters += '!"№;%:?*()_+'

        result = "".join(random.choices(characters, k=length))

        return {"random_string": result}

    except ValueError:
        return {"error": "Invalid input"}, 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
