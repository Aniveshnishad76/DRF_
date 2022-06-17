from django.template.defaulttags import url
from rest_framework_simplejwt import views as jwt_views
from django.urls import path, include

from application import views
from application.views import UserRegistration, schema_view, Profile, Change_password, User_logout, \
    Create_Session_Checkout, payment_success, OTP

urlpatterns = [
    # path('', TestView.as_view(), name='test-url'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('request-otp/', OTP.as_view()),
    path('user/', UserRegistration.as_view()),
    path('actions/', Profile.as_view()),
    path('password/', Change_password.as_view()),
    path('logout/', User_logout.as_view()),
    path('stripe/', Create_Session_Checkout.as_view(), name="stripe"),
    path('success/',views.payment_success, name="success"),
    path('cancel/', views.payment_cancel, name="cancel"),
    path('', views.checkout, name="checkout"),
    # path('paypal/',include('paypal.standard.ipn.urls')),
    path('payment_process', views.payment_process, name="payment_process"),
    path('payment_done/',views.payment_done,name="payment_done"),
    path("payment_canceled/", views.payment_cancel_paypal,name="payment_canceled_paypal"),


]
