from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import User, Group
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.forms import UserCreationForm

from django.db.models.signals import post_save
from django.dispatch import receiver


# class LoginView(View):
#     def get(self, request):
#         return render(request, 'registration/login.html')


class CreateUserView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/new_user.html"

    from django.db.models.signals import post_save
    from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='regular_users'))

    # def form_valid(self, form):
    #     ret_val = super().form_valid(form)
    #     client_group = Group.objects.get(name='regular_users')
    #     self.object.groups.add(client_group)
    #     return ret_val
