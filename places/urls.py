from django.urls import path
from . import views

app_name = 'places'

urlpatterns = [
    path('', views.index, name='index'),  # Index view

    
    path('<int:pk>/', views.place_detail, name='place_detail'),
    path('new/', views.place_new, name='place_new'),
    # Other paths

    path('place/<int:place_id>/book/', views.make_booking, name='make_booking'),
    path('booking-success/<int:booking_id>/', views.booking_success, name='booking_success'),
]

