from django.shortcuts import render
from .models import Receipt, Item
from django.db.models import Sum, F, Avg, Min
from django.utils import timezone
import pandas as pd
from datetime import datetime
import plotly.express as px
from .utils.charts import create_total_sum_plot, get_multiple_axes_plot, histogram
# Create your views here.


def index(request):
    """The main Receipts app's page."""
    return render(request, 'receipts/index.html')


def receipts(request):
    """The receipts list page"""
    receipts = Receipt.objects.order_by('-date_time')
    context = {'receipts': receipts}
    return render(request, 'receipts/receipts.html', context)


def receipt(request, receipt_number):
    """The single receipt page - shows all items"""
    receipt = Receipt.objects.get(receipt_number=receipt_number)
    items = receipt.items.all()
    context = {"items": items, "receipt": receipt}
    return render(request, 'receipts/receipt.html', context)


def items(request):
    """Show distinct items"""
    query_name = request.GET.get('name')
    plot_html = ""

    if query_name:

        items = (
            Item.objects
            .filter(name=query_name)
            .values("name", "receipt__receipt_number")
            .annotate(
                total_sum=Sum('sum'),
                total_quantity=Sum('quantity'),
                receipt_date=F("receipt__date_time"),
                price=Avg("price")
            )
            .order_by('receipt__date_time')
        )

        # plot_html = create_total_sum_plot(items, query_name)
        # plot_html = get_multiple_axes_plot(items)
        plot_html = histogram(items)

    else:
        items = (
            Item.objects
            .values('name')  # GROUP BY name
            .annotate(
                total_price=Sum('sum'),
                total_quantity=Sum('quantity')
            )
            .order_by('-total_price')  # optional
        )
    context = {"items": items, "query_name": query_name, "plot": plot_html}
    return render(request, 'items/items.html', context)


def search_items(request):
    query = request.GET.get("q", "").strip()
    group = request.GET.get("group", "").strip()

    items = Item.objects.none()
    totals = {}
    total_days = 1

    if query:
        items = (
            Item.objects
            .filter(name__icontains=query)
            .select_related("receipt")
            .order_by("-receipt__date_time")
        )
        # ORM aggregation (efficient single SQL query)
        totals = items.aggregate(
            total_sum=Sum("sum"),
            total_quantity=Sum("quantity"),
            days=Min("receipt__date_time")
        )
        try:
            total_days = (timezone.now().date() -
                          datetime.fromisoformat(totals["days"]).date()).days
        except:
            print('Error')

    if group == "name":
        items = (
            items.values("name")
            .annotate(total_quantity=Sum("quantity"), total_sum=Sum("sum"))
            .order_by("name")
        )
        grouped = True
    else:
        grouped = False

    return render(request, "items/search.html", {
        "query": query,
        "items": items,
        "totals": totals,
        "avg": total_days,
        "avg_sum": totals.get('total_sum', 1) / total_days,
        "grouped": grouped
    })
