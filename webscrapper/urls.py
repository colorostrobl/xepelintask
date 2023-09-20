from django.urls import path
from . import views

app_name = 'webscrapper'
urlpatterns = [
    path('', views.the_scrapper, name=''),
]
