from django import forms
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from bread.models import Grain, Flour, Leaven, FlourInLeaven, Bread, FlourInBread


"""
Leaven related views
"""

# class FlourInLeavenView(CreateView):
#     model = FlourInLeaven
#     fields = ['']
#     success_url = reverse_lazy('add_leaven')
#     template_name = 'leaven/flour_in_leaven.html'




class AddLeavenView(View):

    def get(self, request):
        leaven = Leaven.objects.all()
        flours = Flour.objects.all()
        ctx = {'leaven': leaven, 'flours': flours}
        return render(request, 'leaven/add_leaven.html', ctx)

    def post(self, request):
        name = request.POST.get['name']



class ShowLeavensView(ListView):
    model = Leaven
    template_name = 'leaven/show_leaven.html'
    queryset = Leaven.objects.all()



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
