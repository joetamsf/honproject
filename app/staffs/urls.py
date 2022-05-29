from django.urls import path

from .views import staffs_index, show_all_staffs, add_new_staff, get_all_orders, assign_order, staff_login, update_password

urlpatterns = [
    path('staffs', staffs_index),
    path('staffs/show_all', show_all_staffs),
    path('staffs/add', add_new_staff),
    path('staffs/show_all_orders', get_all_orders),
    path('staffs/assign_staff', assign_order),
    path('staffs/login', staff_login),
    path('staffs/update_password', update_password)
]