from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.views import View


urlpatterns = [
    path("", include('django.contrib.auth.urls')),
    path("sign_up/", views.CreateUserView.as_view(), name="sign_up")

]