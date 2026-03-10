from collections import deque
from datetime import timedelta, datetime
from typing import Dict, Any

from src.utils.utils import parse_timestamp


class FlowTracker:
    """
    Tracks recent transactions per account and computes stats.
    """

    def __init__(self, recent_window_minutes: int = 1):
        self.recent_window = timedelta(minutes=recent_window_minutes)
        self.account_flows: Dict[str, Dict[str, Any]] = {}

    def _get_or_create_account_flow(self, account_id: str) -> Dict[str, Any]:
        """
        Get existing flow for account or create a new one.
        """
        if account_id not in self.account_flows:
            self.account_flows[account_id] = {
                "transactions": deque(),  # each item: (timestamp_dt, amount, location)
                "total_amount": 0.0,
                "last_location": None,
            }
        return self.account_flows[account_id]

    def update_account_flow(self, txn: dict) -> dict:
        """
        Update flow tracker with a new transaction.
        Remove old transactions outside the recent window.
        Returns stats for this account.
        """
        account_id = txn["account_id"]
        txn_time = parse_timestamp(txn["timestamp"])
        amount = float(txn["amount"])
        location = txn["location"]

        flow = self._get_or_create_account_flow(account_id)

        # Add new transaction
        flow["transactions"].append((txn_time, amount, location))
        flow["total_amount"] += amount
        flow["last_location"] = location

        # Remove transactions outside the recent window
        while flow["transactions"]:
            oldest_time, oldest_amount, _ = flow["transactions"][0]
            
            if txn_time - oldest_time > self.recent_window:
                flow["transactions"].popleft()
                flow["total_amount"] -= float(oldest_amount) # Ensure float
            else:
                break

        return self._account_stats(flow, account_id)

    def get_account_stats(self, account_id: str) -> dict:
        """
        Return stats for a single account.
        """
        flow = self._get_or_create_account_flow(account_id)
        return self._account_stats(flow, account_id)

    def get_all_account_stats(self) -> Dict[str, dict]:
        """
        Return stats for all accounts.
        Useful for dashboards.
        """
        stats = {}
        for account_id, flow in self.account_flows.items():
            stats[account_id] = self._account_stats(flow, account_id)
        return stats

    @staticmethod
    def _account_stats(flow: Dict[str, Any], account_id: str) -> dict:
        return {
            "account_id": account_id,
            "transaction_count": len(flow["transactions"]),
            "total_amount": flow["total_amount"],
            "last_location": flow["last_location"],
        }