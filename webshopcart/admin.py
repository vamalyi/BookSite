from django.contrib import admin
from webshopcart.models import ProductInCart, ProductCart


class ProductInCartInline(admin.TabularInline):
    model = ProductInCart
    extra = 0


class ProductCartAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'closed', 'paid', 'all_products', 'date_on_add', 'sum', 'check_sum')
    inlines = (ProductInCartInline, )


admin.site.register(ProductInCart)
admin.site.register(ProductCart, ProductCartAdmin)
