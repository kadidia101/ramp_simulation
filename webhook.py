"""Step 1: extract the Ramp webhook envelope, then load the transaction."""

from copy import deepcopy

from ramp.fixtures import TRANSACTIONS, WEBHOOK_EVENT


class WebhookError(ValueError):
    pass


def extract_webhook_payload(event: dict | None = None) -> dict:
    """Return the base Ramp webhook fields used to look up the transaction."""
    payload = deepcopy(event or WEBHOOK_EVENT)
    required = ("id", "type", "created_at", "business_id", "object")
    missing = [field for field in required if field not in payload]
    if missing:
        raise WebhookError(f"Webhook payload missing fields: {missing}")

    object_id = payload.get("object", {}).get("id")
    if not object_id:
        raise WebhookError("Webhook object.id is required")

    if payload["type"] != "transactions.cleared":
        raise WebhookError(f"Unsupported webhook type: {payload['type']}")

    return {
        "event_id": payload["id"],
        "event_type": payload["type"],
        "created_at": payload["created_at"],
        "business_id": payload["business_id"],
        "transaction_id": object_id,
    }


def fetch_transaction(transaction_id: str) -> dict:
    """Stand-in for GET /developer/v1/transactions/{transaction_id}."""
    transaction = TRANSACTIONS.get(transaction_id)
    if transaction is None:
        raise WebhookError(f"Unknown transaction: {transaction_id}")
    return deepcopy(transaction)
