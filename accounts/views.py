from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import User
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.forms import UserCreationForm



class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html')

class CreateUserView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/new_user.html"