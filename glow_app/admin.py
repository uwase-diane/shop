from django.contrib import admin
from .models import Item,Orderitem,Order,Category

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Orderitem)
admin.site.register(Category)


