# urls.py (inside your authentication app)

from django.urls import path
from . import views
from django.conf.urls import handler404
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    #path('forgot/', views.forgot, name='forgot'),

    #path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('manage-products/', views.manage_products, name='manage_products'),
    path('create-products/', views.create_products, name='create_products'),

    path('product-listing/', views.product_listing, name='product_listing'),
    path('host-buisness/', views.host_buisness, name='host_buisness'),
    path('edit-product/<str:product_key>/', views.edit_product, name='edit_product'),
    path('delete-product/<str:product_key>/', views.delete_product, name='delete_product'),


    path('business/<str:username>/', views.user_business_display, name='user_business_display'),


    path('business/', views.business_list, name='business_list'),



    #path('manage-business/', views.manage_business, name='manage_business'),
    #path('take-business-live/', views.take_business_live, name='take_business_live'),
    #path('display-business/<int:business_id>/', views.display_business, name='display_business'),

    #path('fill-business-details/', views.fill_business_details, name='fill_business_details'),
    path('fill-business-details/<str:selected_plan>/', views.fill_business_details, name='fill_business_details'),

    #path('payment/', views.payment, name='payment'),
    path('payment/<str:selected_plan>/<str:currency>/', views.payment, name='payment'),

    path('payment/selected_plan/payment_starter/', views.payment_plan_starter, name='payment_starter'),
    path('payment/selected_plan/payment_standard/', views.payment_plan_standard, name='payment_standard'),
    path('payment/selected_plan/payment_pro/', views.payment_plan_pro, name='payment_pro'),

    path('upload_ad/', views.upload_form, name='upload_form'),
    path('payment/<int:pk>/', views.payment_page, name='payment_page'),
    path('payment/process/<int:pk>/', views.payment_process, name='payment_process'),
    path('success/', views.success_page, name='success_page'),

    path('', views.home, name='home'),




    path('upgrade/', views.upgrade, name='upgrade'),
    path('upgrade/<str:selected_plan>/<str:currency>/', views.upgrade_payment, name='upgrade_payment'),



    path('upgrade/payment/selected_plan/payment_starter/', views.upgrade_payment_plan_starter, name='payment_starter'),
    path('upgrade/payment/selected_plan/payment_standard/', views.upgrade_payment_plan_standard, name='payment_standard'),
    path('upgrade/payment/selected_plan/payment_pro/', views.upgrade_payment_plan_pro, name='payment_pro'),


]


handler404 = views.custom_404
