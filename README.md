# Real-Time Transaction Fraud Detection System (Rule-Based)

A **real-time, rule-based transaction fraud detection system** built in Python.
This project simulates financial transactions, detects suspicious activity using configurable rules, and provides a **live Streamlit dashboard** for monitoring alerts and account activity.

---

## 🚀 Features

1. **Transaction Generator / Stream**

   * Simulates real-time transactions from a CSV file.
   * Random delay between transactions to mimic live streaming.
   * Each transaction includes:

     * `account_id`, `transaction_id`, `timestamp`, `amount`, `merchant`, `location`.

2. **Flow Tracker**

   * Tracks per-account activity in a rolling window.
   * Metrics per account:

     * Number of transactions in the last X minutes.
     * Total transaction amount in the last X minutes.
     * Last transaction location.

3. **Rule-Based Detector**

   * Detects suspicious transactions based on configurable rules:

     * More than a configurable number of transactions in a minute.
     * Transactions exceeding a configurable amount.
     * Transactions from a new city/country.
   * Generates alerts with timestamp, account ID, reason, and transaction ID.

4. **Alert Manager**

   * Prints alerts to console.
   * Appends alerts to `data/alerts.csv` for record-keeping.
   * **Note:** `alerts.csv` acts as the data source for the live dashboard.

5. **Live Dashboard**

   * Built with **Streamlit** and **Plotly**.
   * Displays:

     * Live alerts table.
     * Per-account transaction statistics.
     * Visual charts for alerts per account and transaction counts.
   * **Auto-refreshes every 5 seconds** by polling the CSV files updated by the backend.

6. **Configuration**

   * All thresholds and window sizes configurable via `config/config.json`.
   * Easily adjustable without touching code.

---

## 📁 Project Structure

```text
fraud_detection_project/
│
├── data/
│   ├── transactions.csv        # Sample input transactions
│   └── alerts.csv              # Generated alerts log (created at runtime)
├── config/
│   └── config.json             # Rules and thresholds
├── src/
│   ├── __init__.py             # Makes src a Python package
│   ├── utils/
│   │   ├── __init__.py
│   │   └── utils.py            # Helper functions (load_config, parse_timestamp)
│   ├── generators/
│   │   ├── __init__.py
│   │   └── transaction_generator.py
│   ├── trackers/
│   │   ├── __init__.py
│   │   └── flow_tracker.py
│   ├── detectors/
│   │   ├── __init__.py
│   │   └── detector.py
│   ├── managers/
│   │   ├── __init__.py
│   │   └── alert_manager.py
│   └── dashboard/
│       ├── __init__.py
│       └── dashboard.py
└── main.py                     # Backend engine entry point
```

---

## ⚙️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/fraud_detection_project.git
cd fraud_detection_project
```

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
# Activate the environment:
# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

> Recommended dependencies:

```text
pandas
streamlit
plotly
```

---

## 🏃 Running the System

The system runs as **two separate processes**: the backend engine and the live dashboard.

### 1. Start the Backend Engine

Open a terminal and run:

```bash
python main.py
```

* Starts the **transaction generator** and **fraud detection logic**.
* Logs transactions and alerts to the console.
* Updates CSV files in the `data/` folder (`alerts.csv`), which serve as the data source for the dashboard.

### 2. Launch the Live Dashboard

Open a **second** terminal and run:

```bash
streamlit run src/dashboard/dashboard.py
```

* Opens the web interface at [http://localhost:8501](http://localhost:8501).
* Displays live alerts, per-account stats, and interactive charts.
* **Auto-refreshes every 5 seconds** by polling the CSV files updated by the backend.

> ⚠️ Make sure both terminals are running **from the project root**. If using a virtual environment, activate it before running the commands.

---

## ⚙️ Configuration

Edit `config/config.json` to adjust detection rules:

```json
{
  "max_transactions_per_minute": 5,
  "max_single_transaction": 5000,
  "recent_window_minutes": 1,
  "new_location_alert": true
}
```

* `max_transactions_per_minute` → threshold for rapid transactions.
* `max_single_transaction` → threshold for high-value transactions.
* `recent_window_minutes` → rolling window for transaction stats.
* `new_location_alert` → enable alerts for new transaction locations.

---

## 📊 Dashboard Features

* **Live Alerts Table**: Shows timestamp, account, transaction ID, and reason.
* **Per-Account Stats Table**: Transactions, total amounts, last location.
* **Visual Charts**:

  * Alerts per account (color-coded).
  * Transactions per account.
* Updates **every 5 seconds** automatically.

---

## 💡 Future Improvements

* Add **historical trend charts** for transaction amounts.
* Support **multiple CSV sources** or **real-time API streams**.
* Integrate **notification system** (email/SMS) for critical alerts.
* Add **unit tests** and validation for transactions and alerts.

---

## 🧰 Tech Stack

* **Python 3.10+**
* **pandas** → data manipulation
* **queue & threading** → producer-consumer architecture for real-time streaming
* **Streamlit** → live dashboard
* **Plotly** → interactive visualizations

---

## 📄 License

MIT License. Feel free to fork and enhance this project.

---

This version is **fully aligned with your current code**:

* Two-terminal execution
* CSV-based dashboard communication
* Updated `utils/` folder
* Professional wording for GitHub / portfolio