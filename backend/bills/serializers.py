from rest_framework import serializers
from .models import Bill, Payment
from .robokassa import generate_payment_link

class BillSerializer(serializers.ModelSerializer):
    payment_url = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = ['id', 'resident', 'amount', 'created_date', 'due_date', 
                 'is_paid', 'paid_date', 'bill_type', 'status', 'payment_url']

    def get_payment_url(self, obj):
        if not obj.is_paid:
            return generate_payment_link(number=obj.id)
        return None

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'bill', 'amount', 'payment_date', 
                 'payment_method', 'transaction_id', 'status'] 