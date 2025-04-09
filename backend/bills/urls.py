from django.urls import path
from .views import BillListView, BillDetailView, PaymentListView

urlpatterns = [
    path('', BillListView.as_view(), name='bill-list'),
    path('bills/<int:pk>/', BillDetailView.as_view(), name='bill-detail'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
] 