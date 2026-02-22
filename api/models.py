from django.db import models

class PlanMyEvent(models.Model):
    # Personal Info
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # Event Info
    event_occasion = models.CharField(max_length=255)
    event_location = models.CharField(max_length=255)
    event_date = models.DateField()
    venue = models.CharField(max_length=255, blank=True)
    theme_of_decor = models.CharField(max_length=255, blank=True)
    expected_guests = models.IntegerField(null=True, blank=True)
    budget = models.CharField(max_length=100, blank=True)

    # Food
    food_nigerian_dishes = models.BooleanField(default=False)
    food_oriental_dishes = models.BooleanField(default=False)
    food_continental_dishes = models.BooleanField(default=False)
    food_desserts = models.BooleanField(default=False)
    food_finger_foods = models.BooleanField(default=False)
    food_other = models.BooleanField(default=False)

    # Drinks
    drinks_alcoholic_cocktails = models.BooleanField(default=False)
    drinks_non_alcoholic_cocktails = models.BooleanField(default=False)
    drinks_alcoholic = models.BooleanField(default=False)
    drinks_non_alcoholic = models.BooleanField(default=False)
    drinks_red_wine = models.BooleanField(default=False)
    drinks_champagne = models.BooleanField(default=False)
    drinks_other = models.BooleanField(default=False)

    # Beverages
    beverages_tea = models.BooleanField(default=False)
    beverages_coffee = models.BooleanField(default=False)
    beverages_cappuccino = models.BooleanField(default=False)
    beverages_hot_chocolate = models.BooleanField(default=False)
    beverages_other = models.BooleanField(default=False)

    # Other Services
    service_event_coordination = models.BooleanField(default=False)
    service_marquee_rental = models.BooleanField(default=False)
    service_photography = models.BooleanField(default=False)
    service_videography = models.BooleanField(default=False)
    service_live_band = models.BooleanField(default=False)

    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Plan My Event'
        verbose_name_plural = 'Plan My Event Submissions'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event_occasion}"


class RequestQuote(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Request Quote'
        verbose_name_plural = 'Request Quote Submissions'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service}"


class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact'
        verbose_name_plural = 'Contact Submissions'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
    

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ]

    PAYMENT_PROVIDER = [
        ('stripe', 'Stripe'),
        ('paystack', 'Paystack'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    provider = models.CharField(max_length=20, choices=PAYMENT_PROVIDER)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    reference = models.CharField(max_length=255, unique=True)
    package = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f"{self.name} - {self.provider} - {self.amount} - {self.status}"
