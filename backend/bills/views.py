from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from .models import Bill, Payment
from .serializers import BillSerializer, PaymentSerializer

# Create your views here.

class BillListView(generics.ListCreateAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

class BillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

class PaymentListView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class CreateSubscriptionView(APIView):
    def post(self, request):
        resident_id = request.data.get('resident')
        subscription_type = request.data.get('subscription_period')
        amount = request.data.get('amount')

        if not all([resident_id, subscription_type, amount]):
            return Response(
                {"error": "Необходимо указать resident, subscription_period и amount"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Определяем срок подписки
        if subscription_type == 'MONTH':
            due_date = datetime.now() + timedelta(days=30)
        elif subscription_type == 'SEMESTER':
            due_date = datetime.now() + timedelta(days=180)
        elif subscription_type == 'YEAR':
            due_date = datetime.now() + timedelta(days=365)
        else:
            return Response(
                {"error": "Неверный период подписки"},
                status=status.HTTP_400_BAD_REQUEST
            )

        bill_data = {
            'resident': resident_id,
            'amount': amount,
            'due_date': due_date,
            'bill_type': 'SUBSCRIPTION',
            'subscription_period': subscription_type
        }

        serializer = BillSerializer(data=bill_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
