import threading
from queue import Queue
from pathlib import Path
import time

from src.utils import load_config
from src.generators.transaction_generator import start_transaction_stream
from src.trackers.flow_tracker import FlowTracker
from src.detectors.detector import check_rules
from src.managers.alert_manager import AlertManager

def transaction_processor(txn_queue: Queue, flow_tracker: FlowTracker, alert_manager: AlertManager, config: dict):
    print("[MAIN] Starting transaction processing loop...")
    while True:
        txn = txn_queue.get()
        try:
            if not isinstance(txn, dict): continue

            account_id = txn["account_id"]
            stats_before_txn = flow_tracker.get_account_stats(account_id)
            
            # Update flow tracker
            flow_tracker.update_account_flow(txn)

            # Run detector
            alerts = check_rules(txn, account_stats_before_txn=stats_before_txn, config=config)

            # Handle alerts (Writes to CSV)
            for alert in alerts:
                alert_manager.handle_alert(alert)

        except Exception as e:
            print(f"[MAIN] Error: {e}")

def main():
    print("[MAIN] Initializing Backend Engine...")
    config = load_config("config/config.json")

    txn_queue = Queue(maxsize=1000)
    flow_tracker = FlowTracker(recent_window_minutes=config.get("recent_window_minutes", 1))
    alert_manager = AlertManager(csv_path="data/alerts.csv")

    # Thread 1: Generator
    threading.Thread(target=start_transaction_stream, args=(txn_queue, "data/transactions.csv"), daemon=True).start()

    # Thread 2: Processor
    processor_thread = threading.Thread(target=transaction_processor, args=(txn_queue, flow_tracker, alert_manager, config), daemon=True)
    processor_thread.start()

    print("[MAIN] Engine running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[MAIN] Shutting down...")

if __name__ == "__main__":
    main()