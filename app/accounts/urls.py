from django.urls import path
from accounts import views

app_name = 'account'

urlpatterns = [
    path('create/', views.CreateAccountView.as_view(), name='create')
]
