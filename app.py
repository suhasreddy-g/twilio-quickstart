from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse

load_dotenv()
app = Flask(__name__)


@app.route("/sms", methods=["POST"])
def sms_reply():
    body = request.form.get("Body", "").strip()
    resp = MessagingResponse()
    if body.lower() == "hi":
        resp.message("Hello! Thanks for texting.")
    else:
        resp.message(f"You said: {body}")
    return str(resp), 200, {"Content-Type": "application/xml"}


@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    resp.say("Thanks for calling. This is my Twilio learning project.")
    return str(resp), 200, {"Content-Type": "application/xml"}


if __name__ == "__main__":
    app.run(port=5001, debug=True)