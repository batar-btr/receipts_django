"""Define URL patterns for receipts"""

from django.urls import path

from . import views

app_name = 'receipts'

urlpatterns = [
    # Main page.
    path('', views.index, name='index'),
    path('receipts/', views.receipts, name='receipts')
]
