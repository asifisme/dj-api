import json
from typing import Dict, Any


class PaymentProcessor:
    def __init__(self, data: Dict[str, Any], sep: str = '.'):
        self.sep = sep
        self.flat_data = self._flatten(data)
        self.payment_data = self._build_payment_dict()

    def _flatten(self, d: Dict[str, Any], parent_key: str = '') -> Dict[str, Any]:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{self.sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten(v, new_key).items())
            elif isinstance(v, list):
                for idx, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(self._flatten(item, f"{new_key}[{idx}]").items())
                    else:
                        items.append((f"{new_key}[{idx}]", item))
            else:
                items.append((new_key, v))
        return dict(items)

    def _build_payment_dict(self) -> Dict[str, Any]:
        try:
            return {
                "order_id": int(self.flat_data.get("metadata.order_id", 0)),
                "user_id": int(self.flat_data.get("metadata.user_id", 0)),
                "amount_paid": int(self.flat_data.get("amount_total", 0)),
                "currency": self.flat_data.get("currency", "usd"),
                "stripe_checkout_id": self.flat_data.get("id"),
                "stripe_payment_intent": self.flat_data.get("payment_intent"),
                "stripe_payment_status": self.flat_data.get("payment_status"),
                "payment_method": self.flat_data.get("payment_method_types[0]", "unknown"),
                "receipt_url": self.flat_data.get("receipt_url", None),
                "customer_email": self.flat_data.get("customer_details.email", None),
                "customer_name": self.flat_data.get("customer_details.name", None)
            }
        except Exception as e:
            print(f"Error processing payment data: {e}")
            return {}

    def get_payment_data(self) -> Dict[str, Any]:
        return self.payment_data

    def __str__(self) -> str:
        return json.dumps(self.payment_data, indent=2)

