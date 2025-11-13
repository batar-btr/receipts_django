import pandas as pd
from ..models import Item
from django.db.models import Sum, F, Avg


def get_items_dataframe(name):
    items = (
        Item.objects
        .filter(name=name)
        .values("name", "receipt__receipt_number")
        .annotate(
            total_sum=Sum('sum'),
            total_quantity=Sum('quantity'),
            receipt_date=F("receipt__date_time"),
            price=Avg("price")
        )
        .order_by('receipt__date_time')
    )

    df = pd.DataFrame(items, columns=["total_sum", "receipt_date"])
    df.rename(columns={"receipt_date": "date"}, inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)

    return df
