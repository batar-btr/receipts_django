"""Define URL patterns for receipts"""

from django.urls import path

from . import views

app_name = 'receipts'

urlpatterns = [
    # Main page.
    path('', views.index, name='index'),
    path('receipts/', views.receipts, name='receipts'),
    path('receipts/<int:receipt_number>', views.receipt, name='receipt'),
    path('items/', views.items, name='items'),
    path("items/search/", views.search_items, name="search_items"),
    path("test", views.test_cat, name="test"),
    path('categories', views.categories, name="categories"),
    path('category/<slug:category_slug>',
         views.category_detail, name="category_detail"),
]
