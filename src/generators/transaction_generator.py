import time
import random
from queue import Queue
from pathlib import Path

import pandas as pd


def start_transaction_stream(
    txn_queue: Queue,
    csv_path: str = "data/transactions.csv",
    min_delay: float = 0.5,
    max_delay: float = 2.0,
) -> None:
    """
    Read transactions from a CSV file and push them into the queue one by one.
    Adds a random delay between transactions to simulate real-time streaming.

    Args:
        txn_queue (Queue): Thread-safe queue to put transactions into.
        csv_path (str): Path to transactions CSV file.
        min_delay (float): Minimum delay between transactions (seconds).
        max_delay (float): Maximum delay between transactions (seconds).
    """
    csv_file = Path(csv_path)
    if not csv_file.is_file():
        raise FileNotFoundError(f"Transactions CSV not found: {csv_path}")

    print("[GENERATOR] Loading transactions from CSV...")
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        raise RuntimeError(f"Failed to read CSV: {e}") from e

    # Validate required columns
    required_cols = {"account_id", "transaction_id", "timestamp", "amount", "merchant", "location"}
    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        raise ValueError(f"transactions.csv missing required columns: {missing}")

    # Stream each transaction
    for _, row in df.iterrows():
        txn = {
            "account_id": str(row["account_id"]),
            "transaction_id": str(row["transaction_id"]),
            "timestamp": str(row["timestamp"]),
            "amount": float(row["amount"]),
            "merchant": str(row["merchant"]),
            "location": str(row["location"]),
        }

        print(f"[GENERATOR] Streaming txn {txn['transaction_id']} for {txn['account_id']}...")
        txn_queue.put(txn)

        # Random delay to simulate streaming
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

    print("[GENERATOR] Finished streaming all transactions.")