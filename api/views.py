from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .serializers import PlanMyEventSerializer, RequestQuoteSerializer, ContactSerializer
from .models import Payment
import stripe


@api_view(['POST'])
def plan_my_event(request):
    serializer = PlanMyEventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        try:
            send_mail(
                subject='New Plan My Event Submission',
                message=f"""
New event planning request received!

Name: {data['first_name']} {data['last_name']}
Email: {data['email']}
Phone: {data['phone']}
Event: {data['event_occasion']}
Location: {data['event_location']}
Date: {data['event_date']}
Venue: {data['venue']}
Guests: {data['expected_guests']}
Budget: {data['budget']}
Message: {data['message']}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFY_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"[EMAIL ERROR - plan_my_event]: {e}")

        return Response(
            {'success': True, 'message': 'Your event plan has been submitted successfully! We will get back to you shortly.'},
            status=status.HTTP_201_CREATED
        )
    return Response(
        {'success': False, 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
def request_quote(request):
    serializer = RequestQuoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        try:
            send_mail(
                subject='New Request Quote Submission',
                message=f"""
New quote request received!

Name: {data['first_name']} {data['last_name']}
Email: {data['email']}
Phone: {data['phone']}
Service: {data['service']}
Message: {data['message']}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFY_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"[EMAIL ERROR - request_quote]: {e}")

        return Response(
            {'success': True, 'message': 'Your quote request has been submitted successfully! We will get back to you shortly.'},
            status=status.HTTP_201_CREATED
        )
    return Response(
        {'success': False, 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
def contact(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        try:
            send_mail(
                subject='New Contact Form Submission',
                message=f"""
New contact message received!

Name: {data['first_name']} {data['last_name']}
Email: {data['email']}
Subject: {data['subject']}
Message: {data['message']}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFY_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"[EMAIL ERROR - contact]: {e}")

        return Response(
            {'success': True, 'message': 'Your message has been sent successfully! We will get back to you shortly.'},
            status=status.HTTP_201_CREATED
        )
    return Response(
        {'success': False, 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
def verify_stripe_payment(request):
    try:
        data = request.data
        session_id = data.get('session_id')

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == 'paid':
            payment = Payment.objects.create(
                name=data.get('name', 'Customer'),
                email=session.customer_email,
                amount=session.amount_total / 100,
                currency=session.currency.upper(),
                provider='stripe',
                status='successful',
                reference=session_id,
                package=data.get('package', ''),
            )
            try:
                send_mail(
                    subject='New Stripe Payment Received!',
                    message=f"""
New payment received!

Name: {payment.name}
Email: {payment.email}
Package: {payment.package}
Amount: ${payment.amount} {payment.currency}
Provider: Stripe
Reference: {payment.reference}
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.NOTIFY_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"[EMAIL ERROR - verify_stripe]: {e}")

            return Response(
                {'success': True, 'message': 'Payment verified successfully!'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'success': False, 'message': 'Payment not completed'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response(
            {'success': False, 'message': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def verify_paystack_payment(request):
    try:
        data = request.data
        reference = data.get('reference')
        email = data.get('email')
        amount = data.get('amount')
        name = data.get('name', 'Customer')

        payment = Payment.objects.create(
            name=name,
            email=email,
            amount=amount,
            currency='NGN',
            provider='paystack',
            status='successful',
            reference=reference,
        )
        try:
            send_mail(
                subject='New Paystack Payment Received!',
                message=f"""
New payment received!

Name: {payment.name}
Email: {payment.email}
Amount: ₦{payment.amount}
Provider: Paystack
Reference: {payment.reference}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFY_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"[EMAIL ERROR - verify_paystack]: {e}")

        return Response(
            {'success': True, 'message': 'Payment recorded successfully!'},
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {'success': False, 'message': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )