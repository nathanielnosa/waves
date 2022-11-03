from django.contrib import admin

# Register your models here.
from . models import Banner, Order , Product,Cart,CartProduct

admin.site.register(Banner)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)