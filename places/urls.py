from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),  # Index view

    path('', views.place_list, name='place_list'),
    path('<int:pk>/', views.place_detail, name='place_detail'),
    path('new/', views.place_new, name='place_new'),
    # Other paths
]

