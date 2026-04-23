from django.urls import path
from .views.main import home_page

urlpatterns = [
    path('', home_page, name='home'),
]