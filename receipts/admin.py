from django.contrib import admin

# Register your models here.
from .models import Receipt
from .models import Item

admin.site.register([Receipt, Item])
