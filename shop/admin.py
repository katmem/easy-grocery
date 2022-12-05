from django.contrib import admin
from .models import Products, Customers, CustomersWithoutAccount, Sales, CustomersWithAccount, CardPayment
from .models import PaymentMethod, Category, Subcategory, Subcategory2, Order, OrderItem, Quantity
from .forms import ProductForm

admin.site.register(Sales)
admin.site.register(Customers)
admin.site.register(CustomersWithAccount)
admin.site.register(CustomersWithoutAccount)
admin.site.register(CardPayment)
admin.site.register(PaymentMethod)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Subcategory2)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Quantity)

@admin.register(Products)
class PostsAdmin(admin.ModelAdmin):
    readonly_fields = ('salePrice', 'onSale', )
    form = ProductForm
