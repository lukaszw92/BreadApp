from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from bread.models import Grain


class AddGrainView(CreateView):
    model = Grain
    fields = '__all__'
    success_url = reverse_lazy('add_grain')
    template_name = 'grain/add_grain.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'object_list': Grain.objects.all()})
        return context


class ShowGrainsView(ListView):
    model = Grain
    template_name = 'grain/show_grains.html'
    queryset = Grain.objects.all()

class RemoveGrainView(DeleteView):
    model = Grain
    template_name = 'grain/remove_grain.html'
    success_url = reverse_lazy('add_grain')





