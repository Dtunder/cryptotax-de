from pydantic import BaseModel

class TaxEvent(BaseModel):
    sell_date: str
    asset: str
    amount: float
    buy_price_eur: float
    sell_price_eur: float
    gain_eur: float
    holding_days: int
    taxable: bool
