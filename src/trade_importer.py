import pandas as pd

def parse_trades(file_obj) -> list[dict]:
    """
    Parses a CSV file containing trades.
    Normalizes trades into a list of dicts:
    {date: str (YYYY-MM-DD), type: str (BUY/SELL), asset: str, amount: float, price_eur: float, fee_eur: float}
    """
    df = pd.read_csv(file_obj)

    normalized_trades = []

    # Simple check for Binance-like columns vs Bybit-like columns
    if 'Market' in df.columns and 'Type' in df.columns:
        # Assume Binance format
        for _, row in df.iterrows():
            market = str(row['Market'])
            if market.endswith('EUR'):
                asset = market[:-3]
            else:
                continue # Only handling EUR pairs for simplicity in this MVP

            trade_type = str(row['Type']).upper()

            normalized_trades.append({
                'date': str(row['Date'])[:10], # Extract YYYY-MM-DD
                'type': trade_type,
                'asset': asset,
                'amount': float(row['Amount']),
                'price_eur': float(row['Price']),
                'fee_eur': float(row['Fee']) if 'Fee' in df.columns and pd.notna(row['Fee']) else 0.0
            })
    else:
        # Assume simple generic format if it has expected columns directly
        # E.g. date, type, asset, amount, price_eur, fee_eur
        for _, row in df.iterrows():
            if all(col in df.columns for col in ['date', 'type', 'asset', 'amount', 'price_eur']):
                normalized_trades.append({
                    'date': str(row['date'])[:10],
                    'type': str(row['type']).upper(),
                    'asset': str(row['asset']),
                    'amount': float(row['amount']),
                    'price_eur': float(row['price_eur']),
                    'fee_eur': float(row['fee_eur']) if 'fee_eur' in df.columns and pd.notna(row['fee_eur']) else 0.0
                })

    # Sort trades chronologically
    normalized_trades.sort(key=lambda x: x['date'])
    return normalized_trades
