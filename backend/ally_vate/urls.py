from django.urls import path 
from .views import *
urlpatterns =[
    path('ongoing/',retrieve,name="retrieve"),
    path('end/',end,name="end")
]