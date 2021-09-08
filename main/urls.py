from django.urls import path

from main.views import *

app_name = "main"
urlpatterns = [
    path("", index, name="index"),
    path("view/<str:slug>", page, name="page"),
    path("actions/add-page", add_page, name="add_page"),
]
