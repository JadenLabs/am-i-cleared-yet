import requests
from utils import Details


def notify(details: Details, user_mention: str, webhook_url: str):
    payload = {
        "content": user_mention,
        "embeds": [
            {
                "title": f"Badge {details.badge_number} Cleared!",
                "description": f"**Sponsor**: {details.sponsor}\n**Company**: {details.company}\n**Badge Number**: {details.badge_number}",
                "color": 54784,
                "footer": {"text": details.notify_date},
            }
        ],
    }

    requests.post(webhook_url, json=payload)
