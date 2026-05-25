from datetime import datetime
from collections import deque
from typing import List, Dict

def is_tax_free(buy_date: str, sell_date: str) -> bool:
    """
    Returns True if holding period is > 365 days.
    """
    b_date = datetime.strptime(buy_date[:10], "%Y-%m-%d")
    s_date = datetime.strptime(sell_date[:10], "%Y-%m-%d")
    delta = s_date - b_date
    return delta.days > 365

def calculate_gains(trades: list[dict]) -> list[dict]:
    """
    Strict FIFO per asset. Match SELL against oldest BUY lots. Handle partial lot consumption.
    Returns a list of TaxEvent dicts.
    """
    inventory: Dict[str, deque] = {}
    tax_events = []

    for trade in trades:
        asset = trade['asset']
        if asset not in inventory:
            inventory[asset] = deque()

        if trade['type'] == 'BUY':
            inventory[asset].append({
                'date': trade['date'],
                'amount': trade['amount'],
                'price_eur': trade['price_eur']
            })
        elif trade['type'] == 'SELL':
            sell_amount = trade['amount']
            sell_price_eur = trade['price_eur']
            sell_date = trade['date']

            while sell_amount > 0 and inventory[asset]:
                buy_lot = inventory[asset][0]

                amount_to_consume = min(sell_amount, buy_lot['amount'])

                buy_date = buy_lot['date']
                buy_price_eur = buy_lot['price_eur']

                gain_eur = (sell_price_eur - buy_price_eur) * amount_to_consume
                holding_days = (datetime.strptime(sell_date[:10], "%Y-%m-%d") - datetime.strptime(buy_date[:10], "%Y-%m-%d")).days
                taxable = not is_tax_free(buy_date, sell_date)

                tax_events.append({
                    'sell_date': sell_date,
                    'asset': asset,
                    'amount': amount_to_consume,
                    'buy_price_eur': buy_price_eur,
                    'sell_price_eur': sell_price_eur,
                    'gain_eur': gain_eur,
                    'holding_days': holding_days,
                    'taxable': taxable
                })

                buy_lot['amount'] -= amount_to_consume
                sell_amount -= amount_to_consume

                if buy_lot['amount'] <= 0:
                    inventory[asset].popleft()

            # Note: if sell_amount > 0 after consuming inventory, it means selling more than we have (shorting or missing data).
            # For this MVP, we ignore missing cost basis.

    return tax_events
