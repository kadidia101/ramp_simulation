"""Run Dwight Schrute's fake fire drill expense through the Ramp simulation."""

import json

from ramp.pipeline import sync_transaction


def main() -> None:
    result = sync_transaction()

    print("1. Base webhook payload")
    print(json.dumps(result["webhook"], indent=2))

    print("\n2. Fetched Ramp transaction")
    print(json.dumps(result["transaction"], indent=2))

    print("\n3. GL mapping (translated to Office Expenses)")
    print(json.dumps(result["gl_mapping"], indent=2))

    print("\n4. ERP journal entry")
    print(json.dumps(result["erp"], indent=2))


if __name__ == "__main__":
    main()
