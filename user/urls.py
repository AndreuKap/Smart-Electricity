from django.urls import path
from . import views


app_name = 'user'

urlpatterns = [
    path('', views.LoginUserView.as_view(), name='index'),
    path('register/', views.BwellerRegistrationView.as_view(), name='register'),
    path('password-reset/', views.password_reset_request_view, name='password_reset'),
    path('password-reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('password-reset/complete/', views.password_reset_complete_view, name='password_reset_complete'),
]