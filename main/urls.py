from django.urls import path

from main.views import *


urlpatterns = [
    path("/", index, name="index"),
    path("/view/<str:slug>", page, name="page"),
]
