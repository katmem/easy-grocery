"""
Views that handle the entire website's operations including user registration, 
viewing and adding products to cart, card payment and viewing order history
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.views.generic import ListView, CreateView, UpdateView
from .forms import (RegisterForm, RegistrationForm, ProductForm, CheckoutForm,
                    QuantityForm, PaymentMethodForm, CardPaymentForm, UpdateForm)
from .models import (Quantity, Products, Category, Subcategory, Subcategory2,
                    OrderItem, Order, CustomersWithAccount, CustomersWithoutAccount,
                    PaymentMethod, CardPayment)
from .extras import generate_order_id

def change_password(request):
    """Handles the password update process."""
    storage = messages.get_messages(request)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Ο κωδικός σας άλλαξε με επιτυχία!')
            return redirect('change_password')
        messages.error(request, 'Παρακαλούμε διορθώστε το λάθος.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'shop/change_password.html', {'form':form, 'messages':storage})

def update_profile(request):
    """Updates the profile of the user with the new data he entered to the form."""
    storage = messages.get_messages(request)
    current_user = CustomersWithAccount.objects.filter(user = request.user).first()
    initial= {'first_name':request.user.first_name,
              'last_name':request.user.last_name,
              'email':request.user.email,
              'phone':current_user.phone,
              'country':current_user.country,
              'county':current_user.county,
              'region':current_user.region,
              'address':current_user.address,
              'addressNum':current_user.addressNum,
              'postcode':current_user.postcode
              }
    if request.method == 'POST':
        update_profile_form = UpdateForm(request.POST, initial)
        if update_profile_form.is_valid():
            request.user.first_name = update_profile_form.cleaned_data['first_name']
            request.user.last_name = update_profile_form.cleaned_data['last_name']
            request.user.email = update_profile_form.cleaned_data['email']
            current_user.phone = update_profile_form.cleaned_data['phone']
            current_user.country = update_profile_form.cleaned_data['country']
            current_user.county = update_profile_form.cleaned_data['county']
            current_user.region = update_profile_form.cleaned_data['region']
            current_user.address = update_profile_form.cleaned_data['address']
            current_user.addressNum = update_profile_form.cleaned_data['addressNum']
            current_user.postcode = update_profile_form.cleaned_data['postcode']
            request.user.save()
            current_user.save()
            messages.success(request, 'Οι αλλαγές αποθηκεύτηκαν!')
            return redirect('update_profile')
        messages.error(request, 'Παρακαλούμε διορθώστε το λάθος.')
    else:
        update_profile_form = UpdateForm(initial)

    return render(request, "shop/update_profile.html",
                  {'update_profile_form':update_profile_form,
                  'messages':storage}
                 )

def anonymous(request):
    """Renders the page for the anonymous users if the user is unauthenticated."""
    return render(request, 'shop/anonymous.html', {})

def my_profile(request):
    """Renders the page in which the user's order history is displayed."""
    my_user_profile = CustomersWithAccount.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
    my_items = []
    total_orders = 0
    for order in my_orders:
        total_orders = total_orders+1
        my_items.append(Quantity.objects.filter(ref_code_id=order.id))
    return render(request, "shop/profile.html",
                  {'my_orders':my_orders,
                   'my_items':my_items,
                   'total_orders':total_orders
                  }
                 )

def get_user_pending_order(request):
    """Returns the order which has not been completed yet, otherwise it returns 0."""
    user_profile = get_object_or_404(CustomersWithAccount, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        return order[0]
    return 0

def add_to_cart_product_detail(request, **kwargs):
    """Handles adding to cart when the user is on the page with the product details."""
    user_profile = get_object_or_404(CustomersWithAccount, user=request.user)
    product = Products.objects.filter(id = kwargs.get('item_id', "")).first()
    quantity = request.session['quantity']
    order_item, status = OrderItem.objects.get_or_create(product=product)

    order_item.date_added_to_cart = datetime.now()
    order_item.save()

    user_order = Order.objects.filter(owner=user_profile, is_ordered=False).first()
    if user_order is None:
        user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
        Quantity.objects.create(ref_code_id=user_order.id,
                                product_id=order_item.id,
                                quantity=quantity)
    else:
        for item in user_order.get_cart_items():
            if order_item==item:
                existing_product = Quantity.objects.filter(
                                    ref_code_id=user_order.id,
                                    product_id=order_item.id).first()
                existing_product = Quantity.objects.filter(
                                    ref_code_id=user_order.id,
                                    product_id=order_item.id).first().delete()
                order_item.date_added = datetime.now()
                order_item.save()

        Quantity.objects.create(ref_code_id=user_order.id,
                                product_id=order_item.id,
                                quantity=quantity)
    if status:
        user_order.ref_code = generate_order_id()
        user_order.save()
    return redirect(reverse('product_detail', kwargs={'product_slug':product.slug}))

def add_to_cart_order_summary(request, **kwargs):
    """Handles adding to cart when the user is on the order summary page."""
    quantity = request.POST.get('quantities')
    user_profile = get_object_or_404(CustomersWithAccount, user=request.user)
    product = Products.objects.filter(id=kwargs.get('item_id', "")).first()
    order_item, status = OrderItem.objects.get_or_create(product=product)
    order_item.date_added_to_cart = datetime.now()
    order_item.save()
    user_order = Order.objects.filter(owner=user_profile, is_ordered=False).first()
    if user_order is None:
        user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
        Quantity.objects.create(ref_code_id=user_order.id,
                                product_id=order_item.id,
                                quantity=quantity)
    else:
        for item in user_order.get_cart_items():
            if order_item==item:
                existing_product = Quantity.objects.filter(ref_code_id=user_order.id,
                                                            product_id=order_item.id).first()
                existing_product = Quantity.objects.filter(ref_code_id=user_order.id,
                                                            product_id=order_item.id
                                                          ).first().delete()
                order_item.date_added = datetime.now()
                order_item.save()

        Quantity.objects.create(ref_code_id=user_order.id,
                                product_id=order_item.id,
                                quantity=quantity)
    if status:
        user_order.ref_code = generate_order_id()
        user_order.save()
    return redirect(reverse('order_summary'))

def add_to_cart_from_offers(request, **kwargs):
    """Handles adding to cart when the user is on the offers page."""
    quantity = request.POST.get('quantities')
    user_profile = get_object_or_404(CustomersWithAccount, user=request.user)
    product = Products.objects.filter(id=kwargs.get('item_id', "")).first()
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        current_order_products = [product.product for product in user_order_items]
        current_product_id = product.id
        found = False
        if product is not None:
            for item in user_order_items:
                if item.product.id==current_product_id:
                    found = True
                    current_quantity = Quantity.objects.filter(
                        ref_code_id=user_order.id,
                        product_id=item.id).first().quantity

        if found is False:
            current_quantity = 1

    order_item, status = OrderItem.objects.get_or_create(product=product)
    user_order = Order.objects.filter(owner=user_profile, is_ordered=False).first()
    order_item.date_added_to_cart = datetime.now()
    order_item.save()
    if user_order is None:
        user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
        Quantity.objects.create(ref_code_id=user_order.id,
                                product_id=order_item.id,
                                quantity=quantity)
    else:
        for item in user_order.get_cart_items():
            if order_item==item:
                existing_product = Quantity.objects.filter(ref_code_id=user_order.id,
                                                            product_id=order_item.id).first()
                existing_product = Quantity.objects.filter(ref_code_id=user_order.id,
                                                            product_id=order_item.id
                                                          ).first().delete()
                order_item.date_added = datetime.now()
                order_item.save()

        Quantity.objects.create(ref_code_id=user_order.id,
                                product_id=order_item.id,
                                quantity=quantity)

    if status:
        user_order.ref_code = generate_order_id()
        user_order.save()
    return redirect(reverse('offers'))

def add_to_cart_from_category(request, **kwargs):
    """Handles adding to cart when the user is on the product categories page."""
    quantity = request.POST.get('quantities')
    user_profile = get_object_or_404(CustomersWithAccount, user=request.user)
    product = Products.objects.filter(id = kwargs.get('item_id', "")).first()
    category_slug = product.category.slug
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        current_order_products = [product.product for product in user_order_items]

        current_product_id = product.id

        found = False
        if product is not None:
            for item in user_order_items:
                if item.product.id==current_product_id:
                    found = True
                    current_quantity = Quantity.objects.filter(ref_code_id=user_order.id,
                                                               product_id=item.id).first().quantity
        if found is False:
            current_quantity = 1

    order_item, status = OrderItem.objects.get_or_create(product=product)
    user_order = Order.objects.filter(owner=user_profile, is_ordered=False).first()
    order_item.date_added_to_cart = datetime.now()
    order_item.save()
    if user_order is None:
        user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
        Quantity.objects.create(ref_code_id=user_order.id,
                                product_id=order_item.id,
                                quantity=quantity)
    else:
        for item in user_order.get_cart_items():
            if order_item==item:
                existing_product = Quantity.objects.filter(ref_code_id=user_order.id,
                                                            product_id=order_item.id).first()
                existing_product = Quantity.objects.filter(ref_code_id=user_order.id,
                                                            product_id=order_item.id
                                                          ).first().delete()
                order_item.date_added = datetime.now()
                order_item.save()

        Quantity.objects.create(ref_code_id=user_order.id,
                                product_id=order_item.id,
                                quantity=quantity)

    if status:
        user_order.ref_code = generate_order_id()
        user_order.save()
    return redirect(reverse('list_of_product_by_category', kwargs={'category_slug':category_slug}))

def add_to_cart_from_subcategory(request, **kwargs):
    """Handles adding to cart when the user is on the product subcategory page."""
    quantity = request.POST.get('quantities')
    user_profile = get_object_or_404(CustomersWithAccount, user=request.user)
    product = Products.objects.filter(id = kwargs.get('item_id', "")).first()
    category_slug = product.category.slug
    subcategory_slug = product.subcategory.slug
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        current_order_products = [product.product for product in user_order_items]

        current_product_id = product.id

        found = False
        if product is not None:
            for item in user_order_items:
                if item.product.id==current_product_id:
                    found = True
                    current_quantity = Quantity.objects.filter(ref_code_id=user_order.id,
                                                                product_id=item.id).first().quantity

        if found is False:
            current_quantity = 1

    order_item, status = OrderItem.objects.get_or_create(product=product)
    user_order = Order.objects.filter(owner=user_profile, is_ordered=False).first()

    order_item.date_added_to_cart = datetime.now()
    order_item.save()

    if user_order is None:
        user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
        Quantity.objects.create(ref_code_id=user_order.id,
                                product_id=order_item.id,
                                quantity=quantity)
    else:
        for item in user_order.get_cart_items():
            if order_item==item:
                existing_product = Quantity.objects.filter(ref_code_id=user_order.id,
                                                            product_id=order_item.id).first()
                existing_product = Quantity.objects.filter(ref_code_id=user_order.id,
                                                            product_id=order_item.id
                                                          ).first().delete()
                order_item.date_added = datetime.now()
                order_item.save()

        Quantity.objects.create(ref_code_id=user_order.id,
                                product_id=order_item.id,
                                quantity=quantity)

    if status:
        user_order.ref_code = generate_order_id()
        user_order.save()
    return redirect(reverse('list_of_product_by_subcategory',
                    kwargs={'category_slug': category_slug, 'subcategory_slug':subcategory_slug}))

def add_to_cart_from_subcategory2(request, **kwargs):
    """Handles adding to cart when the user is on the 2nd subcategory page."""
    quantity = request.POST.get('quantities')
    user_profile = get_object_or_404(CustomersWithAccount, user=request.user)
    product = Products.objects.filter(id=kwargs.get('item_id', "")).first()
    category_slug = product.category.slug
    subcategory_slug = product.subcategory.slug
    subcategory2_slug = product.subcategory2.slug

    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        current_order_products = [product.product for product in user_order_items]
        current_product_id = product.id
        found = False
        if product is not None:
            for item in user_order_items:
                if item.product.id==current_product_id:
                    found = True
                    current_quantity = Quantity.objects.filter(ref_code_id=user_order.id,
                                                                product_id=item.id
                                                              ).first().quantity
        if found is False:
            current_quantity = 1

    order_item, status = OrderItem.objects.get_or_create(product=product)
    user_order = Order.objects.filter(owner=user_profile, is_ordered=False).first()
    order_item.date_added_to_cart = datetime.now()
    order_item.save()

    if user_order is None:
        user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
        Quantity.objects.create(ref_code_id=user_order.id,
                                product_id=(order_item.id),
                                quantity=quantity)

    else:
        for item in user_order.get_cart_items():
            if order_item==item:
                existing_product = Quantity.objects.filter(ref_code_id=user_order.id,
                                                            product_id=order_item.id).first()
                existing_product = Quantity.objects.filter(ref_code_id=user_order.id,
                                                            product_id=order_item.id
                                                          ).first().delete()
                order_item.date_added = datetime.now()
                order_item.save()

        Quantity.objects.create(ref_code_id=user_order.id,
                                product_id=order_item.id,
                                quantity=quantity)

    if status:
        user_order.ref_code = generate_order_id()
        user_order.save()

    return redirect(reverse('list_of_product_by_subcategory2',
                            kwargs={'category_slug': category_slug,
                                    'subcategory_slug':subcategory_slug,
                                    'subcategory2_slug': subcategory2_slug})
                    )

def delete_from_cart(request, item_id):
    """Handles deletion of a product from the cart."""
    existing_order = get_user_pending_order(request)
    item_to_delete = Quantity.objects.filter(product_id=item_id, ref_code_id=existing_order)
    if item_to_delete.exists():
        item_to_delete[0].delete()
    return redirect(reverse('order_summary'))


def order_details(request):
    """Renders the page showing the order summary."""
    productscat = Category.objects.all()
    productssub = Subcategory.objects.all()
    productssub2 = Subcategory2.objects.all()

    if not request.user.is_authenticated:
        context = {'productscat':productscat,
                   'productssub':productssub,
                   'productssub2':productssub2
                  }
        return render(request, 'shop/anonymous.html', context)

    existing_order = get_user_pending_order(request)
    # Save the quantities of each cart item to a list
    instance = Quantity.objects.filter(ref_code_id=existing_order).order_by('ref_code_id')

    instances=[]
    if existing_order != 0:
        for item in existing_order.get_cart_items():
            instances.append(Quantity.objects.get(ref_code=existing_order,
                                                  product=item).quantity)

        item_subtotal = []
        k = -1
        for item in existing_order.get_cart_items():
            k+=1
            for i, instance in enumerate(instances):
                if k==i:
                    if item.product.salePrice==0:
                        item_subtotal.append(item.product.price*instance)
                    else:
                        item_subtotal.append(item.product.salePrice*instance)

        total_sum = 0
        for i, subtotal in enumerate(item_subtotal):
            total_sum = total_sum + subtotal

        context = {'item_subtotal':item_subtotal,
                    'total_sum':total_sum,
                    'instance':instance,
                    'order':existing_order,
                    'productscat':productscat,
                    'productssub':productssub,
                    'productssub2':productssub2
                  }

    else:
        context = {'instance':instance,
                    'order':existing_order,
                    'productscat':productscat,
                    'productssub':productssub,
                    'productssub2':productssub2
                  }
    return render(request, 'shop/order_summary.html', context)

def checkout(request):
    """Renders the checkout page where the user enters the details related to delivery."""
    existing_order = get_user_pending_order(request)
    existing_user_name = User.objects.filter(username=existing_order.owner)
    existing_user_first_name = existing_user_name[0].first_name
    existing_user_last_name = existing_user_name[0].last_name
    existing_user_email = existing_user_name[0].email
    existing_user = existing_order.owner
    existing_user_phone = existing_user.phone
    existing_user_country = existing_user.country
    existing_user_county = existing_user.county
    existing_user_region = existing_user.region
    existing_user_address = existing_user.address
    existing_user_address_num = existing_user.addressNum
    existing_user_postcode = existing_user.postcode

    instance = Quantity.objects.filter(ref_code_id=existing_order).order_by('ref_code_id')[::-1]
    instances=[]

    for item in existing_order.get_cart_items():
        instances.append(Quantity.objects.get(ref_code=existing_order, product=item).quantity)

    item_subtotal = []
    k = -1
    for item in existing_order.get_cart_items():
        k+=1
        for i, instance in enumerate(instances):
            if k==i:
                if item.product.salePrice == 0:
                    item_subtotal.append(item.product.price*instance)
                else:
                    item_subtotal.append(item.product.salePrice*instance)

    total_sum = 0
    for i, subtotal in enumerate(item_subtotal):
        total_sum += subtotal

    if request.method == 'POST':
        checkout_form = CheckoutForm(request.POST, initial={'first_name':existing_user_first_name,
                                                            'last_name':existing_user_last_name,
                                                            'email':existing_user_email,
                                                            'phone':existing_user_phone,
                                                            'country':existing_user_country,
                                                            'county':existing_user_county,
                                                            'region':existing_user_region,
                                                            'address':existing_user_address,
                                                            'addressNum':existing_user_address_num,
                                                            'postcode':existing_user_postcode})
        if checkout_form.is_valid():
            checkout = checkout_form.save()
            return redirect(reverse('payment', kwargs={'total_sum':total_sum,
                                                        'order_id':existing_order.id,
                                                        'checkout':checkout.id}))
    else:
        checkout_form = CheckoutForm(initial={'first_name':existing_user_first_name,
                                                'last_name':existing_user_last_name,
                                                'email':existing_user_email,
                                                'phone':existing_user_phone,
                                                'country':existing_user_country,
                                                'county':existing_user_county,
                                                'region':existing_user_region,
                                                'address':existing_user_address,
                                                'addressNum':existing_user_address_num,
                                                'postcode':existing_user_postcode})

    productscat = Category.objects.all()
    productssub = Subcategory.objects.all()
    productssub2 = Subcategory2.objects.all()

    context = {'item_subtotal':item_subtotal,
                'total_sum':total_sum,
                'instance':instance,
                'checkout_form':checkout_form,
                'order':existing_order,
                'productscat':productscat,
                'productssub':productssub,
                'productssub2':productssub2}
    return render(request, 'shop/checkout.html', context)

def payment(request, **kwargs):
    """Handles user's choice of payment method, which can be either cash or card."""
    productscat = Category.objects.all()
    productssub = Subcategory.objects.all()
    productssub2 = Subcategory2.objects.all()

    total_sum = kwargs.get('total_sum')
    order_id = kwargs.get('order_id')
    checkout = kwargs.get('checkout')

    if request.method == 'POST':
        payment_form = PaymentMethodForm(request.POST)
        if payment_form.is_valid():
            payment_method = payment_form.save()
            if payment_method.method=='Πληρωμή με κάρτα':
                return redirect(reverse('card_payment',
                                        kwargs={'total_sum':total_sum,
                                                'order_id':order_id,
                                                'checkout':checkout,
                                                'payment_method_id':payment_method.id
                                                }))
            return redirect(reverse('update_records',
                                    kwargs={'total_sum':total_sum,
                                            'order_id':order_id,
                                            'checkout':checkout,
                                            'payment_method_id':payment_method.id,
                                            'card_id':0
                                            }))
    else:
        payment_form = PaymentMethodForm()

    context = {'payment_form':payment_form,
                'total_sum':total_sum,
                'order_id':order_id,
                'checkout':checkout,
                'productscat':productscat,
                'productssub':productssub,
                'productssub2':productssub2
              }
    return render(request, 'shop/payment_method.html', context)

def card_payment(request, **kwargs):
    """Handles the payment by card."""
    productscat = Category.objects.all()
    productssub = Subcategory.objects.all()
    productssub2 = Subcategory2.objects.all()

    total_sum = kwargs.get('total_sum')
    order_id = kwargs.get('order_id')
    checkout = kwargs.get('checkout')
    payment_method_id = kwargs.get('payment_method_id')

    if request.method == 'POST':
        card_form = CardPaymentForm(request.POST)
        if card_form.is_valid():
            card = card_form.save()
            return redirect(reverse('update_records',
                                    kwargs={'total_sum':total_sum,
                                            'order_id':order_id,
                                            'checkout':checkout,
                                            'payment_method_id':payment_method_id,
                                            'card_id':card.id
                                            }))
    else:
        card_form = CardPaymentForm()

    context = {'card_form':card_form,
                'total_sum':total_sum,
                'order_id':order_id,
                'checkout':checkout,
                'productscat':productscat,
                'productssub':productssub,
                'productssub2':productssub2,
                'payment_method_id':payment_method_id
              }
    return render(request, 'shop/card_payment.html', context)

def process_payment(request, order_id):
    return redirect(reverse('update_records', kwargs={'order_id':order_id}))

def update_transaction_records(request, order_id, checkout, total_sum, payment_method_id, card_id):
    order_to_purchase = Order.objects.filter(pk=order_id).first()
    order_to_purchase.is_ordered = True
    order_to_purchase.date_ordered = datetime.now()
    order_to_purchase.order_total = total_sum

    payment_instance = PaymentMethod.objects.filter(id=payment_method_id).first()
    order_to_purchase.paymentmethod = payment_instance

    if card_id!=0:
        card_instance = CardPayment.objects.filter(id=card_id).first()
        order_to_purchase.credit_card = card_instance

    order_to_purchase.payment = CustomersWithoutAccount.objects.filter(id=checkout)[0]
    order_to_purchase.save()

    order_items = order_to_purchase.items.all()
    order_items.update(is_ordered=True, date_ordered=datetime.now())
    user_profile = get_object_or_404(CustomersWithAccount, user=request.user)
    order_products = [item.product for item in order_items]
    user_profile.items.add(*order_products)
    user_profile.save()
    return redirect(reverse('my_profile'))

def success(request):
    return redirect(reverse('my_profile'))

def list_of_product_by_category(request, category_slug):
    """Renders the page which shows the products when the user clicks on a category."""
    productscat = Category.objects.all().order_by("name")
    productssub = Subcategory.objects.all().order_by("name")
    productssub2 = Subcategory2.objects.all().order_by("name")
    categories = Category.objects.all()
    product = Products.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        product = product.filter(category=category)

    if request.user.is_authenticated:
        filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
        current_order_products = []
        if filtered_orders.exists():
            user_order = filtered_orders[0]
            user_order_items = user_order.items.all()
            current_order_products = [product.product for product in user_order_items]
            quantity = Quantity.objects.filter(ref_code_id=user_order.id).order_by('ref_code_id')
        else:
            quantity = 0

        context = {'categories':categories,
                    'product':product,
                    'category': category,
                    'productscat':productscat,
                    'productssub':productssub,
                    'productssub2':productssub2,
                    'current_order_products':current_order_products,
                    'quantity':quantity
                  }
    else:
        context = {'categories':categories,
                    'product':product,
                    'category':category,
                    'productscat':productscat,
                    'productssub':productssub,
                    'productssub2':productssub2,
                    'anonymous':1
                  }
    template = 'shop/list_of_product_by_category.html'
    return render(request, template, context)

def list_of_product_by_subcategory(request, subcategory_slug):
    """Renders the page which shows the products when the user clicks on a subcategory."""
    productscat = Category.objects.all()
    productssub = Subcategory.objects.all()
    productssub2 = Subcategory2.objects.all()
    subcategories = Subcategory.objects.all()
    product = Products.objects.filter(available=True)
    if subcategory_slug:
        subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
        product= product.filter(subcategory=subcategory)

    if request.user.is_authenticated:
        filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
        current_order_products = []
        if filtered_orders.exists():
            user_order = filtered_orders[0]
            user_order_items = user_order.items.all()
            current_order_products = [product.product for product in user_order_items]
            quantity = Quantity.objects.filter(ref_code_id=user_order.id).order_by('ref_code_id')
        else:
            quantity = 0

        context = {'subcategories':subcategories,
                    'product':product,
                    'subcategory':subcategory,
                    'productscat':productscat,
                    'productssub':productssub,
                    'productssub2':productssub2,
                    'current_order_products':current_order_products,
                    'quantity':quantity
                  }

    else:
        context = {'subcategories':subcategories,
                    'product':product,
                    'subcategory':subcategory,
                    'productscat':productscat,
                    'productssub':productssub,
                    'productssub2':productssub2,
                    'anonymous':1
                  }
    template = 'shop/list_of_product_by_subcategory.html'
    return render(request, template, context)

def list_of_product_by_subcategory2(request, subcategory2_slug):
    """Renders the page which shows the products when the user clicks on the subcategory of a subcategory."""
    productscat = Category.objects.all()
    productssub = Subcategory.objects.all()
    productssub2 = Subcategory2.objects.all()
    subcategories2 = Subcategory2.objects.all()
    product = Products.objects.filter(available=True)
    if subcategory2_slug:
        subcategory2 = get_object_or_404(Subcategory2, slug=subcategory2_slug)
        product= product.filter(subcategory2=subcategory2)

    if request.user.is_authenticated:
        filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
        current_order_products = []
        if filtered_orders.exists():
            user_order = filtered_orders[0]
            user_order_items = user_order.items.all()
            current_order_products = [product.product for product in user_order_items]
            quantity = Quantity.objects.filter(ref_code_id=user_order.id).order_by('ref_code_id')
        else:
            quantity = 0

        context = {'subcategories2':subcategories2,
                    'product':product,
                    'subcategory2':subcategory2,
                    'productscat':productscat,
                    'productssub':productssub,
                    'productssub2':productssub2,
                    'current_order_products':current_order_products,
                    'quantity':quantity
                  }

    else:
        context = {'subcategories2':subcategories2,
                    'product':product,
                    'subcategory2':subcategory2,
                    'productscat':productscat,
                    'productssub':productssub,
                    'productssub2':productssub2,
                    'anonymous':1
                  }

    template = 'shop/list_of_product_by_subcategory2.html'
    return render(request, template, context)

def product_detail(request, product_slug):
    """Renders the page which shows the details of a single product."""
    productscat = Category.objects.all()
    productssub = Subcategory.objects.all()
    productssub2 = Subcategory2.objects.all()
    product = get_object_or_404(Products, slug=product_slug)
    current_product = Products.objects.filter(slug=product_slug).first().id

    if request.user.is_authenticated:
        filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
        current_order_products = []
        current_quantity = 1

        if filtered_orders.exists():
            user_order = filtered_orders[0]
            user_order_items = user_order.items.all()
            current_order_products = [product.product for product in user_order_items]

            found = False
            if current_product is not None:
                for item in user_order_items:
                    if item.product.id==current_product:
                        found = True
                        current_quantity = Quantity.objects.filter(ref_code_id=user_order.id,
                                                                    product_id = item.id
                                                                  ).first().quantity

            if found is False:
                current_quantity = 1
    else:
        current_quantity = 1

    if request.method == 'POST':
        quantity_form = QuantityForm(request.POST, initial={'quantity':current_quantity} )
        if quantity_form.is_valid():
            instance = quantity_form.cleaned_data['quantity']
            request.session['quantity'] = instance
            return redirect(reverse('add_to_cart_product_detail', kwargs={'item_id':product.id}))
    else:
        quantity_form = QuantityForm(initial={'quantity':current_quantity})

    if request.user.is_authenticated:
        context = {'quantity_form':quantity_form,
                    'product':product,
                    'productscat':productscat,
                    'productssub':productssub,
                    'productssub2':productssub2,
                    'current_order_products':current_order_products
                  }
    else:
        context = {'quantity_form':quantity_form,
                    'product':product,
                    'productscat':productscat,
                    'productssub':productssub,
                    'productssub2':productssub2,
                    'anonymous':1
                  }
    template = 'shop/single.html'
    return render(request, template, context)

class ProductListView(ListView):
    model = Products
    context_object_name = 'people'

class ProductCreateView(CreateView):
    model = Products
    form_class = ProductForm

class ProductUpdateView(UpdateView):
    model = Products
    form_class = ProductForm

def load_subcategories(request):
    """Finds the subcategories of a category and passes them to the template."""
    category_id = request.GET.get('category')
    subcategories = Subcategory.objects.filter(category_id=category_id).order_by('name')
    return render(request,
                  'subcategory_dropdown_list_options.html',
                  {'subcategories':subcategories})

def load_subcategories2(request):
    """Finds the subcategories of a subcategory and passes them to the template."""
    subcategory_id = request.GET.get('subcategory')
    subcategories2 = Subcategory2.objects.filter(subcategory_id=subcategory_id).order_by('name')
    return render(request,
                  'subcategory2_dropdown_list_options.html',
                  {'subcategories2':subcategories2})

def register_view(request):
    """Handles user registration."""
    productscat = Category.objects.all()
    productssub = Subcategory.objects.all()
    productssub2 = Subcategory2.objects.all()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        profile_form = RegisterForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()
            return redirect ('home')
    else:
        form = RegistrationForm()
        profile_form = RegisterForm()
    return render(request, "shop/register.html", {'form':form,
                                                    'profile_form':profile_form,
                                                    'productscat':productscat,
                                                    'productssub':productssub,
                                                    'productssub2':productssub2
                                                 })

def index_view(request):
    """Renders the homepage."""
    productscat = Category.objects.all().order_by("name")
    productssub = Subcategory.objects.all().order_by("name")
    productssub2 = Subcategory2.objects.all().order_by("name")
    context = {'productscat':productscat, 'productssub':productssub, 'productssub2':productssub2}
    return render(request, "shop/test_template.html", context)


def offers(request):
    """Renders the page which displays the offers."""
    product = [obj for obj in Products.objects.all() if obj.onSale ]
    productscat = Category.objects.all()
    productssub = Subcategory.objects.all()
    productssub2 = Subcategory2.objects.all()

    if request.user.is_authenticated:
        filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
        current_order_products = []
        if filtered_orders.exists():
            user_order = filtered_orders[0]
            current_order_products = [product.product for product in user_order.items.all()]
            quantity = Quantity.objects.filter(ref_code_id=user_order.id).order_by('ref_code_id')
        else:
            quantity = 0

        context = {'product':product,
                    'productscat':productscat,
                    'productssub':productssub,
                    'productssub2':productssub2,
                    'current_order_products':current_order_products,
                    'quantity':quantity
                  }
    else:
        context = {'product':product,
                    'productscat':productscat,
                    'productssub':productssub,
                    'productssub2':productssub2,
                    'anonymous':1
                  }
    return render(request, "shop/offers.html", context)
