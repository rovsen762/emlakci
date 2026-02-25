from .views import register,user_login,forgot_password,verify_forgot_password_otp,reset_password,user_logout,verify_register_otp,\
    customer_list, customer_details,profile,customer_grid

from django.urls import path

urlpatterns = [
    path('register/', register, name='register'),
    path('verify-register-otp/', verify_register_otp, name='verify-register-otp'),
    path('login/', user_login, name='login'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('verify-forgot-password-otp/', verify_forgot_password_otp, name='verify-forgot-password-otp'),
    path('reset-password/', reset_password, name='reset-password'),
    path('logout/', user_logout, name='logout'),
    
    path('customer-list/', customer_list, name='customer-list'),
    path('customer-grid/', customer_grid, name='customer-grid'),
    path('customer-details/<int:customer_id>/', customer_details, name='customer-details'),
    path('profile/', profile, name='profile'),
]