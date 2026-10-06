from django.contrib import admin

from shopapp.models import *

class ProductAdmin(admin.ModelAdmin):
    list_display=('name','price')
    search_fields=('name',)
    list_filter=('price',)
    ordering=('-price',)

admin.site.register(Product,ProductAdmin)
class CustomUserAdmin(admin.ModelAdmin):
    list_display=('username','role')
admin.site.register(CustomUser,CustomUserAdmin)

class SellerAdmin(admin.ModelAdmin):
    list_display=('name', 'email', 'shop_name', 'phone', 'status')
admin.site.register(Seller,SellerAdmin)


