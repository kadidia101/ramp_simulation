"""Simulated Ramp data for Dunder Mifflin.

Ramp webhooks only send an event envelope with a resource id.
The full card transaction is fetched afterward from GET /transactions/{id}.
"""

WEBHOOK_EVENT = {
    "id": "evt_dwight_fire_drill_001",
    "type": "transactions.cleared",
    "created_at": "2026-10-19T14:32:00Z",
    "business_id": "biz_dunder_mifflin_scranton",
    "object": {
        "id": "txn_dwight_fake_fire_drill",
    },
}

TRANSACTIONS = {
    "txn_dwight_fake_fire_drill": {
        "id": "txn_dwight_fake_fire_drill",
        "state": "CLEARED",
        "sync_status": "SYNC_READY",
        "user_transaction_time": "2026-10-19T13:05:00Z",
        "accounting_date": "2026-10-19",
        "memo": "Fake fire drill expenses",
        "merchant_name": "Schrute Safety Supply",
        "merchant_descriptor": "SCHRUTE SAFETY SUPPLY",
        "merchant_category_code": "5085",
        "sk_category_name": "Office supplies",
        "entity_id": "ent_dunder_mifflin",
        "entity_amount": {
            "amount": 24783,
            "currency_code": "USD",
        },
        "minor_unit_conversion_rate": 100,
        "card_holder": {
            "first_name": "Dwight",
            "last_name": "Schrute",
            "department": "Sales",
            "location": "Scranton",
        },
        "line_items": [
            {
                "id": "li_fire_alarm",
                "memo": "Industrial alarm horns for surprise drill",
                "amount": 24783,
            }
        ],
        "accounting_field_selections": [],
    }
}

CHART_OF_ACCOUNTS = [
    {
        "code": "1000",
        "name": "Ramp Card Liability",
        "classification": "LIABILITY",
    },
    {
        "code": "6100",
        "name": "Office Expenses",
        "classification": "EXPENSE",
    },
    {
        "code": "6200",
        "name": "Travel",
        "classification": "EXPENSE",
    },
    {
        "code": "6300",
        "name": "Meals & Entertainment",
        "classification": "EXPENSE",
    },
]
