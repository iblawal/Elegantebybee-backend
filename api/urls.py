from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [
    path('plan-my-event/', views.plan_my_event, name='plan-my-event'),
    path('request-quote/', views.request_quote, name='request-quote'),
    path('contact/', views.contact, name='contact'),
    path('verify-stripe-payment/', views.verify_stripe_payment, name='verify-stripe-payment'),
    path('verify-paystack-payment/', views.verify_paystack_payment, name='verify-paystack-payment'),
]
