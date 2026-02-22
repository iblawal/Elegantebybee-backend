from rest_framework import serializers
from .models import PlanMyEvent, RequestQuote, Contact
from .models import PlanMyEvent, RequestQuote, Contact, Payment


class PlanMyEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanMyEvent
        fields = '__all__'

    def validate_expected_guests(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Number of guests cannot be negative.")
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value.lower().strip()


class RequestQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestQuote
        fields = '__all__'

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value.lower().strip()


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value.lower().strip()
    
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'