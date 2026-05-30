from typing import List, Dict, Optional


def check_rules(
    txn: Dict,
    account_stats_before_txn: Optional[Dict] = None,
    config: Dict = None
) -> List[Dict]:
    """
    Rule-based fraud detection engine for a single transaction.

    Evaluates a transaction against predefined heuristics and returns
    a list of alerts if any rules are violated.

    This function is designed to be stateless and works using:
        - The current transaction
        - Snapshot of account state BEFORE the transaction
        - Configuration-defined thresholds

    Args:
        txn (Dict):
            Transaction record containing:
                - account_id
                - transaction_id
                - timestamp
                - amount
                - location

        account_stats_before_txn (Optional[Dict]):
            Snapshot of account activity BEFORE this transaction was applied.
            Used for detecting anomalies such as frequency spikes or location changes.

        config (Dict):
            Rule configuration dictionary containing thresholds such as:
                - max_transactions_per_minute
                - max_single_transaction
                - new_location_alert

    Returns:
        List[Dict]:
            A list of triggered alert objects. Each alert contains:
                - timestamp
                - account_id
                - transaction_id
                - reason
    """

    if config is None:
        config = {}

    alerts = []

    # Load rule thresholds with safe defaults
    max_txn_per_min = config.get("max_transactions_per_minute", 5)
    max_single_txn = config.get("max_single_transaction", 5000)
    new_location_alert = config.get("new_location_alert", True)

    # Extract prior account state (if available)
    txn_count = account_stats_before_txn.get("transaction_count", 0) if account_stats_before_txn else 0
    last_location = account_stats_before_txn.get("last_location") if account_stats_before_txn else None

    # Rule 1: Detect high transaction frequency within time window
    if txn_count + 1 > max_txn_per_min:
        alerts.append({
            "timestamp": txn["timestamp"],
            "account_id": txn["account_id"],
            "transaction_id": txn["transaction_id"],
            "reason": "High transaction frequency",
        })

    # Rule 2: Detect unusually large transaction amounts
    if float(txn["amount"]) > max_single_txn:
        alerts.append({
            "timestamp": txn["timestamp"],
            "account_id": txn["account_id"],
            "transaction_id": txn["transaction_id"],
            "reason": "High transaction amount",
        })

    # Rule 3: Detect location anomaly for account
    if new_location_alert:
        if last_location and last_location != txn["location"]:
            alerts.append({
                "timestamp": txn["timestamp"],
                "account_id": txn["account_id"],
                "transaction_id": txn["transaction_id"],
                "reason": "New location for account",
            })

    return alerts
