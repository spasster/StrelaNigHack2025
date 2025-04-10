from rest_framework import serializers
from .models import Bill, Payment
from .robokassa import generate_payment_link

class BillSerializer(serializers.ModelSerializer):
    payment_url = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = '__all__'
        read_only_fields = ('created_date', 'status', 'is_paid', 'paid_date')

    def get_payment_url(self, obj):
        if not obj.is_paid:
            return generate_payment_link(number=obj.id)
        return None

    def validate(self, data):
        if data.get('bill_type') == 'SUBSCRIPTION' and not data.get('subscription_period'):
            raise serializers.ValidationError("Для подписки необходимо указать период")
        return data

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('payment_date', 'status') 