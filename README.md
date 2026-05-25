# CryptoTax-DE

FIFO gain calculator + German-language PDF report for annual Steuererklärung (§23 EStG).
Imports Binance and Bybit CSV files, applies strict FIFO per asset matching, and exempts crypto held for >365 days from taxes.

## Installation

1. Ensure you have Python 3.11+ installed.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

The application is built with Streamlit. To start the app, run:

```bash
streamlit run app.py
```

Then navigate to the URL provided in the terminal (usually `http://localhost:8501`).

## Running Tests

The project uses `pytest` for unit testing. To run the test suite:

```bash
python3 -m pytest tests/
```

## Environment Variables / Mock Flags

Currently, this MVP does not require any external API keys or environment variables. All operations are local and based on CSV uploads.

* **MOCK_DATA**: (Not implemented) - In future versions, setting `MOCK_DATA=true` could load pre-configured sample data without requiring a CSV upload.
