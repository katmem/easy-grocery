from datetime import datetime
from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.urls import reverse
from creditcards import types
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
from .choices import COUNTRY_CHOICES, COUNTY_CHOICES, PAYMENT_CHOICES

class Category(models.Model):
    """Contains the categories of the supermarket products like bakery and dairy"""
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('list_of_product_by_category', args=[self.slug])

class Subcategory(models.Model):
    """
    Contains the subcategories of every product category.
    For example, subcategories of the "Dairy" category are "Milk", "Yogurt", "Cheese".
    """

    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('list_of_product_by_subcategory', args=[self.slug])

class Subcategory2(models.Model):
    """
    Contains the subcategories of every product subcategory.
    For example, subcategories of the "Cheese" subcategory are "Creamy cheese", "Mozzarella", "Gouda", etc.
    """

    subcategory = models.ForeignKey('Subcategory', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('list_of_product_by_subcategory2', args=[self.slug])

class Products(models.Model):
    """Contains fields related to product information like category to which it belongs, name, price, discount."""
    category = models.ForeignKey('Category', max_length=30, null=True, on_delete=models.CASCADE)
    subcategory = models.ForeignKey('Subcategory', max_length=30, null=True, on_delete=models.CASCADE)
    subcategory2 = models.ForeignKey('Subcategory2', max_length=30, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=False, unique=True)
    barcode = models.CharField(max_length=12, blank=False)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=4, decimal_places=2, blank=False)
    photo = models.ImageField(upload_to='img/', blank=False)
    quantity = models.DecimalField(max_digits=7, decimal_places=3, blank=False)
    available = models.BooleanField(blank=False)
    saleId = models.ForeignKey('Sales', blank=True, on_delete=models.CASCADE, null=True)
    salePrice = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def get_sale_price(self):
        """
        Returns the discounted price of a product if there is a discount,
        otherwise it returns 0."""

        if self.saleId:
            return Decimal(self.price-self.saleId.SalePercent*self.price/100).quantize(Decimal('0.01'))
        return 0

    salePrice = property(get_sale_price)

    def get_on_sale(self):
        """Returns True if the product is still on sale, otherwise it returns 0."""
        if self.saleId:
            return self.saleId.TimeStart<=datetime.now().replace(tzinfo=timezone.utc) and self.saleId.TimeEnd>=datetime.now().replace(tzinfo=timezone.utc)
        return False

    onSale = property(get_on_sale)

class Sales(models.Model):
    """Contains fields about sales like start and end times."""
    SaleId = models.AutoField(blank=False, primary_key=True)
    SalePercent = models.PositiveIntegerField(blank=False)
    TimeStart = models.DateTimeField(auto_now=False, auto_now_add=False)
    TimeEnd = models.DateTimeField(auto_now=False, auto_now_add=False)

class Customers(models.Model):
    """Contains fields about customers."""
    phone = models.CharField(max_length=10, blank=False)
    country = models.CharField(max_length=6, blank=False, choices=COUNTRY_CHOICES)
    county = models.CharField(max_length=30, blank=False, choices=COUNTY_CHOICES)
    region = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=30, blank=False)
    addressNum = models.CharField(max_length=3, blank=False)
    postcode = models.CharField(max_length=5, blank=False)
    items = models.ManyToManyField(Products, blank=True)

class CustomersWithoutAccount(Customers):
    """
    Contains fields about customers who don't have an account.
    These will be used for the order delivery.
    """

    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    email = models.EmailField()

class CustomersWithAccount(Customers):
    """Contains the user field (for users who have an account)."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return str(self.user.username)

class PaymentMethod(models.Model):
    """Contains the method of the payment which can be cash or card."""
    method = models.CharField(max_length=30, choices=PAYMENT_CHOICES)

class CardPayment(models.Model):
    """Contains fields about the card payment."""
    cc_number = CardNumberField(_('card number'))
    cc_expiry = CardExpiryField(_('expiration date'))
    cc_code = SecurityCodeField(_('security code'))

    assert types.get_type('4444333322221111')==types.CC_TYPE_VISA
    assert types.get_type('343434343434343')==types.CC_TYPE_AMEX
    assert types.get_type('0000000000000000')==types.CC_TYPE_GENERIC

class OrderItem(models.Model):
    """Contains fields about the items that have been added to the cart."""
    product = models.OneToOneField(Products, on_delete=models.CASCADE, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)
    date_added_to_cart = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

class Order(models.Model):
    """Contains fields about orders like total amount, date ordered, items ordered."""
    ref_code = models.CharField(max_length=15)
    items = models.ManyToManyField(OrderItem, through='Quantity')
    owner = models.ForeignKey(CustomersWithAccount, on_delete=models.CASCADE, null=True)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now=True)
    order_total = models.DecimalField(default=0, max_digits=4, decimal_places=2)
    paymentmethod = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True)
    credit_card = models.ForeignKey(CardPayment, on_delete=models.CASCADE, null=True)

    def get_cart_items(self):
        """Returns the items that have been added to the cart."""
        return self.items.all().order_by('date_added_to_cart')

    def get_cart_total(self):
        """Returns the total amount of the items of the cart."""
        return sum([item.product.price for item in self.items.all()])

    def __str__(self):
        return f"{self.owner} - {self.ref_code}"

class Quantity(models.Model):
    """Contains fields about the quantity of the items that will be ordered."""
    ref_code = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1,  null=True)
    date_modified = models.DateTimeField(auto_now=True)

    def get_product_quantity(self):
        """Returns the quantity of an item that has been added to the cart."""
        return str(self.quantity)
