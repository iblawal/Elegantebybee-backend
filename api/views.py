import json
import os
from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .serializers import PlanMyEventSerializer, RequestQuoteSerializer, ContactSerializer
from .models import Payment, ChatMessage
import stripe
import urllib.request
import urllib.parse


BUSINESS_CONTEXT = """You are the EleganteBee AI Assistant — a sophisticated, warm, and knowledgeable virtual concierge for EleganteBee Services, a luxury event planning and coordination company.

COMPANY OVERVIEW:
- Full name: ELEGANTE BEE SERVICES
- Founded: 2014
- Tagline: "Elegance is a language — and every event is a story waiting to be told."
- Locations: Maryland, USA (3600 Leonardtown Rd #203, Waldorf, MD 20601) & Lagos, Nigeria

FOUNDER:
- Name: Mrs Bukola Zubair Lawal — Founder & CEO
- Quote: "Our passion is elegance. Our tool is excellence."

SERVICES:
1. Event Planning & Coordination — Full-service from concept to execution
2. Birthday Shoutouts — $75 (US)
3. Fashion Influencing — Style inspiration and brand collaborations
4. Event Venue Scouting
5. Decoration & Styling
6. Entertainment & Activities
7. Photography & Videography
8. Media Coverage
9. Event Blogging
10. Brand Activations

US PRICING:
- 100-250 guests: $700
- 251+ guests: $1,000
- Red Carpet Experience: $175
- Event Confirmations: $100
- Birthday Shoutout: $75

NIGERIA: Custom Naira pricing — WhatsApp +234 916 779 6186

CONTACT:
- Email: elegantebybee@gmail.com
- US Phone/WhatsApp: +1 240-604-0025
- Nigeria WhatsApp: +234 916 779 6186

SOCIAL: Instagram/TikTok @elegantebybee | Facebook: elegant_by_bee

BOOKING: Discovery Call → Custom Proposal (5-7 days) → Contract → Execution

STATS: 300+ events, 5+ years, 200+ happy clients, 5-star rated

YOUR PERSONALITY: You are refined, warm, and professional like a luxury hotel concierge. Keep responses concise (2-4 sentences). Always guide clients toward booking a discovery call or requesting a quote. For Nigeria pricing always direct to WhatsApp +234 916 779 6186."""


@api_view(['POST'])
def chatbot(request):
    try:
        data = request.data
        messages = data.get('messages', [])
        session_id = data.get('session_id', 'anonymous')
        user_message = data.get('user_message', '')

        if not messages or not user_message:
            return Response(
                {'success': False, 'message': 'Messages and user_message are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Rate limiting — max 20 messages per session per hour
        one_hour_ago = timezone.now() - timedelta(hours=1)
        recent_count = ChatMessage.objects.filter(
            session_id=session_id,
            created_at__gte=one_hour_ago,
            role='user'
        ).count()

        if recent_count >= 20:
            return Response(
                {'success': False, 'message': 'Message limit reached. Contact us at elegantebybee@gmail.com'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Save user message
        ChatMessage.objects.create(
            session_id=session_id,
            role='user',
            content=user_message
        )

        # Get Gemini API key
        gemini_key = os.environ.get('GEMINI_API_KEY', '')
        if not gemini_key:
            return Response(
                {'success': False, 'message': 'AI service temporarily unavailable. Please contact us directly.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Build conversation history for Gemini
        gemini_contents = []
        
        # Add system context as first user message
        gemini_contents.append({
            "role": "user",
            "parts": [{"text": f"SYSTEM INSTRUCTIONS:\n{BUSINESS_CONTEXT}\n\nNow respond to the following conversation as the EleganteBee AI Assistant."}]
        })
        gemini_contents.append({
            "role": "model",
            "parts": [{"text": "Understood. I am the EleganteBee AI Assistant, ready to help with all inquiries about EleganteBee Services."}]
        })

        # Add conversation history
        for msg in messages[:-1]:  # all except the last (current) message
            role = "user" if msg["role"] == "user" else "model"
            gemini_contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })

        # Add current user message
        gemini_contents.append({
            "role": "user",
            "parts": [{"text": user_message}]
        })

        # Call Gemini API
        url =url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}"
        payload = json.dumps({
            "contents": gemini_contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000,
            }
        }).encode('utf-8')

        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))

        reply = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')

        if not reply:
            return Response(
                {'success': False, 'message': 'No response from AI'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Save assistant reply
        ChatMessage.objects.create(
            session_id=session_id,
            role='assistant',
            content=reply
        )

        return Response({
            'success': True,
            'reply': reply,
            'session_id': session_id
        }, status=status.HTTP_200_OK)

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"[GEMINI ERROR]: {e.code} - {error_body}")
        return Response(
            {'success': False, 'message': 'AI service error. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        print(f"[CHATBOT ERROR]: {e}")
        return Response(
            {'success': False, 'message': 'Something went wrong. Contact us at elegantebybee@gmail.com'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def plan_my_event(request):
    serializer = PlanMyEventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        try:
            send_mail(
                subject='New Plan My Event Submission',
                message=f"Name: {data['first_name']} {data['last_name']}\nEmail: {data['email']}\nPhone: {data['phone']}\nEvent: {data['event_occasion']}\nLocation: {data['event_location']}\nDate: {data['event_date']}\nGuests: {data['expected_guests']}\nMessage: {data['message']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFY_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"[EMAIL ERROR - plan_my_event]: {e}")
        return Response({'success': True, 'message': 'Your event plan has been submitted successfully!'}, status=status.HTTP_201_CREATED)
    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def request_quote(request):
    serializer = RequestQuoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        try:
            send_mail(
                subject='New Request Quote Submission',
                message=f"Name: {data['first_name']} {data['last_name']}\nEmail: {data['email']}\nPhone: {data['phone']}\nService: {data['service']}\nMessage: {data['message']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFY_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"[EMAIL ERROR - request_quote]: {e}")
        return Response({'success': True, 'message': 'Your quote request has been submitted successfully!'}, status=status.HTTP_201_CREATED)
    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def contact(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        try:
            send_mail(
                subject='New Contact Form Submission',
                message=f"Name: {data['first_name']} {data['last_name']}\nEmail: {data['email']}\nSubject: {data['subject']}\nMessage: {data['message']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFY_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"[EMAIL ERROR - contact]: {e}")
        return Response({'success': True, 'message': 'Your message has been sent successfully!'}, status=status.HTTP_201_CREATED)
    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


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
                    message=f"Name: {payment.name}\nEmail: {payment.email}\nPackage: {payment.package}\nAmount: ${payment.amount}\nReference: {payment.reference}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.NOTIFY_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"[EMAIL ERROR - stripe]: {e}")
            return Response({'success': True, 'message': 'Payment verified!'}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': 'Payment not completed'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_paystack_payment(request):
    try:
        data = request.data
        payment = Payment.objects.create(
            name=data.get('name', 'Customer'),
            email=data.get('email'),
            amount=data.get('amount'),
            currency='NGN',
            provider='paystack',
            status='successful',
            reference=data.get('reference'),
        )
        try:
            send_mail(
                subject='New Paystack Payment Received!',
                message=f"Name: {payment.name}\nEmail: {payment.email}\nAmount: ₦{payment.amount}\nReference: {payment.reference}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFY_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"[EMAIL ERROR - paystack]: {e}")
        return Response({'success': True, 'message': 'Payment recorded!'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)