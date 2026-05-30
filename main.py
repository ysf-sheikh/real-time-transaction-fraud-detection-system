import threading
from queue import Queue
from pathlib import Path
import time

from src.utils import load_config
from src.generators.transaction_generator import start_transaction_stream
from src.trackers.flow_tracker import FlowTracker
from src.detectors.detector import check_rules
from src.managers.alert_manager import AlertManager


def transaction_processor(
    txn_queue: Queue,
    flow_tracker: FlowTracker,
    alert_manager: AlertManager,
    config: dict,
):
    """
    Worker thread responsible for processing incoming transactions.

    Processing pipeline:
        1. Fetch transaction from queue
        2. Retrieve pre-transaction account state
        3. Update account flow statistics
        4. Run fraud/rule detection engine
        5. Forward alerts to alert manager for persistence

    Runs continuously in a daemon thread.
    """
    print("[MAIN] Starting transaction processing loop...")

    while True:
        txn = txn_queue.get()
        try:
            # Ignore malformed messages
            if not isinstance(txn, dict):
                continue

            account_id = txn["account_id"]

            # Snapshot state before applying transaction update
            stats_before_txn = flow_tracker.get_account_stats(account_id)

            # Update internal account flow tracking
            flow_tracker.update_account_flow(txn)

            # Run detection rules using pre/post transaction context
            alerts = check_rules(
                txn,
                account_stats_before_txn=stats_before_txn,
                config=config,
            )

            # Handle and persist generated alerts
            for alert in alerts:
                alert_manager.handle_alert(alert)

        except Exception as e:
            print(f"[MAIN] Error: {e}")


def main():
    """
    Entry point for the transaction monitoring engine.

    Responsibilities:
        - Load configuration
        - Initialize queues and core components
        - Start transaction generator thread
        - Start processing worker thread
        - Keep main thread alive until interrupted
    """
    print("[MAIN] Initializing Backend Engine...")

    # Load system configuration
    config = load_config("config/config.json")

    # Shared queue between generator and processor
    txn_queue = Queue(maxsize=1000)

    # Core system components
    flow_tracker = FlowTracker(
        recent_window_minutes=config.get("recent_window_minutes", 1)
    )
    alert_manager = AlertManager(csv_path="data/alerts.csv")

    # Thread 1: Transaction stream generator (simulated ingestion pipeline)
    threading.Thread(
        target=start_transaction_stream,
        args=(txn_queue, "data/transactions.csv"),
        daemon=True,
    ).start()

    # Thread 2: Transaction processing engine
    processor_thread = threading.Thread(
        target=transaction_processor,
        args=(txn_queue, flow_tracker, alert_manager, config),
        daemon=True,
    )
    processor_thread.start()

    print("[MAIN] Engine running. Press Ctrl+C to stop.")

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[MAIN] Shutting down...")


if __name__ == "__main__":
    main()
