from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('car/search/<str:company>/<str:model>/<str:modelDetail>/', views.search, name='search'),
]