from django.urls import path
from . import views

urlpatterns = [
    path('bills/', views.BillListView.as_view(), name='bill-list'),
    path('bills/<int:pk>/', views.BillDetailView.as_view(), name='bill-detail'),
    path('payments/', views.PaymentListView.as_view(), name='payment-list'),
    path('subscriptions/create/', views.CreateSubscriptionView.as_view(), name='create-subscription'),
    path('rent/create/', views.CreateRentView.as_view(), name='create-rent'),
] 