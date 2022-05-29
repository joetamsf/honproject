from turtle import update
from django.urls import path

from .views import customer_login, validate_token, create_order, get_my_order, delete_my_order, update_password, create_account

urlpatterns = [
    path('customers/create_account', create_account),
    path('customers/login', customer_login),
    path('customers/verify_token', validate_token),
    path('customers/new_order', create_order),
    path('customers/my_orders', get_my_order),
    path('customers/cancel_order', delete_my_order),
    path('customers/update_password', update_password)
]