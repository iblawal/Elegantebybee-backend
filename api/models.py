from django.db import models


class PlanMyEvent(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    event_occasion = models.CharField(max_length=200)
    event_location = models.CharField(max_length=200)
    event_date = models.DateField()
    venue = models.CharField(max_length=200, blank=True)
    theme_of_decor = models.CharField(max_length=200, blank=True)
    expected_guests = models.CharField(max_length=50, blank=True)
    budget = models.CharField(max_length=100, blank=True)
    food_nigerian_dishes = models.BooleanField(default=False)
    food_oriental_dishes = models.BooleanField(default=False)
    food_continental_dishes = models.BooleanField(default=False)
    food_desserts = models.BooleanField(default=False)
    food_finger_foods = models.BooleanField(default=False)
    food_other = models.BooleanField(default=False)
    drinks_alcoholic_cocktails = models.BooleanField(default=False)
    drinks_non_alcoholic_cocktails = models.BooleanField(default=False)
    drinks_alcoholic = models.BooleanField(default=False)
    drinks_non_alcoholic = models.BooleanField(default=False)
    drinks_red_wine = models.BooleanField(default=False)
    drinks_champagne = models.BooleanField(default=False)
    drinks_other = models.BooleanField(default=False)
    beverages_tea = models.BooleanField(default=False)
    beverages_coffee = models.BooleanField(default=False)
    beverages_cappuccino = models.BooleanField(default=False)
    beverages_hot_chocolate = models.BooleanField(default=False)
    beverages_other = models.BooleanField(default=False)
    service_event_coordination = models.BooleanField(default=False)
    service_marquee_rental = models.BooleanField(default=False)
    service_photography = models.BooleanField(default=False)
    service_videography = models.BooleanField(default=False)
    service_live_band = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event_occasion}"


class RequestQuote(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service}"


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"


class Payment(models.Model):
    PROVIDER_CHOICES = [('stripe', 'Stripe'), ('paystack', 'Paystack')]
    STATUS_CHOICES = [('successful', 'Successful'), ('failed', 'Failed'), ('pending', 'Pending')]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    reference = models.CharField(max_length=200, unique=True)
    package = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount} {self.currency} via {self.provider}"


class ChatMessage(models.Model):
    ROLE_CHOICES = [('user', 'User'), ('assistant', 'Assistant')]

    session_id = models.CharField(max_length=200, db_index=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.session_id} - {self.role} - {self.created_at}"