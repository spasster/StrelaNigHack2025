from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppealViewSet

router = DefaultRouter()
router.register(r'', AppealViewSet, basename='appeal')

urlpatterns = [
    path('', include(router.urls)),
] 