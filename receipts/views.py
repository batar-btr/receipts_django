from django.shortcuts import render
from .models import Receipt
# Create your views here.


def index(request):
    """The main Receipts app's page."""
    return render(request, 'receipts/index.html')


def receipts(request):
    """The receipts list page"""
    receipts = Receipt.objects.order_by('date_time')
    context = {'receipts': receipts}
    return render(request, 'receipts/receipts.html', context)
