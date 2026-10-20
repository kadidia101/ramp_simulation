"""Ramp-style spend sync: webhook → GL mapping → ERP journal."""

from ramp.erp import post_journal_entry
from ramp.mapper import map_to_gl
from ramp.webhook import extract_webhook_payload, fetch_transaction


def sync_transaction(webhook_event: dict | None = None) -> dict:
    envelope = extract_webhook_payload(webhook_event)
    transaction = fetch_transaction(envelope["transaction_id"])
    coded = map_to_gl(transaction)
    erp_result = post_journal_entry(coded)
    return {
        "webhook": envelope,
        "transaction": transaction,
        "gl_mapping": coded["gl_translation"],
        "erp": erp_result,
    }
