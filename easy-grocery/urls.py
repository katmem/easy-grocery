"""easy-grocery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from shop import views
from shop.views import register_view, index_view

urlpatterns = [
    path('test_template.html', index_view),
    path('admin/', admin.site.urls),
    url(r'^register/$', register_view, name='register'),
    path('', index_view, name = 'home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ajax/load-subcategories/',
        views.load_subcategories,
        name='ajax_load_subcategories'
        ),
    path('ajax/load-subcategories2/',
        views.load_subcategories2,
        name='ajax_load_subcategories2'
        ),
    url(r'^category/(?P<category_slug>[-\w]+)/$',
        views.list_of_product_by_category,
        name='list_of_product_by_category'
        ),
    url(r'^category/(?P<category_slug>[-\w]+)/subcategory/(?P<subcategory_slug>[-\w]+)$',
        views.list_of_product_by_subcategory,
        name='list_of_product_by_subcategory'
        ),
    url(r'^category/(?P<category_slug>[-\w]+)/subcategory/(?P<subcategory_slug>[-\w]+)/subcategory2/(?P<subcategory2_slug>[-\w]+)$',
        views.list_of_product_by_subcategory2,
        name='list_of_product_by_subcategory2'
        ),
    url(r'^product/(?P<product_slug>[-\w]+)/$',
        views.product_detail,
        name='product_detail'
        ),

    url(r'^add-to-cart/(?P<item_id>[-\w]+)$',
        views.add_to_cart_product_detail,
        name='add_to_cart_product_detail'
        ),
    url(r'^add-to-cart-order-summary/(?P<item_id>[-\w]+)$',
        views.add_to_cart_order_summary,
        name='add_to_cart_order_summary'
        ),
    url(r'^add-to-cart-from-offers/(?P<item_id>[-\w]+)$',
        views.add_to_cart_from_offers,
        name='add_to_cart_from_offers'
        ),
    url(r'^add-to-cart-from-category/(?P<item_id>[-\w]+)$',
        views.add_to_cart_from_category,
        name='add_to_cart_from_category'
        ),
    url(r'^add-to-cart-from-subcategory/(?P<item_id>[-\w]+)$',
        views.add_to_cart_from_subcategory,
        name='add_to_cart_from_subcategory'
        ),
    url(r'^add-to-cart-from-subcategory2/(?P<item_id>[-\w]+)$',
        views.add_to_cart_from_subcategory2,
        name='add_to_cart_from_subcategory2'
        ),
    url(r'^order-summary/$', views.order_details, name='order_summary'),
    url(r'^success/$', views.success, name='purchase_success'),
    url(r'^item/delete/(?P<item_id>[-\w]+)$', views.delete_from_cart, name='delete_from_cart'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^payment/(?P<order_id>[-\w]+)$', views.process_payment, name='process_payment'),
    url(r'^update-transaction/(?P<order_id>[-\w]+)/(?P<checkout>[-\w]+)/(?P<total_sum>\d+\.\d{2})/(?P<payment_method_id>[-\w]+)/(?P<card_id>[-\w]+)/$',
        views.update_transaction_records, name='update_records'),
    url(r'^my-orders/$', views.my_profile, name='my_profile'),
    url(r'^you-must-be-registered/$', views.anonymous, name='anonymous'),
    url(r'^payment/(?P<total_sum>\d+\.\d{2})/(?P<order_id>[-\w]+)/(?P<checkout>[-\w]+)/$',
        views.payment, name='payment'),
    url(r'^card-payment/(?P<total_sum>\d+\.\d{2})/(?P<order_id>[-\w]+)/(?P<checkout>[-\w]+)/(?P<payment_method_id>[-\w]+)/$',
        views.card_payment, name='card_payment'),
    url(r'^update-profile/$', views.update_profile, name='update_profile'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^offers/$', views.offers, name='offers'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
