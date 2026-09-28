import logging

import requests
from flask import current_app


logger = logging.getLogger(__name__)


def send_note_webhook(note):
    webhook_url = current_app.config.get("WEBHOOK_URL")

    if not webhook_url:
        logger.warning("WEBHOOK_URL is not configured.")
        return False

    payload = {
        "event": "note_created",
        "note": {
            "id": note.id,
            "name": note.name,
            "message": note.message,
            "category": note.category.name,
        },
    }

    try:
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=5,
        )

        response.raise_for_status()

        logger.info("Note creation webhook sent successfully.")
        return True

    except requests.RequestException as error:
        logger.error("Webhook request failed: %s", error)
        return False