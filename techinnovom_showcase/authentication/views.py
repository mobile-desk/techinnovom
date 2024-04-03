# views.py

import pyrebase
from requests.exceptions import HTTPError
from django.http import Http404
from django.http import JsonResponse
import requests
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
import random
from .models import CustomUser
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordResetView

from .forms import UserUploadForm


from django.core.mail import send_mail
from django.conf import settings
#from .utils import generate_referral_code
#from .forms import BusinessInfoForm


config = {
    "apiKey": "AIzaSyC_QcKwkwaFiIxdVBlY8EDidpWGlLndnW8",
    "authDomain": "techinnovom-showcase.firebaseapp.com",
    "databaseURL": "https://techinnovom-showcase-default-rtdb.firebaseio.com",
    "projectId": "techinnovom-showcase",
    "storageBucket": "techinnovom-showcase.appspot.com",
    "messagingSenderId": "685028861115",
    "appId": "1:685028861115:web:5cd16b660adccb66e7759e",
    "measurementId": "G-1WN04EPE2M"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
storage = firebase.storage()

def home(request):
    return render(request, 'home.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

#from django.contrib.auth.views import PasswordResetView

#class CustomPasswordResetView(PasswordResetView):
#    template_name = 'your_custom_template.html'


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == 'POST':
            name = request.POST.get('name')
            user_name = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password1 = request.POST.get('password1')
            referral = request.POST.get('referral')

            if CustomUser.objects.filter(username=user_name):
                messages.error(request, "Username already exists")
                return redirect('signup')

            if CustomUser.objects.filter(email=email):
                messages.error(request, "Email already exists")
                return redirect('signup')

            if len(user_name)>10:
                messages.error(request, "Username must be under 10 characters")
                return redirect('signup')

            if password != password1:
                messages.error(request, "Password does not match")
                return redirect('signup')


            # Create the user
            user = CustomUser.objects.create_user(username=user_name, email=email, password=password)
            user.first_name = name
            if referral:
                user.ref = referral
            user.save()


            product_data = {
                'username': user_name,
                'referral': referral,
                'email': email,
            }


            database.child('referral').child('signup').set(product_data)


            # Log in the user
            messages.success(request, "Your Account has been created successfully.")
            return redirect('login')

        return render(request, 'authentication/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')  # Redirect to the home page after successful login
            else:
                # Handle authentication failure
                # You may want to display an error message or redirect to a different page
                messages.error(request, "Login Error")
                return render(request, 'authentication/login.html')
        return render(request, 'authentication/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Replace 'login' with the name of your login page URL pattern


@login_required
def profile_view(request):
    # Fetch the current user's details
    user = request.user
    u = request.user.username
    # Retrieve user's products from Firebase
    user_products = database.child('data').child(u).child('products').get().val()
    business = database.child('business').child(u).child('products').get().val()


    context = {
        'user': user,
        'user_products': user_products,
        'business': business,
    }

    # Pass the user details to the template
    return render(request, 'authentication/profile.html', context)


@login_required
def manage_products(request):
    # Logic to fetch and display products for managing
    u = request.user.username


    #products = {
    #        'name': product_name,
    #        'price': product_price,
    #        'description': product_description,
    #        'image_url': storage.child(image_path).get_url() if product_image else None,
    #        'user_id': user.id
    #    }


    user = request.user
    total_products = user.totalproduct
    products = database.child('data').child(u).child('products').get().val()

    data = database.child("business").child(u).get().val()

    subscription_plan = data['subscription_plan']
    business = database.child('business').child(u).child('products').get().val()

    #u = request.user.username
    # Retrieve user's products from Firebase
    user_products = database.child('data').child(u).child('products').get().val()


    # Fetch products from Firebase or any other storage
    context = {
        'products': products,
        'total_products': total_products,
        'subscription_plan': subscription_plan,
        'business': business,
        'user_products': user_products,
    }
    return render(request, 'product/manage_products.html', context)


@login_required
def edit_product(request, product_key):

    user = request.user

    # Retrieve the product from Firebase using the product key
    u = request.user.username
    product = database.child('data').child(u).child('products').child(product_key).get().val()

    if product is None:
        raise Http404("Product does not exist")

    if request.method == 'POST':
        # Retrieve product details from form
        product_name = request.POST.get('name')
        product_price = request.POST.get('price')
        product_description = request.POST.get('description')





        userr = authe.sign_in_with_email_and_password("bw43269@gmail.com", "Thepass@1")

        # Get the authentication token
        id_token = userr['idToken']


        # Save product details to Firebase Database
        product_data = {
            'name': product_name,
            'price': product_price,
            'description': product_description,
            'user_id': user.id
        }

        u = request.user.username

        database.child('data').child(u).child("products").child(product_key).update(product_data)

        messages.success(request, 'Product updated successfully!')
        return redirect('profile')

    context = {
        'product': product,
    }

    return render(request, 'product/edit_product.html', context)


@login_required
def delete_product(request, product_key):
    # Retrieve the product from the database using the product key
    u = request.user.username
    database.child('data').child(u).child('products').child(product_key).remove()

    return redirect('profile')


@login_required
def host_buisness(request):
    user = request.user

    u = request.user.username
    data = database.child("business").child(u).get().val()
    plan = data['subscription_plan']
    buisness_name = data['name']

    if request.method == 'POST':

        banner = request.FILES.get('banner')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        logo = request.FILES.get('logo')
        description = request.POST.get('description')
        about = request.POST.get('about')
        address = request.POST.get('address')
        images = request.FILES.getlist('images[]')


        # Save images to Firebase
        banner_path = f'banner/{user.username}/{banner.name}'
        storage.child(banner_path).put(banner)

        logo_path = f'logo/{user.username}/{logo.name}'
        storage.child(logo_path).put(logo)

        userr = authe.sign_in_with_email_and_password("bw43269@gmail.com", "Thepass@1")

        # Get the authentication token
        id_token = userr['idToken']



        if images:
            image_urls = []
            for image in images:
                image_path = f'images/{user.username}/{image.name}'
                # Upload the image to storage
                storage.child(image_path).put(image)
                # Get the URL of the uploaded image
                image_url = storage.child(image_path).get_url(id_token)
                # Append the image URL to the list
                image_urls.append(image_url)
                # Print the image URL for debugging
                print(f"Image URL: {image_url}")
        else:
            print("No images uploaded.")





        # Save product details to Firebase Database
        buisness = {
            'buisness_name': buisness_name,
            'banner_url': storage.child(banner_path).get_url(id_token) if banner else None,
            'phone': phone,
            'email': email,
            'logo_url': storage.child(logo_path).get_url(id_token) if logo else None,
            'description': description,
            'about': about,
            'address': address,
            'image_urls': image_urls,
            'user_id': user.id
        }

        user.host_buisness = True
        user.save()

        u = request.user.username

        database.child('data').child(u).child('business').set(buisness)

        messages.success(request, 'Buisness listed successfully!')
        return redirect('profile')

    return render(request, 'product/host_buisness.html')


def get_user_business_data(username):
    try:
        data = database.child('data').child(username).child('business').get().val()
        return data
    except Exception as e:
        print("Error retrieving user business data:", e)
        return None




def user_business_display(request, username):
    user = get_object_or_404(CustomUser, username=username)


    #u = get_object_or_404(CustomUser, username=username)
    # Retrieve user's products from Firebase
    user_products = database.child('data').child(user).child('products').get().val()
    #user_business = database.child('data').child(user).child('business').get().val()

    user_business = get_user_business_data(user)


    business = database.child("business").child(user).get().val()
    bussiness = database.child('business').child(user).child('products').get().val()


    context = {
        'user': user,
        'user_products': user_products,
        'user_business': user_business,
        'business': business,
        'bussiness': bussiness,

    }


    return render(request, 'product/buisness/user_business_display.html', context)

@login_required
def create_products(request):#creaTe buisness
    if request.method == 'POST':
        # Get the selected plan from the form
        selected_plan = request.POST.get('selected_plan')
        # Redirect to fill_business_details with the selected plan
        return redirect('fill_business_details', selected_plan=selected_plan)

    plans = [
        {
            'name': 'Free Plan',
            'features': [
                '10 product listing functionality',
                'No image uploads for products',
                'Basic customization options (predefined themes)',
                'About page included in the price distinctions page',

            ],
            'price': 'Free'
        },
        {
            'name': 'Starter Plan',
            'features': [
                '50 product listing limit',
                '1mb image upload capacity each',
                'Additional customization options (more predefined themes and logo)',
                'About page included in the price distinctions page',

            ],
            'price': '$15'
        },
        {
            'name': 'Standard Plan',
            'features': [
                '200 product listing limit',
                '5mb image upload capacity each',
                'Advanced customization options (e.g., custom CSS)',
                'About page included as a separate page',

            ],
            'price': '$30'
        },
        {
            'name': 'Pro Plan',
            'features': [
                'Unlimited product listing',
                'Expanded image upload capacity',
                'Full access to customization options',
                'About page included as a separate page with more advanced pages like gallery etc',
                'No ads on landing page',

            ],
            'price': '$50'
        }
    ]

    return render(request, 'product/create_products.html', {'plans': plans})

@login_required
def product_listing(request):
    user = request.user

    u = request.user.username
    data = database.child("business").child(u).get().val()
    plan = data['subscription_plan']


    totalproduct = user.totalproduct

    # Set plan restrictions
    if plan == 'Free Plan':
        max_products = 10
        max_image_size = 0  # No image allowed
    elif plan == 'Starter Plan':
        max_products = 50
        max_image_size = 1024 * 1024  # 1MB
    elif plan == 'Standard Plan':
        max_products = 200
        max_image_size = 5 * 1024 * 1024  # 5MB
    elif plan == 'Pro Plan':
        max_products = float('inf')  # Unlimited
        max_image_size = None  # Unlimited

    if request.method == 'POST':
        # Retrieve product details from form
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_description = request.POST.get('product_description')
        product_image = request.FILES.get('product_image')

        # Check if user exceeds product limit
        # Implement this check

        # Check image size
        if max_image_size is not None:
            if product_image and product_image.size > max_image_size:
                messages.error(request, f'Image size exceeds the maximum allowed size ({max_image_size} bytes).')
                return redirect('product_listing')



        # Upload product image to Firebase Storage
        if product_image:
            # Customize the path to save the image
            image_path = f'product_images/{product_name}_{user.username}.jpg'
            storage.child(image_path).put(product_image)



        userr = authe.sign_in_with_email_and_password("bw43269@gmail.com", "Thepass@1")

        # Get the authentication token
        id_token = userr['idToken']


        # Save product details to Firebase Database
        product_data = {
            'name': product_name,
            'price': product_price,
            'description': product_description,
            'image_url': storage.child(image_path).get_url(id_token) if product_image else None,
            'user_id': user.id
        }

        u = request.user.username

        database.child('data').child(u).child('products').push(product_data)

        messages.success(request, 'Product added successfully!')
        return redirect('profile')

    return render(request, 'product/product_listing.html', {'max_products': max_products})

@login_required
def fill_business_details(request, selected_plan):

    if request.method == 'POST':
        # Save business details in the database
        name = request.POST.get('name')
        industry = request.POST.get('industry')
        description = request.POST.get('description')
        subscription_plan = request.POST.get('subscription_plan')
        currency = request.POST.get('currency')

        data = {
            'name': name,
            'industry': industry,
            'description': description,
            'subscription_plan': subscription_plan,
            'currency': currency
            }

        u = request.user.username

        # Store user details in the database
        database.child("business").child(u).set(data)


        # Set has_business to true for the current user
        request.user.has_business = True
        request.user.save()
        if subscription_plan == 'Free Plan':
            user = request.user
            plan = subscription_plan
            has_business = True
            total = user.total + 1

            user.plan = plan
            user.has_business = has_business
            user.total = total
            user.save()

            return redirect('profile')
        else:
            return redirect('payment', selected_plan=subscription_plan, currency=currency)
         # Redirect to payment page after filling business details


    #return render(request, 'product/fill_business_details.html')
    return render(request, 'product/fill_business_details.html', {'selected_plan': selected_plan})


@login_required
def payment_plan_starter(request):
    user = request.user
    plan = 'Starter Plan'
    has_business = True
    total = user.total + 1

    user.plan = plan
    user.has_business = has_business
    user.total = total
    user.save()

    product_data = {
            'username': user_name,
            'referral': referral,
            'email': email,
        }


    database.child('referral').child('starter').set(product_data)


    return render(request, 'payment/payment_starter.html')

@login_required
def payment_plan_standard(request):
    user = request.user
    plan = 'Standard Plan'
    has_business = True
    total = user.total + 1

    user.plan = plan
    user.has_business = has_business
    user.total = total
    user.save()

    product_data = {
            'username': user_name,
            'referral': referral,
            'email': email,
        }


    database.child('referral').child('standard').set(product_data)

    return render(request, 'payment/payment_standard.html')

@login_required
def payment_plan_pro(request):
    user = request.user
    plan = 'Pro Plan'
    has_business = True
    total = user.total + 1

    user.plan = plan
    user.has_business = has_business
    user.total = total
    user.save()

    product_data = {
            'username': user_name,
            'referral': referral,
            'email': email,
        }


    database.child('referral').child('pro').set(product_data)

    return render(request, 'payment/payment_pro.html')


@login_required
def payment(request, selected_plan, currency):
    # Retrieve the selected plan from the database or session

    tx_ref = f"{selected_plan.lower()}-{''.join(random.choices('0123456789', k=6))}"
    amount = 0

    # Calculate amount based on selected plan and currency
    # This is just a placeholder, you need to replace it with actual calculation
    if selected_plan.lower() == 'free plan':
        pass
    elif selected_plan.lower() == 'starter plan':
        if currency == 'GBP':
            amount = 10  # Placeholder value
        elif currency == 'NGN':
            amount = 20000  # Placeholder value
        elif currency == 'USD':
            amount = 15  # Placeholder value
        else:
            pass
    elif selected_plan.lower() == 'standard plan':
        if currency == 'GBP':
            amount = 25  # Placeholder value
        elif currency == 'NGN':
            amount = 50000  # Placeholder value
        elif currency == 'USD':
            amount = 30  # Placeholder value
        else:
            pass
    elif selected_plan.lower() == 'pro plan':
        if currency == 'GBP':
            amount = 40  # Placeholder value
        elif currency == 'NGN':
            amount = 80000  # Placeholder value
        elif currency == 'USD':
            amount = 50  # Placeholder value
        else:
            pass
    else:
        pass


    # Generate redirect_url
    if selected_plan == 'Free Plan':
        pass
    elif selected_plan == 'Starter Plan':
        redirect_url = 'https://techinnovomshowcase.pythonanywhere.com/payment/selected_plan/payment_starter'
    elif selected_plan == 'Standard Plan':
        redirect_url = 'https://techinnovomshowcase.pythonanywhere.com/payment/selected_plan/payment_standard'
    elif selected_plan == 'Pro Plan':
        redirect_url = 'https://techinnovomshowcase.pythonanywhere.com/payment/selected_plan/payment_pro'
    else:
        pass

    u = request.user.username
    # Get customer name, email, and token from session or form submission data
    data = database.child("business").child(u).get().val()
    business_name = data['name']


    customer_email = request.user.email  # Placeholder, replace with actual value
    meta_token = request.user.username


    # You can perform additional logic here, such as fetching the price based on the plan

    return render(request, 'product/payment.html', {
        'selected_plan': selected_plan,
        'tx_ref': tx_ref,
        'amount': amount,
        'redirect_url': redirect_url,
        'customer_email': customer_email,
        'meta_token': meta_token,
        'selected_plan': selected_plan,
        'currency': currency,
        'business_name': business_name
    })


def upload_form(request):
    if request.method == 'POST':
        form = UserUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            return redirect('payment_page', pk=instance.pk)
    else:
        form = UserUploadForm()
    return render(request, 'ads/upload_form.html', {'form': form})

def payment_page(request, pk):
    user_upload = UserUpload.objects.get(pk=pk)
    # Calculate total amount based on days chosen

    currency = user_upload.currency

    if currency == 'USD':
        total_amount = f'${user_upload.days * 1}'
        tamount = user_upload.days * 1

    if currency == 'EUR':
        total_amount = f'€{user_upload.days * 1}'
        tamount = user_upload.days * 1
    if currency == 'GBP':
        total_amount = f'£{user_upload.days * 1}'
        tamount = user_upload.days * 1
    if currency == 'NGN':
        total_amount = f'₦{user_upload.days * 300}'
        tamount = user_upload.days * 300
    else:
        pass

    tx_ref = f"ads-{''.join(random.choices('0123456789', k=6))}"

    redirect_url = reverse('payment_process', kwargs={'pk': pk})

    return render(request, 'ads/payment_page.html', {'user_upload': user_upload, 'total_amount': total_amount, 'tamount': tamount, 'currency': currency, 'tx_ref': tx_ref, 'redirect_url': redirect_url})


def payment_process(request, pk):
    if request.method == 'POST':
        user_upload_id = pk
        try:
            user_upload = UserUpload.objects.get(pk=user_upload_id)
        except UserUpload.DoesNotExist:
            messages.error(request, 'Ad not found.')
            return redirect('upload_form')

        # Process payment here

        # If payment is successful
        user_upload.is_live = True
        user_upload.calculate_end_date()  # Calculate end date
        user_upload.save()
        messages.success(request, 'Payment successful!')
        return redirect('success_page')

    else:
        messages.error(request, 'Invalid request.')
        return redirect('upload_form')



def success_page(request):
    return render(request, 'ads/success_page.html')





@login_required
def upgrade(request):
    u = request.user.username
    data = database.child("business").child(u).get().val()
    plan = data['subscription_plan']


    currency = data['currency']


    if request.method == 'POST':
        # Get the selected plan from the form
        selected_plan = request.POST.get('selected_plan')
        # Redirect to fill_business_details with the selected plan
        return redirect('upgrade_payment', selected_plan=selected_plan, currency=currency)


    if plan == 'Free Plan':
        plans = [

            {
                'name': 'Starter Plan',
                'features': [
                    '50 product listing limit',
                    '1mb image upload capacity each',
                    'Additional customization options (more predefined themes and logo)',
                    'About page included in the price distinctions page',

                ],
                'price': '$20'
            },
            {
                'name': 'Standard Plan',
                'features': [
                    '200 product listing limit',
                    '5mb image upload capacity each',
                    'Advanced customization options (e.g., custom CSS)',
                    'About page included as a separate page',

                ],
                'price': '$40'
            },
            {
                'name': 'Pro Plan',
                'features': [
                    'Unlimited product listing',
                    'Expanded image upload capacity',
                    'Full access to customization options',
                    'About page included as a separate page with more advanced pages like gallery etc',
                    'No ads on landing page',

                ],
                'price': '$50'
            }
        ]
    elif plan == 'Starter Plan':
        plans = [

            {
                'name': 'Standard Plan',
                'features': [
                    '200 product listing limit',
                    '5mb image upload capacity each',
                    'Advanced customization options (e.g., custom CSS)',
                    'About page included as a separate page',

                ],
                'price': '$30'
            },
            {
                'name': 'Pro Plan',
                'features': [
                    'Unlimited product listing',
                    'Expanded image upload capacity',
                    'Full access to customization options',
                    'About page included as a separate page with more advanced pages like gallery etc',
                    'No ads on landing page',

                ],
                'price': '$45'
            }
        ]
    elif plan == 'Standard Plan':
        plans = [

            {
                'name': 'Pro Plan',
                'features': [
                    'Unlimited product listing',
                    'Expanded image upload capacity',
                    'Full access to customization options',
                    'About page included as a separate page with more advanced pages like gallery etc',
                    'No ads on landing page',

                ],
                'price': '$40'
            }
        ]
    elif plan == 'Pro Plan':
        return redirect('profile')

    else:
        pass



    return render(request, 'product/upgrade/upgrade.html', {'plans': plans})



@login_required
def upgrade_payment(request, selected_plan, currency):
    # Retrieve the selected plan from the database or session
    u = request.user.username
    data = database.child("business").child(u).get().val()
    plan = data['subscription_plan']


    tx_ref = f"{currency.lower()}-{''.join(random.choices('0123456789', k=6))}"
    amount = 0

    # Calculate amount based on selected plan and currency
    # This is just a placeholder, you need to replace it with actual calculation
    if selected_plan.lower() == 'free plan':
        pass
    elif selected_plan.lower() == 'starter plan':

        if currency == 'GBP':
            amount = 13  # Placeholder value
        elif currency == 'NGN':
            amount = 26000  # Placeholder value
        elif currency == 'USD':
            amount = 20  # Placeholder value
        else:
            pass
    elif selected_plan.lower() == 'standard plan':
        if plan.lower() == 'free plan':
            if currency == 'GBP':
                amount = 33  # Placeholder value
            elif currency == 'NGN':
                amount = 66000  # Placeholder value
            elif currency == 'USD':
                amount = 40  # Placeholder value
            else:
                pass
        elif plan.lower() == 'starter plan':
            if currency == 'GBP':
                amount = 25  # Placeholder value
            elif currency == 'NGN':
                amount = 50000  # Placeholder value
            elif currency == 'USD':
                amount = 30  # Placeholder value
            else:
                pass
        else:
            pass


    elif selected_plan.lower() == 'pro plan':
        if plan.lower() == 'free plan':
            if currency == 'GBP':
                amount = 40  # Placeholder value
            elif currency == 'NGN':
                amount = 80000  # Placeholder value
            elif currency == 'USD':
                amount = 50  # Placeholder value
            else:
                pass

        elif plan.lower() == 'starter plan':
            if currency == 'GBP':
                amount = 36  # Placeholder value
            elif currency == 'NGN':
                amount = 72000  # Placeholder value
            elif currency == 'USD':
                amount = 45  # Placeholder value
            else:
                pass

        elif plan.lower() == 'standard plan':
            if currency == 'GBP':
                amount = 32  # Placeholder value
            elif currency == 'NGN':
                amount = 64000  # Placeholder value
            elif currency == 'USD':
                amount = 40  # Placeholder value
            else:
                pass

        else:
            pass




    else:
        pass


    # Generate redirect_url
    if selected_plan == 'Free Plan':
        pass
    elif selected_plan == 'Starter Plan':
        redirect_url = 'https://techinnovomshowcase.pythonanywhere.com/upgrade/payment/selected_plan/payment_starter'
    elif selected_plan == 'Standard Plan':
        redirect_url = 'https://techinnovomshowcase.pythonanywhere.com/upgrade/payment/selected_plan/payment_standard'
    elif selected_plan == 'Pro Plan':
        redirect_url = 'https://techinnovomshowcase.pythonanywhere.com/upgrade/payment/selected_plan/payment_pro'
    else:
        pass

    u = request.user.username
    # Get customer name, email, and token from session or form submission data
    data = database.child("business").child(u).get().val()
    business_name = data['name']


    customer_email = request.user.email  # Placeholder, replace with actual value
    meta_token = request.user.username


    # You can perform additional logic here, such as fetching the price based on the plan

    return render(request, 'product/upgrade/payment.html', {
        'selected_plan': selected_plan,
        'tx_ref': tx_ref,
        'amount': amount,
        'redirect_url': redirect_url,
        'customer_email': customer_email,
        'meta_token': meta_token,
        'selected_plan': selected_plan,
        'currency': currency,
        'business_name': business_name
    })




@login_required
def upgrade_payment_plan_starter(request):
    u = request.user.username
    data = database.child("business").child(u).get().val()
    plan = data['subscription_plan']
    referral = user.ref


    product_data = {
            'username': user_name,
            'referral': referral,
            'email': email,
        }


    database.child('referral').child('starter').set(product_data)



    ddata ={
        'currency': data['currency'],
        'description': data['description'],
        'industry': data['industry'],
        'name': data['name'],
        'subscription_plan': 'Starter Plan',

        }

    database.child('business').child(u).update(ddata)


    return render(request, 'upgrade/payment/payment_starter.html')

@login_required
def upgrade_payment_plan_standard(request):
    u = request.user.username
    data = database.child("business").child(u).get().val()
    plan = data['subscription_plan']
    referral = user.ref


    product_data = {
            'username': user_name,
            'referral': referral,
            'email': email,
        }


    database.child('referral').child('standard').set(product_data)



    ddata ={
        'currency': data['currency'],
        'description': data['description'],
        'industry': data['industry'],
        'name': data['name'],
        'subscription_plan': 'Standard Plan',

        }

    database.child('business').child(u).update(ddata)

    return render(request, 'upgrade/payment/payment_standard.html')

@login_required
def upgrade_payment_plan_pro(request):
    u = request.user.username
    data = database.child("business").child(u).get().val()
    plan = data['subscription_plan']
    referral = user.ref


    product_data = {
            'username': user_name,
            'referral': referral,
            'email': email,
        }


    database.child('referral').child('pro').set(product_data)



    ddata ={
        'currency': data['currency'],
        'description': data['description'],
        'industry': data['industry'],
        'name': data['name'],
        'subscription_plan': 'Pro Plan',

        }

    database.child('business').child(u).update(ddata)

    return render(request, 'upgrade/payment/payment_pro.html')


def business_list(request):
    # Retrieve all users with host_business set to True
    businesses = CustomUser.objects.filter(host_buisness=True)
    businesses = list(businesses)
    # Randomize the list of businesses
    random.shuffle(businesses)

    business_details = []
    for business in businesses:
        username = business.username

        user_business = get_user_business_data(username)
        business_detail = database.child("business").child(username).get().val()
        business_details.append({'username': username, 'business_detail': business_detail, 'user_business': user_business})


    return render(request, 'product/buisness/business_list.html',
                  {'business_details': business_details})

