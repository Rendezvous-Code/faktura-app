from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accountant import views

router = DefaultRouter()
router.register('accountant', views.AccountViewSet)

app_name = 'accountant'

urlpatterns = [
    path('', include(router.urls))
]
