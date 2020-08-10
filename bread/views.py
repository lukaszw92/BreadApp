from django import forms
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from bread.models import Grain, Flour, Starter, FlourInStarter, Bread, FlourInBread


"""
Starter related views
"""

# class FlourInStarterView(CreateView):
#     model = FlourInStarter
#     fields = ['']
#     success_url = reverse_lazy('add_starter')
#     template_name = 'starter/flour_in_starter.html'


class AddStarterView(CreateView):
    model = Starter
    fields = '__all__'
    success_url = reverse_lazy('show_starters')
    template_name = 'starter/add_starter.html'
    widgets = {
        'name': forms.CheckboxSelectMultiple()
    }


class ShowStartersView(ListView):
    model = Starter
    template_name = 'starter/show_starters.html'
    queryset = Starter.objects.all()

class RemoveStarterView(DeleteView):
    model = Starter
    template_name = 'starter/remove_starter.html'
    success_url = reverse_lazy('add_starter')


class EditStarterView(UpdateView):
    model = Flour
    fields = '__all__'
    template_name = 'starter/edit_starter.html'
    success_url = reverse_lazy('add_starter')






"""
Grain related views
"""


class AddGrainView(CreateView):
    model = Grain
    fields = '__all__'
    success_url = reverse_lazy('add_grain')
    template_name = 'grain/add_grain.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'object_list': Grain.objects.all()})
        return context


class RemoveGrainView(DeleteView):
    model = Grain
    template_name = 'grain/remove_grain.html'
    success_url = reverse_lazy('add_grain')


"""
Flour related views
"""


class AddFlourView(CreateView):
    model = Flour
    fields = '__all__'
    success_url = reverse_lazy('add_flour')
    template_name = 'flour/add_flour.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'object_list': Flour.objects.all()})
        return context


class RemoveFlourView(DeleteView):
    model = Flour
    template_name = 'flour/remove_flour.html'
    success_url = reverse_lazy('add_flour')


class EditFlourView(UpdateView):
    model = Flour
    fields = '__all__'
    template_name = 'flour/edit_flour.html'
    success_url = reverse_lazy('add_flour')
