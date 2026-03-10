import json
from datetime import datetime
from pathlib import Path


def load_config(path: str = "config/config.json") -> dict:
    """
    Load configuration from a JSON file and validate required keys.
    Raises FileNotFoundError if config file doesn't exist.
    Raises KeyError if required keys are missing.
    """
    config_path = Path(path)
    if not config_path.is_file():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(config_path, "r") as f:
        config = json.load(f)

    # Validate required keys
    required_keys = [
        "max_transactions_per_minute",
        "max_single_transaction",
        "recent_window_minutes",
        "new_location_alert"
    ]
    for key in required_keys:
        if key not in config:
            raise KeyError(f"Missing required config key: {key}")

    return config


def parse_timestamp(ts_str: str) -> datetime:
    """
    Parse timestamp string into a datetime object.
    Expected format: YYYY-MM-DD HH:MM:SS
    """
    try:
        return datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        raise ValueError(f"Invalid timestamp format: {ts_str}") from e


def format_alert_for_console(alert: dict) -> str:
    """
    Format an alert dictionary into a console-friendly string.
    """
    return f"[ALERT] {alert['timestamp']} | {alert['account_id']} | {alert['reason']}"