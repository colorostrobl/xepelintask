from django.urls import path
from . import views

app_name = 'GSheetEditor'
urlpatterns = [
    path('', views.home, name='home'),
]