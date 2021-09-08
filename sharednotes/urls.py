from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('', include("main.urls")),
    path('user/', include("userapp.urls")),    
    path('admin/', admin.site.urls),
]
