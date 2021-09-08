from django.urls import path
from .views import *

app_name = "userapp"
urlpatterns = [
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("auth/<int:user_id>/<str:token>/", auth, name="auth"),

]
