from rest_framework import serializers
from .models import Donation
    

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = [ 'email','full_name', 'location','amount', 'payment_status', 'stripe_session_id', 'donation_id', 'created_at']
        read_only_fields = ['donation_id', 'stripe_session_id', 'created_at', 'payment_status']

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount cannot be negative.")
        return value