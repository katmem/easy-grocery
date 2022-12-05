from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Products(models.Model):
	Name		 	=	models.CharField(max_length = 30, blank = False, unique = True)
	Barcode		 	= 	models.CharField(max_length = 12, blank = False)
	Category 	 	= 	models.CharField(max_length = 30, blank = False)
	Subcategory  	= 	models.CharField(max_length = 30, blank = False)
	SubCategory2 	= 	models.CharField(max_length = 30, blank = False)
	Description  	= 	models.TextField(blank = True)
	Price 			= 	models.DecimalField(max_digits = 4, decimal_places = 2, blank = False)
	Photo 			= 	models.ImageField(upload_to = 'images/', blank = False)
	Quantity		= 	models.DecimalField(max_digits = 7, decimal_places = 3, blank = False)
	Availability 	= 	models.BooleanField(blank = False)
	OnSale 			= 	models.BooleanField(blank = False)
	SalePrice 		= 	models.DecimalField(max_digits = 4, decimal_places = 2, blank = True)
	SaleId			= 	models.ForeignKey('Sales', blank = True, on_delete = models.CASCADE)


class Sales(models.Model):
	SaleId		=	models.AutoField(blank = False, primary_key = True)
	SalePercent	=	models.DecimalField(max_digits = 4, decimal_places = 2, blank = False)
	TimeStart	=	models.DateTimeField(auto_now = False, auto_now_add = False)
	TimeEnd		=	models.DateTimeField(auto_now = False, auto_now_add = False)


'''class Customers(models.Model):
	Name		=	models.CharField(max_length = 30, blank = False)
	Surname		=	models.CharField(max_length = 30, blank = False)
	Phone		=	models.CharField(max_length = 10, blank = False)
	Email		=	models.EmailField(max_length=254, blank = False, unique = True)


class CustomersWithoutAccount(Customers):
	pass'''

class CustomersWithAccount(AbstractUser):

	COUNTRY_CHOICES = (
        ('Ελλάδα', 'Ελλάδα'),
    )

	COUNTY_CHOICES = (
        ('Νομός Φωκίδας', 'Νομός Φωκίδας'),
        ('Νομός Αιτωλοακαρνανίας', 'Νομός Αιτωλοακαρνανίας'),
        ('Νομός Αργολίδας', 'Νομός Αργολίδας'),
        ('Νομός Αρκαδίας', 'Νομός Αρκαδίας'),
        ('Νομός Άρτας', 'Νομός Άρτας'),
        ('Νομός Αχαίας', 'Νομός Αχαίας'),
        ('Νομός Αττικής', 'Νομός Αττικής'),
        ('Νομός Βοιωτίας', 'Νομός Βοιωτίας'),
        ('Νομός Γρεβενών', 'Νομός Γρεβενών'),
        ('Νομός Δράμας', 'Νομός Δράμας'),
        ('Νομός Δωδεκανήσου', 'Νομός Δωδεκανήσου'),
        ('Νομός Έβρου', 'Νομός Έβρου'),
        ('Νομός Ευβοίας', 'Νομός Ευβοίας'),
        ('Νομός Ευρυτανίας', 'Νομός Ευρυτανίας'),
        ('Νομός Ζακύνθου', 'Νομός Ζακύνθου'),
        ('Νομός Ηλείας', 'Νομός Ηλείας'),
        ('Νομός Ημαθίας', 'Νομός Ημαθίας'),
        ('Νομός Ηρακλείου', 'Νομός Ηρακλείου'),
        ('Νομός Θεσπρωτίας', 'Νομός Θεσπρωτίας'),
        ('Νομός Θεσσαλονίκης', 'Νομός Θεσσαλονίκης'),
        ('Νομός Ιωαννίνων', 'Νομός Ιωαννίνων'),
        ('Νομός Καβάλας', 'Νομός Καβάλας'),
        ('Νομός Καρδίτσας', 'Νομός Καρδίτσας'),
        ('Νομός Καστοριάς', 'Νομός Καστοριάς'),
        ('Νομός Κέρκυρας', 'Νομός Κέρκυρας'),
        ('Νομός Κεφαλλονιάς', 'Νομός Κεφαλλονιάς'),
        ('Νομός Κιλκίς', 'Νομός Κιλκίς'),
        ('Νομός Κοζάνης', 'Νομός Κοζάνης'),
        ('Νομός Κορινθίας', 'Νομός Κορινθίας'),
        ('Νομός Κυκλάδων', 'Νομός Κυκλάδων'),
        ('Νομός Λακωνίας', 'Νομός Λακωνίας'),
        ('Νομός Λάρισας', 'Νομός Λάρισας'),
        ('Νομός Λασιθίου', 'Νομός Λασιθίου'),
        ('Νομός Λέσβου', 'Νομός Λέσβου'),
        ('Νομός Λευκάδας', 'Νομός Λευκάδας'),
        ('Νομός Μαγνησίας', 'Νομός Μαγνησίας'),
        ('Νομός Μεσσηνίας', 'Νομός Μεσσηνίας'),
        ('Νομός Ξάνθης', 'Νομός Ξάνθης'),
        ('Νομός Πέλλας', 'Νομός Πέλλας'),
        ('Νομός Πιερίας', 'Νομός Πιερίας'),
        ('Νομός Πρέβεζας', 'Νομός Πρέβεζας'),
        ('Νομός Ρεθύμνου', 'Νομός Ρεθύμνου'),
        ('Νομός Ροδόπης', 'Νομός Ροδόπης'),
        ('Νομός Σάμου', 'Νομός Σάμου'),
        ('Νομός Σερρών', 'Νομός Σερρών'),
        ('Νομός Τρικάλων', 'Νομός Τρικάλων'),
        ('Νομός Φθιώτιδας', 'Νομός Φθιώτιδας'),
        ('Νομός Φλώρινας', 'Νομός Φλώρινας'),
        ('Νομός Φωκίδας', 'Νομός Φωκίδας'),
        ('Νομός Χαλκιδικής', 'Νομός Χαλκιδικής'),
        ('Νομός Χανίων', 'Νομός Χανίων'),
        ('Νομός Χίου', 'Νομός Χίου'),
    )
	'''Name		=	models.CharField(max_length = 30, blank = False)
	Surname		=	models.CharField(max_length = 30, blank = False)'''
	Phone		=	models.CharField(max_length = 10, blank = False)
	'''Email		=	models.EmailField(max_length=254, blank = False, unique = True)
	Username	=	models.CharField(max_length = 30, blank = False, unique = True)
	Password	=	models.CharField(max_length = 30, blank = False, unique = False)'''
	Country		=	models.CharField(max_length = 6, blank = False, choices = COUNTRY_CHOICES)
	County 		=	models.CharField(max_length = 30, blank = False, choices = COUNTY_CHOICES)
	Region		=	models.CharField(max_length = 30, blank = False)
	Address 	=	models.CharField(max_length = 30, blank = False)
	AddressNum	=	models.CharField(max_length = 3, blank = False)
	Postcode	=	models.CharField(max_length = 5, blank = False)


class Payment(models.Model):
	CardNum			=	models.CharField(max_length = 16, blank = True, unique = True, null = True)
	CardName		=	models.CharField(max_length = 61, blank = False)
	SecurityCode	=	models.CharField(max_length = 3, blank = False)
	ExpiryYear		=	models.PositiveIntegerField(blank = False)
	ExpiryMonth		=	models.PositiveIntegerField(blank = False)
	ReceiptNum		= 	models.AutoField(blank = False, primary_key = True)		
	OrderNum 		= 	models.OneToOneField('Orders', null = False, blank = False, on_delete = models.CASCADE)
	COD 			=	models.BooleanField(blank = False)


class Orders(models.Model):
	OrderNum		=	models.AutoField(blank = False, primary_key = True)
	OrderTime		=	models.DateTimeField(auto_now = False, auto_now_add = False)
	DeliveryTime	=	models.DateTimeField(auto_now = False, auto_now_add = False)
	Delivered		=	models.BooleanField(blank = False)
	TotalAmount		=	models.DecimalField(max_digits = 5, decimal_places = 2, blank = False)
	Country			=	models.CharField(max_length = 30, blank = False)
	County 			=	models.CharField(max_length = 30, blank = False)
	Region			=	models.CharField(max_length = 30, blank = False)
	Address 		=	models.CharField(max_length = 30, blank = False)
	AddressNum		=	models.CharField(max_length = 3, blank = False)
	Postcode		=	models.CharField(max_length = 5, blank = False)
	Email			=	models.ForeignKey('CustomersWithAccount', blank = False, on_delete = models.CASCADE, null = False)


class Contains(models.Model):
	QuantityKg		=	models.DecimalField(max_digits = 7, decimal_places = 3, blank = True)
	QuantityPieces	=	models.PositiveIntegerField(blank = True)
	OrderNum		=	models.ForeignKey('Orders', blank = False, on_delete = models.CASCADE)
	Barcode			=	models.ForeignKey('Products', blank = False, on_delete = models.CASCADE)

