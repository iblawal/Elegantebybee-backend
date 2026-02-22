from django.contrib import admin
from .models import PlanMyEvent, RequestQuote, Contact
from .models import PlanMyEvent, RequestQuote, Contact, Payment


@admin.register(PlanMyEvent)
class PlanMyEventAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'event_occasion', 'event_date', 'created_at']
    list_filter = ['event_date', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'event_occasion']
    readonly_fields = ['created_at']


@admin.register(RequestQuote)
class RequestQuoteAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'service', 'created_at']
    list_filter = ['created_at']
    search_fields = ['first_name', 'last_name', 'email', 'service']
    readonly_fields = ['created_at']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'subject', 'created_at']
    list_filter = ['created_at']
    search_fields = ['first_name', 'last_name', 'email', 'subject']
    readonly_fields = ['created_at']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'amount', 'currency', 'provider', 'status', 'created_at']
    list_filter = ['provider', 'status', 'created_at']
    search_fields = ['name', 'email', 'reference']
    readonly_fields = ['created_at']