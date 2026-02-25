from django.urls import path
from . import views

urlpatterns = [
    path('plan-my-event/', views.plan_my_event, name='plan_my_event'),
    path('request-quote/', views.request_quote, name='request_quote'),
    path('contact/', views.contact, name='contact'),
    path('verify-stripe-payment/', views.verify_stripe_payment, name='verify_stripe_payment'),
    path('verify-paystack-payment/', views.verify_paystack_payment, name='verify_paystack_payment'),
    path('chatbot/', views.chatbot, name='chatbot'),
]
