from django.contrib import admin
from django.urls import path
from adminapp import views

urlpatterns = [
   
    # path('get_countries_data',views.get_countries_data,name='get_countries_data'),
    # path('get_country_by_city/<str:city_name>/', views.get_country_by_city, name='get_country_by_city'),

    path('get_country_by_city', views.get_country_by_city, name='get_country_by_city'),
    # path('load_abbreviations_excel', views.load_abbreviations_excel, name='load_abbreviations_excel'),
    

]


