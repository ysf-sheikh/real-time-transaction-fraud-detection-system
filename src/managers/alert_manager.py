import csv
from pathlib import Path
from typing import List, Dict

from src.utils.utils import format_alert_for_console


class AlertManager:
    """
    Handles fraud alerts: printing, storing in memory, and writing to CSV.
    """

    def __init__(self, csv_path: str = "data/alerts.csv"):
        self.alerts_history: List[Dict] = []
        self.csv_path = Path(csv_path)
        self._init_csv()

    def _init_csv(self) -> None:
        """
        Create alerts CSV file with header if it doesn't exist.
        """
        if not self.csv_path.exists():
            self.csv_path.parent.mkdir(parents=True, exist_ok=True)
            with self.csv_path.open(mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "account_id", "transaction_id", "reason"])

    def handle_alert(self, alert: Dict) -> None:
        """
        Print alert, store in memory, and append to CSV.
        """
        # Print to console
        print(format_alert_for_console(alert))

        # Store in memory for dashboard
        self.alerts_history.append(alert)

        # Append to CSV
        with self.csv_path.open(mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                alert["timestamp"],
                alert["account_id"],
                alert.get("transaction_id", ""),
                alert["reason"],
            ])

    def get_alerts(self) -> List[Dict]:
        """
        Return all alerts stored in memory.
        """
        return self.alerts_history.copy()