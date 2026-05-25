import pytest
from src.tax_calculator import calculate_gains, is_tax_free

def test_is_tax_free_true():
    assert is_tax_free("2022-01-01", "2023-01-02") == True

def test_is_tax_free_false_exact_year():
    assert is_tax_free("2022-01-01", "2023-01-01") == False

def test_is_tax_free_false_short():
    assert is_tax_free("2022-01-01", "2022-06-01") == False

def test_calculate_gains_simple_buy_sell():
    trades = [
        {'date': '2022-01-01', 'type': 'BUY', 'asset': 'BTC', 'amount': 1.0, 'price_eur': 40000.0},
        {'date': '2022-02-01', 'type': 'SELL', 'asset': 'BTC', 'amount': 1.0, 'price_eur': 50000.0}
    ]
    gains = calculate_gains(trades)
    assert len(gains) == 1
    assert gains[0]['gain_eur'] == 10000.0
    assert gains[0]['taxable'] == True

def test_calculate_gains_tax_free():
    trades = [
        {'date': '2022-01-01', 'type': 'BUY', 'asset': 'BTC', 'amount': 1.0, 'price_eur': 40000.0},
        {'date': '2023-01-02', 'type': 'SELL', 'asset': 'BTC', 'amount': 1.0, 'price_eur': 50000.0}
    ]
    gains = calculate_gains(trades)
    assert len(gains) == 1
    assert gains[0]['gain_eur'] == 10000.0
    assert gains[0]['taxable'] == False

def test_calculate_gains_partial_lot():
    trades = [
        {'date': '2022-01-01', 'type': 'BUY', 'asset': 'BTC', 'amount': 1.0, 'price_eur': 40000.0},
        {'date': '2022-02-01', 'type': 'SELL', 'asset': 'BTC', 'amount': 0.5, 'price_eur': 50000.0}
    ]
    gains = calculate_gains(trades)
    assert len(gains) == 1
    assert gains[0]['amount'] == 0.5
    assert gains[0]['gain_eur'] == 5000.0

def test_calculate_gains_multiple_lots_fifo():
    trades = [
        {'date': '2022-01-01', 'type': 'BUY', 'asset': 'BTC', 'amount': 1.0, 'price_eur': 10000.0},
        {'date': '2022-02-01', 'type': 'BUY', 'asset': 'BTC', 'amount': 1.0, 'price_eur': 20000.0},
        {'date': '2022-03-01', 'type': 'SELL', 'asset': 'BTC', 'amount': 1.5, 'price_eur': 30000.0}
    ]
    gains = calculate_gains(trades)
    assert len(gains) == 2

    # First lot: 1.0 BTC bought at 10000, sold at 30000 -> gain 20000
    assert gains[0]['amount'] == 1.0
    assert gains[0]['gain_eur'] == 20000.0

    # Second lot: 0.5 BTC bought at 20000, sold at 30000 -> gain 5000
    assert gains[1]['amount'] == 0.5
    assert gains[1]['gain_eur'] == 5000.0

def test_calculate_gains_different_assets():
    trades = [
        {'date': '2022-01-01', 'type': 'BUY', 'asset': 'BTC', 'amount': 1.0, 'price_eur': 40000.0},
        {'date': '2022-01-02', 'type': 'BUY', 'asset': 'ETH', 'amount': 10.0, 'price_eur': 2000.0},
        {'date': '2022-02-01', 'type': 'SELL', 'asset': 'ETH', 'amount': 5.0, 'price_eur': 3000.0},
        {'date': '2022-02-02', 'type': 'SELL', 'asset': 'BTC', 'amount': 1.0, 'price_eur': 50000.0}
    ]
    gains = calculate_gains(trades)
    assert len(gains) == 2

    eth_gain = next(e for e in gains if e['asset'] == 'ETH')
    assert eth_gain['amount'] == 5.0
    assert eth_gain['gain_eur'] == 5000.0

    btc_gain = next(e for e in gains if e['asset'] == 'BTC')
    assert btc_gain['amount'] == 1.0
    assert btc_gain['gain_eur'] == 10000.0
