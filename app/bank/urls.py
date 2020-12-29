from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bank import views

router = DefaultRouter()
router.register('clients', views.ClientViewSet)

app_name = 'bank'

urlpatterns = [
    path('', include(router.urls))
]
