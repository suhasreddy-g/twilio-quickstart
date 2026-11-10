import os
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, abort, request
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse

load_dotenv()
app = Flask(__name__)


def twilio_signed(view):
    """Reject requests that Twilio did not sign.

    Off by default so local curl tests work. Set VALIDATE_TWILIO=true,
    TWILIO_AUTH_TOKEN and PUBLIC_BASE_URL in production.
    """

    @wraps(view)
    def wrapper(*args, **kwargs):
        if os.environ.get("VALIDATE_TWILIO", "false").lower() != "true":
            return view(*args, **kwargs)

        token = os.environ.get("TWILIO_AUTH_TOKEN")
        base_url = os.environ.get("PUBLIC_BASE_URL", "").rstrip("/")
        if not token or not base_url:
            abort(500)

        url = base_url + request.path
        if request.query_string:
            url += "?" + request.query_string.decode()

        signature = request.headers.get("X-Twilio-Signature", "")
        if not RequestValidator(token).validate(url, request.form, signature):
            abort(403)
        return view(*args, **kwargs)

    return wrapper


@app.route("/sms", methods=["POST"])
@twilio_signed
def sms_reply():
    body = request.form.get("Body", "").strip()
    resp = MessagingResponse()
    if body.lower() == "hi":
        resp.message("Hello! Thanks for texting.")
    else:
        resp.message(f"You said: {body}")
    return str(resp), 200, {"Content-Type": "application/xml"}


@app.route("/voice", methods=["POST"])
@twilio_signed
def voice():
    resp = VoiceResponse()
    resp.say("Thanks for calling. This is my Twilio learning project.")
    return str(resp), 200, {"Content-Type": "application/xml"}


if __name__ == "__main__":
    app.run(port=5001, debug=True)