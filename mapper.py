"""Step 2: map the Ramp transaction onto a GL account.

Ramp stores coding as accounting field selections. Here we translate
Dwight's fire-drill spend into the Office Expenses account.
"""

from copy import deepcopy

from ramp.fixtures import CHART_OF_ACCOUNTS

CATEGORY_TO_GL = {
    "office supplies": "6100",
    "office expenses": "6100",
    "safety supplies": "6100",
    "travel": "6200",
    "meals": "6300",
}

VALID_GL_CODES = {account["code"] for account in CHART_OF_ACCOUNTS}


class MappingError(ValueError):
    pass


def _amount_dollars(transaction: dict) -> float:
    cents = transaction["entity_amount"]["amount"]
    rate = transaction["minor_unit_conversion_rate"]
    return cents / rate


def map_to_gl(transaction: dict) -> dict:
    """Code the transaction as a valid Office Expenses GL entry."""
    category = (transaction.get("sk_category_name") or "").strip().lower()
    gl_code = CATEGORY_TO_GL.get(category)
    if gl_code is None:
        raise MappingError(f"No GL mapping for category: {category!r}")
    if gl_code not in VALID_GL_CODES:
        raise MappingError(f"GL account {gl_code} is not in the chart of accounts")

    gl_account = next(account for account in CHART_OF_ACCOUNTS if account["code"] == gl_code)
    liability = next(
        account for account in CHART_OF_ACCOUNTS if account["classification"] == "LIABILITY"
    )
    holder = transaction["card_holder"]
    amount = _amount_dollars(transaction)

    coded = deepcopy(transaction)
    coded["accounting_field_selections"] = [
        {
            "ramp_field_name": "GL Account",
            "remote_code": gl_account["code"],
            "remote_name": gl_account["name"],
        }
    ]
    coded["gl_translation"] = {
        "source_memo": transaction["memo"],
        "source_category": transaction["sk_category_name"],
        "translated_to": gl_account["name"],
        "is_valid": gl_account["classification"] == "EXPENSE",
        "employee": f"{holder['first_name']} {holder['last_name']}",
        "department": holder["department"],
        "entity": "Dunder Mifflin",
        "amount": amount,
        "currency": transaction["entity_amount"]["currency_code"],
        "debit_account": gl_account,
        "credit_account": liability,
    }
    return coded
