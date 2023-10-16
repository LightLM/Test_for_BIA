from django.urls import path
from . import views

urlpatterns = [
    path('generate_schedule/<int:year>/<int:month>/', views.generate_schedule, name='generate_schedule'),
]
