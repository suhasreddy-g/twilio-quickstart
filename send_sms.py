"""Twilio Messaging quickstart: send one SMS.

Reads credentials from environment variables (or a local .env file).
Based on https://www.twilio.com/docs/messaging/quickstart
"""
import os
import sys

from dotenv import load_dotenv
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

load_dotenv()


def require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        sys.exit(f"Missing {name}. Copy .env.example to .env and fill it in.")
    return value


def main() -> None:
    account_sid = require("TWILIO_ACCOUNT_SID")
    api_key = require("TWILIO_API_KEY")
    api_secret = require("TWILIO_API_SECRET")
    from_number = require("TWILIO_FROM_NUMBER")  # your Twilio number, E.164
    to_number = require("TWILIO_TO_NUMBER")      # verified recipient, E.164

    client = Client(api_key, api_secret, account_sid)

    try:
        message = client.messages.create(
            body="Hello from my Twilio quickstart.",
            from_=from_number,
            to=to_number,
        )
    except TwilioRestException as err:
        sys.exit(f"Twilio error {err.code} (HTTP {err.status}): {err.msg}")

    print(f"Queued message {message.sid}, status: {message.status}")


if __name__ == "__main__":
    main()
