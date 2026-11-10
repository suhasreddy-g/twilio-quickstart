# Twilio Messaging quickstart

Learning project based on https://www.twilio.com/docs/messaging/quickstart

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in your values
```

## Run

```bash
python check_credentials.py   # confirms the keys still work
python send_sms.py            # sends one SMS
```

## Notes

- Never commit `.env`. It is listed in `.gitignore`.
- Numbers must be E.164 format, for example +15558675310.
- Trial accounts can only message verified recipients. An expired trial must be upgraded before real sends work.
- Next steps: inbound replies with Flask and ngrok, then Voice.
