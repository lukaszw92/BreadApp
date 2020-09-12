from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import User, Group
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.forms import UserCreationForm


# class LoginView(View):
#     def get(self, request):
#         return render(request, 'registration/login.html')


class CreateUserView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/new_user.html"

    def form_valid(self, form):
        ret_val = super().form_valid(form)
        client_group = Group.objects.get(name='regular_users')
        self.object.groups.add(client_group)
        return ret_val
