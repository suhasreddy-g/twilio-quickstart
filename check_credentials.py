"""Check whether your Twilio credentials still work.

Makes one read-only call (fetch the account) and never prints secrets.
Works with an API key + secret, or falls back to the Auth Token.
"""
import os
import sys

from dotenv import load_dotenv
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

load_dotenv()

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
api_key = os.environ.get("TWILIO_API_KEY")
api_secret = os.environ.get("TWILIO_API_SECRET")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

if not account_sid:
    sys.exit("TWILIO_ACCOUNT_SID is not set.")

if api_key and api_secret:
    client = Client(api_key, api_secret, account_sid)
    mode = "API key"
elif auth_token:
    client = Client(account_sid, auth_token)
    mode = "Auth Token"
else:
    sys.exit("Set TWILIO_API_KEY and TWILIO_API_SECRET (or TWILIO_AUTH_TOKEN).")

try:
    account = client.api.accounts(account_sid).fetch()
except TwilioRestException as err:
    sys.exit(f"Credentials rejected ({mode}): error {err.code}, HTTP {err.status}")

print(f"OK ({mode}). Account: {account.friendly_name}, status: {account.status}, type: {account.type}")
