from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scrapCarPrice', views.scrapCarPrice, name='scrapCarPrice'),
    path('scrapCarGrade', views.scrapCarGrade, name='scrapCarGrade'),
    path('scrapCarGradeSubGroup', views.scrapCarGradeSubGroup, name='scrapCarGradeSubGroup'),
    # path('car/search/<str:company>/<str:model>/<str:modelDetail>/', views.search, name='search'),
]