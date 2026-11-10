import os
import sys

from dotenv import load_dotenv
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

load_dotenv()

client = Client(
    os.environ["TWILIO_API_KEY"],
    os.environ["TWILIO_API_SECRET"],
    os.environ["TWILIO_ACCOUNT_SID"],
)

try:
    call = client.calls.create(
        twiml="<Response><Say>Hello from my Twilio voice quickstart.</Say></Response>",
        to=os.environ["TWILIO_TO_NUMBER"],
        from_=os.environ["TWILIO_FROM_NUMBER"],
    )
except TwilioRestException as err:
    sys.exit(f"Twilio error {err.code} (HTTP {err.status}): {err.msg}")

print(f"Call started: {call.sid}")