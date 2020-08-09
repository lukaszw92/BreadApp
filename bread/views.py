from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from bread.models import Grain, Flour


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


class AddFlourView(CreateView):
    model = Flour
    fields = '__all__'
    success_url = reverse_lazy('add_flour')
    template_name = 'add_flour.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'object_list': Flour.objects.all()})
        return context


class ShowFloursView(ListView):
    model = Flour
    template_name = 'show_flours.html'
    queryset = Flour.objects.all()


class RemoveFlourView(DeleteView):
    model = Flour
    template_name = 'remove_flour.html'
    success_url = reverse_lazy('add_flour')
    

class EditFlourView(UpdateView):
    model = Flour
    fields = '__all__'
    template_name = 'edit_flour.html'
    success_url = reverse_lazy('add_flour')