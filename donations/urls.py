from django.urls import path
# from .views import CreateCheckoutSession, PaymentSuccess
from .views import CreateCheckoutSession, PaymentSuccessView, StripeWebhookView, AllDonationList, DonatorDetails

urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSession.as_view(), name='create-checkout-session'),
    path('success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('all-donations/', AllDonationList.as_view(), name='all-donations'),
    path('donator/<int:donation_id>/', DonatorDetails.as_view(), name='donation-by-session'),
]