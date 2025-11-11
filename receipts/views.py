from django.shortcuts import render
from .models import Receipt, Item
from django.db.models import Sum
# Create your views here.


def index(request):
    """The main Receipts app's page."""
    return render(request, 'receipts/index.html')


def receipts(request):
    """The receipts list page"""
    receipts = Receipt.objects.order_by('date_time')
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
    items_summary = (
        Item.objects
        .values('name')  # GROUP BY name
        .annotate(
            total_price=Sum('sum'),
            total_quantity=Sum('quantity')
        )
        .order_by('-total_price')  # optional
    )
    context = {"items": items_summary}
    return render(request, 'receipts/items.html', context)


def search_items(request):
    query = request.GET.get("q", "").strip()
    group = request.GET.get("group", "").strip()

    items = Item.objects.none()
    totals = {}

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
            total_quantity=Sum("quantity")
        )
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
        "grouped": grouped
    })
