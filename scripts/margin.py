#!/usr/bin/env python3
"""Margin of one product from its price, purchase cost and the store's fixed costs.

  python3 scripts/margin.py --price 32.90 --cost 12.00 --packaging 0.70 --fulfillment 5.00 --payment-fee-pct 1.5
  python3 scripts/margin.py --price 32.90 --cost 12.00 --vat-pct 23

--price is what the customer pays. With --vat-pct the VAT is taken out of the price first,
and --cost, --packaging and --fulfillment are expected net. The payment fee is charged on
the full price paid. There is no default for --cost: an unknown cost means no margin.
"""
import argparse
from decimal import ROUND_HALF_UP, Decimal


def money(x):
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def main():
    p = argparse.ArgumentParser(description="Margin of one product.")
    p.add_argument("--price", type=Decimal, required=True, help="price paid by the customer")
    p.add_argument("--cost", type=Decimal, required=True, help="purchase cost of one unit")
    p.add_argument("--packaging", type=Decimal, default=Decimal(0), help="packaging cost per order")
    p.add_argument("--fulfillment", type=Decimal, default=Decimal(0), help="fulfillment cost per order")
    p.add_argument("--payment-fee-pct", type=Decimal, default=Decimal(0), help="payment fee, percent of the price")
    p.add_argument("--vat-pct", type=Decimal, default=Decimal(0), help="VAT rate included in the price; 0 if VAT-exempt")
    a = p.parse_args()

    net_price = a.price / (1 + a.vat_pct / 100)
    fee = a.price * a.payment_fee_pct / 100
    margin = net_price - a.cost - a.packaging - a.fulfillment - fee

    print(f"price paid:        {money(a.price)}")
    if a.vat_pct:
        print(f"VAT ({a.vat_pct}%):        -{money(a.price - net_price)}")
    print(f"net price:         {money(net_price)}")
    print(f"purchase cost:    -{money(a.cost)}")
    print(f"packaging:        -{money(a.packaging)}")
    print(f"fulfillment:      -{money(a.fulfillment)}")
    print(f"payment fee:      -{money(fee)}")
    print(f"MARGIN:            {money(margin)}  ({money(margin / net_price * 100)}% of net price)")


if __name__ == "__main__":
    main()
