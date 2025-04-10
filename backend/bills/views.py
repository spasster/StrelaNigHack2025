from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from .models import Bill, Payment
from .serializers import BillSerializer, PaymentSerializer
from rooms.models import CheckInInformation

# Create your views here.

class BillListView(generics.ListCreateAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Получаем все счета для текущего пользователя
        user_email = self.request.user.email
        check_in = CheckInInformation.objects.filter(email=user_email).first()
        if check_in:
            return Bill.objects.filter(resident=check_in)
        return Bill.objects.none()

class BillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

class PaymentListView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

class CreateRentBillView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Получаем CheckInInformation по email из токена
        user_email = request.user.email
        check_in = CheckInInformation.objects.filter(email=user_email).first()
        
        if not check_in:
            return Response(
                {"error": "Информация о заселении не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        subscription_type = request.data.get('subscription_period')
        amount = request.data.get('amount')
        rent_start_date = request.data.get('rent_start_date')

        if not all([subscription_type, amount, rent_start_date]):
            return Response(
                {"error": "Необходимо указать subscription_period, amount и rent_start_date"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            rent_start_date = datetime.strptime(rent_start_date, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"error": "Неверный формат даты. Используйте YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, нет ли уже активного счета
        active_bill = Bill.objects.filter(
            resident=check_in,
            bill_type='RENT',
            status__in=['PENDING', 'PAID']
        ).first()

        if active_bill:
            return Response(
                {"error": "У вас уже есть активный счет на аренду"},
                status=status.HTTP_400_BAD_REQUEST
            )

        bill_data = {
            'resident': check_in.id,
            'amount': amount,
            'due_date': datetime.now() + timedelta(days=7),
            'bill_type': 'RENT',
            'subscription_period': subscription_type,
            'rent_start_date': rent_start_date
        }

        serializer = BillSerializer(data=bill_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        bill_id = request.data.get('bill')
        amount = request.data.get('amount')
        payment_method = request.data.get('payment_method')
        transaction_id = request.data.get('transaction_id')

        if not all([bill_id, amount, payment_method, transaction_id]):
            return Response(
                {"error": "Необходимо указать bill, amount, payment_method и transaction_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, принадлежит ли счет текущему пользователю
        user_email = request.user.email
        check_in = CheckInInformation.objects.filter(email=user_email).first()
        if not check_in:
            return Response(
                {"error": "Информация о заселении не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        bill = Bill.objects.filter(id=bill_id, resident=check_in).first()
        if not bill:
            return Response(
                {"error": "Счет не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        payment_data = {
            'bill': bill.id,
            'amount': amount,
            'payment_method': payment_method,
            'transaction_id': transaction_id,
            'status': 'SUCCESS'
        }

        serializer = PaymentSerializer(data=payment_data)
        if serializer.is_valid():
            payment = serializer.save()
            # Обновляем статус счета
            bill.is_paid = True
            bill.paid_date = datetime.now()
            bill.status = 'PAID'
            bill.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
