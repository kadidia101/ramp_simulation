"""Step 3: post the coded transaction into a mock ERP and return the result."""

from datetime import datetime, timezone
from uuid import uuid4

LEDGER: list[dict] = []


def reset_ledger() -> None:
    LEDGER.clear()


def post_journal_entry(coded_transaction: dict) -> dict:
    """Create a double-entry journal in the ERP (debit expense, credit Ramp card)."""
    translation = coded_transaction["gl_translation"]
    if not translation["is_valid"]:
        raise ValueError("Refusing to post an invalid GL mapping")

    amount = translation["amount"]
    debit = translation["debit_account"]
    credit = translation["credit_account"]
    posted_at = datetime.now(timezone.utc).isoformat()

    journal = {
        "erp": "Dunder Mifflin ERP",
        "journal_id": f"JE-{uuid4().hex[:8].upper()}",
        "status": "POSTED",
        "posted_at": posted_at,
        "company": "Dunder Mifflin Paper Company, Inc.",
        "subsidiary": "Scranton Branch",
        "source": "Ramp",
        "ramp_transaction_id": coded_transaction["id"],
        "memo": (
            f"{translation['employee']} — {translation['translated_to']}: "
            f"{translation['source_memo']}"
        ),
        "lines": [
            {
                "line_number": 1,
                "account_code": debit["code"],
                "account_name": debit["name"],
                "debit": amount,
                "credit": 0.0,
                "department": translation["department"],
            },
            {
                "line_number": 2,
                "account_code": credit["code"],
                "account_name": credit["name"],
                "debit": 0.0,
                "credit": amount,
                "department": translation["department"],
            },
        ],
        "totals": {
            "debit": amount,
            "credit": amount,
            "balanced": True,
        },
    }
    LEDGER.append(journal)
    return journal
