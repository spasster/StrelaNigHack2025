from django.urls import path
from . import views

urlpatterns = [
    path('bills/', views.BillListView.as_view(), name='bill-list'),
    path('bills/<int:pk>/', views.BillDetailView.as_view(), name='bill-detail'),
    path('payments/', views.PaymentListView.as_view(), name='payment-list'),
    path('rent/create/', views.CreateRentBillView.as_view(), name='create-rent-bill'),
    path('payments/create/', views.CreatePaymentView.as_view(), name='create-payment'),
] 