import datetime
import random

import signal

import paypalrestsdk as paypalrestsdk
import stripe

from django.contrib.auth.hashers import make_password
from django.db.models import Q

from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.cache import cache

from paypal.standard.forms import PayPalPaymentsForm
from rest_framework import status, request

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_swagger.views import get_swagger_view
from twilio.rest import Client

from AuthenticationSystem import settings
# from application.models import UserInfo, StripPayment
from application.models import UserInfo, UserOTP
from application.serializers import UserSerializer, ActionsUserSerializer, ChangePasswordSerializer, SendOTP

schema_view = get_swagger_view(title='Pastebin API')

stripe.api_key = settings.Stripe_Secret_Key

PAYPAL_CLIENT_ID = "AflenAaDF0G1OCP7Bn4rGS3pWNOOIav91TLPla1730Cao07LqTOHAFoN0dFzQNPuojL0lnaUIbz9YTuk"
PAYPAL_CLIENT_SECRET = "EMBzQiMGAQywlzDPHGrRXoo-kxYGJGL1KiPUT0JCHT85CrloYLh2-b5DCOtYbq7aSdNOvo6wrGCmr-ab"

paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": PAYPAL_CLIENT_ID,
    "client_secret": PAYPAL_CLIENT_SECRET})


class OTP(APIView):
    def post(self, request):
        serializer = SendOTP(data=request.data)
        if serializer.is_valid():
            OTP = ""
            for i in range(0, 4):
                digit = random.randint(0, 9)
                OTP = OTP + str(digit)

            account_sid = 'AC5f11c2ec41e52e02d06c1cc5a2f398cd'
            auth_token = '79a8475f07daa0faae86409cb8d22b0f'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f'Hey Your verification code is {OTP}\nThankyou for trust on us.',
                from_=serializer.validated_data.get("mobile_no"),
                to='+919589957396'
            )
            UserOTP.objects.create(user=serializer.validated_data.get("email"), otp=OTP)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistration(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = UserOTP.objects.filter(user=serializer.validated_data.get("email"))
            otp = serializer.validated_data.get('otp')
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            for i in data:
                if otp == i.otp:
                    user = UserOTP.objects.get(user=i.user)
                    user.status = False
                    user.save()
                    new_user = serializer.save()
                    if new_user:
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response({"msg": "Somthing wrong"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"msg": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Profile(APIView):

    def get(self, request, format=None):
        details = request.user
        serializer = UserSerializer(details)
        return Response(serializer.data)

    def put(self, request, format=None):
        user = request.user
        serializer = ActionsUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        user = request.user
        user.delete()
        return Response({"msg": "User deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


class Change_password(APIView):
    def put(self, request, fromat=None):
        user = request.user
        serializer = ChangePasswordSerializer(user, data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            new_user = serializer.save()
            if new_user:
                return Response({"msg": "Password updated Successfully"}, status=status.HTTP_200_OK)
        return Response({"msg": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class User_logout(APIView):
    def post(self, request):
        request.user.delete()
        return Response({"msg": "User logout Successfully"}, status=status.HTTP_200_OK)


class Create_Session_Checkout(APIView):
    def post(self, request):
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "inr",
                        "unit_amount": 10000,
                        "product_data": {
                            "name": "Premium Subscription",
                        }
                    },
                    "quantity": 1,
                },

            ],
            mode='payment',
            success_url='http://127.0.0.1:8000/success/',
            cancel_url='http://127.0.0.1:8000/cancel/',
        )

        return redirect(checkout_session.url, code=303)


def payment_success(request):
    user = request.user
    print(user)
    user_data = UserInfo.objects.get(email=user.email)
    user_data.is_premium = True
    user_data.premium_expiry = datetime.datetime.now()
    user_data.save()
    return render(request, "stripe_success_page.html")


def payment_cancel(request):
    return render(request, "stripe_cancel_page.html")


def checkout(request):
    user = request.user
    user_data = UserInfo.objects.get(email=user.email)
    if user_data.is_premium:
        return render(request, "already_member.html")
    return render(request, "stripe_home.html")


def payment_process(request):
    user = request.user
    user_data = UserInfo.objects.get(email=user.email)
    if user_data.is_premium:
        return render(request, "already_member.html")
    else:
        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': '100',
            'item_name': 'Item_Name_xyz',
            'invoice': 'Test Payment Invoice',
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
            'cancel_return': 'http://{}{}'.format(host, reverse('payment_canceled_paypal')),
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request, 'payment_process.html', {'form': form})


def payment_done(request):
    user = request.user
    print(user)
    user_data = UserInfo.objects.get(email=user.email)
    user_data.is_premium = True
    user_data.premium_expiry = datetime.datetime.now()
    user_data.save()
    return render(request, "payment_done.html")


def payment_cancel_paypal(request):
    return render(request, "payment_cancel_paypal.html")

#
# class TestView(APIView):
#     def get(self, request):
#
#         # Locate name in redis database
#         if 'name' in cache:
#             # get results from cache
#             name = cache.get('name')
#
#             print('form cache')
#             return Response(name)
#
#         # If not found
#         else:
#             result = {
#                 "name": "anivesh"
#             }
#
#             # store data in cache
#             cache.set('name', result, timeout=settings.CACHE_TTL)
#
#             print('not from cache')
#             return Response(result)