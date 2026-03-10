from typing import List, Dict, Optional


def check_rules(
    txn: Dict,
    account_stats_before_txn: Optional[Dict] = None,
    config: Dict = None
) -> List[Dict]:
    """
    Apply rule-based fraud checks to a single transaction.
    Returns a list of alerts (can be multiple reasons for same txn).

    Args:
        txn (Dict): Transaction dictionary with keys:
            - account_id
            - transaction_id
            - timestamp
            - amount
            - location
        account_stats_before_txn (Dict): Stats BEFORE adding this transaction
            (needed for correct 'new location' detection)
        config (Dict): Configuration dictionary with thresholds.

    Returns:
        List[Dict]: List of alert dictionaries.
    """
    if config is None:
        config = {}

    alerts = []

    max_txn_per_min = config.get("max_transactions_per_minute", 5)
    max_single_txn = config.get("max_single_transaction", 5000)
    new_location_alert = config.get("new_location_alert", True)

    txn_count = account_stats_before_txn.get("transaction_count", 0) if account_stats_before_txn else 0
    last_location = account_stats_before_txn.get("last_location") if account_stats_before_txn else None

    # Rule 1: too many transactions in recent window
    if txn_count + 1 > max_txn_per_min:
        alerts.append({
            "timestamp": txn["timestamp"],
            "account_id": txn["account_id"],
            "transaction_id": txn["transaction_id"],
            "reason": "High transaction frequency",
        })

    # Rule 2: single transaction too large
    if float(txn["amount"]) > max_single_txn:
        alerts.append({
            "timestamp": txn["timestamp"],
            "account_id": txn["account_id"],
            "transaction_id": txn["transaction_id"],
            "reason": "High transaction amount",
        })

    # Rule 3: new location for this account
    if new_location_alert:
        if last_location and last_location != txn["location"]:
            alerts.append({
                "timestamp": txn["timestamp"],
                "account_id": txn["account_id"],
                "transaction_id": txn["transaction_id"],
                "reason": "New location for account",
            })

    return alerts