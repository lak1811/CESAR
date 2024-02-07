from django.urls import path, include
from . import views
import include


urlpatterns=[
    path("testapp1/",views.index),
    path('', views.index, name='index'),
    path('dash/', views.dash_view, name='dash_view'),

    



]