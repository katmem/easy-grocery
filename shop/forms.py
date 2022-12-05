from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import (Subcategory, Subcategory2, Products, CustomersWithoutAccount,
                    CustomersWithAccount, PaymentMethod, CardPayment)
from .choices import COUNTRY_CHOICES, COUNTY_CHOICES

class RegistrationForm(UserCreationForm):
    """Form for user registration."""
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=True, label="Όνομα")
    last_name = forms.CharField(required=True, label="Επίθετο")
    password1 = forms.CharField(label=("Κωδικός πρόσβασης"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Επιβεβαίωση κωδικού πρόσβασης"),
        widget=forms.PasswordInput,
        help_text=("Εισάγετε τον ίδιο κωδικό με παραπάνω για επιβεβαίωση."))

    class Meta:
        model = User
        fields = {
            'username', 'first_name','last_name','email','password1','password2'
        }

        fields = ('username', 'first_name','last_name','email','password1','password2')

        labels = {
            "username": "Όνομα χρήστη",
            "password1": "Κωδικός πρόσβασης"
        }

        def save(self, commit = True):
            """Saves the form data."""
            user = super(RegistrationForm, self.save(commit = False))
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']

            if commit:
                user.save()

            return user

class RegisterForm(ModelForm):
    class Meta:
        model = CustomersWithAccount
        fields = ['phone', 'country', 'county', 'region', 'address', 'addressNum', 'postcode']

        labels = {
            "phone":"Τηλέφωνο",
            "country":"Χώρα",
            "county":"Νομός",
            "region":"Περιοχή",
            "address":"Διεύθυνση",
            "addressNum":"Αριθμός",
            "postcode":"ΤΚ"
        }

class ProductForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = ('name', 'barcode', 'category', 'subcategory', 'subcategory2',
                  'description', 'slug', 'price', 'photo', 'quantity', 'available', 'saleId')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = Subcategory.objects.none()
        self.fields['subcategory2'].queryset = Subcategory2.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(
                                                      category_id = category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('name')

        if 'subcategory' in self.data:
            try:
                subcategory_id = int(self.data.get('subcategory'))
                self.fields['subcategory2'].queryset = Subcategory2.objects.filter(
                                                       subcategory_id = subcategory_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subcategory2'].queryset = self.instance.subcategory.subcategory2_set.order_by('name')


class CheckoutForm(forms.ModelForm):
    """Checkout form for adding user's details about delivery"""
    class Meta:
        model = CustomersWithoutAccount
        fields = ('first_name', 'last_name', 'email', 'phone', 'country',
                  'county', 'region', 'address', 'addressNum', 'postcode')
        labels = {
            "first_name":"Όνομα",
            "last_name":"Επίθετο",
            "email":"Email",
            "phone":"Τηλέφωνο",
            "country":"Ελλάδα",
            "county":"Νομός",
            "region":"Περιοχή",
            "address":"Διεύθυνση",
            "addressNum":"Αριθμός",
            "postcode":"ΤΚ",
        }

        def save(self, commit = True):
            """Saves the form data."""
            checkout = checkout_form.save(commit = False)
            checkout.first_name = self.cleaned_data['first_name']
            checkout.last_name = self.cleaned_data['last_name']
            checkout.email = self.cleaned_data['email']
            checkout.phone = self.cleaned_data['phone']
            checkout.country = self.cleaned_data['country']
            checkout.county = self.cleaned_data['county']
            checkout.region = self.cleaned_data['region']
            checkout.address = self.cleaned_data['address']
            checkout.addressNum = self.cleaned_data['addressNum']
            checkout.postcode = self.cleaned_data['postcode']

            if commit:
                checkout.save()

            return checkout

class PaymentMethodForm(forms.ModelForm):
    """Form for choosing the payment method."""
    class Meta:
        model = PaymentMethod
        fields = ['method',]
        labels = {"method":"Μέθοδος πληρωμής",}

        def save(self, commit = True):
            """Saves the form data."""
            payment_method = payment_form.save(commit=False)
            payment_method.method = self.cleaned_data['method']

            if commit:
                payment_method.save()

            return payment_method


class QuantityForm(forms.Form):
    """Form for adding the quantity of an item to the cart."""
    quantity = forms.IntegerField(min_value=1, max_value=50)

class CardPaymentForm(forms.ModelForm):
    """Card payment form for adding the card details."""
    class Meta:
        model = CardPayment
        fields = ['cc_number', 'cc_expiry', 'cc_code',]
        labels = {  "cc_number":"Κωδικός κάρτας",
                    "cc_expiry":"Ημερομηνία λήξης κάρτας",
                    "cc_code":"Κωδικός ασφαλείας",
                 }

        def save(self, commit=True):
            """Saves the card data."""
            card = card_form.save(commit = False)
            card.cc_number = self.cleaned_data['cc_number']
            card.cc_expiry = self.cleaned_data['cc_expiry']
            card.cc_code = self.cleaned_data['cc_code']

            if commit:
                card.save()

            return card

class UpdateForm(forms.Form):
    """Form for updating user's profile."""
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=True, label="Όνομα")
    last_name = forms.CharField(required=True,label="Επίθετο")
    phone = forms.CharField(max_length=10)
    country = forms.ChoiceField(choices=COUNTRY_CHOICES)
    county = forms.ChoiceField(choices=COUNTY_CHOICES)
    region = forms.CharField(max_length=30)
    address = forms.CharField(max_length=30)
    addressNum = forms.CharField(max_length=3)
    postcode = forms.CharField(max_length=5)
