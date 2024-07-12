from django.urls import path
from . import views

app_name = 'homecounter'

urlpatterns = [
    path('profile_user/', views.Profile.as_view(), name='profile'),
    path('profile_admin/', views.Profile_admin.as_view(), name='profile_admin'),
    path('out/', views.out.as_view(), name='out'),
    path('settings_user/', views.Settings_user.as_view(), name='settings_user'),
    path('settings_admin/', views.Settings_admin.as_view(), name='settings_admin'),
    path('house_admin/', views.Summari_home.as_view(), name='summari_home'),
    path('analize/', views.Analize.as_view(), name='analize'),
    path('get_data/', views.get_data, name='get_data'), #генерация данных
   
]