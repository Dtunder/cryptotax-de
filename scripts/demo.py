import os
import sys

# Ensure src module is reachable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.trade_importer import parse_trades
from src.tax_calculator import calculate_gains

def run_demo():
    print("=== CryptoTax-DE Demo Pipeline ===")

    file_path = "data/sample_trades.csv"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    print(f"Loading trades from {file_path}...")
    trades = parse_trades(file_path)
    print(f"Successfully loaded {len(trades)} trades.")

    print("Calculating taxable gains (FIFO)...")
    tax_events = calculate_gains(trades)

    total_gain = sum(e['gain_eur'] for e in tax_events)
    total_taxable = sum(e['gain_eur'] for e in tax_events if e['taxable'])
    total_tax_free = sum(e['gain_eur'] for e in tax_events if not e['taxable'])

    print("\n--- Summary ---")
    print(f"Total Gain:       {total_gain:.2f} EUR")
    print(f"Taxable Gain:     {total_taxable:.2f} EUR")
    print(f"Tax-free Gain:    {total_tax_free:.2f} EUR")

    tax_events_count = len([e for e in tax_events if e['taxable']])
    tax_free_events_count = len([e for e in tax_events if not e['taxable']])

    print(f"\nEvents Breakdown:")
    print(f"- Taxable events (>0 days, <=365 days): {tax_events_count}")
    print(f"- Tax-free events (>365 days):         {tax_free_events_count}")
    print("==================================")

if __name__ == "__main__":
    run_demo()
