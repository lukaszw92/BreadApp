from django import forms
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from bread.models import Grain, Flour, Leaven, FlourInLeaven, Bread, FlourInBread
from bread.forms import LeavenForm, FlourInLeavenForm


"""
Leaven related views
"""


class FlourInLeavenView(View):

    def get(self, request, pk):
        form = FlourInLeavenForm()
        return render(request, "leaven/flour_in_leaven.html", {'form': form})

    def post(self, request, pk):
        leaven = Leaven.objects.get(pk=pk)
        form = FlourInLeavenForm(request.POST)

        if form.is_valid():
            form_input = form.save(commit=False)
            form_input.leaven = leaven
            form_input.save()
            return redirect(reverse("show_leavens"))
        return render(request, 'leaven/flour_in_leaven.html', {'form': form})

class AddLeavenView(View):

    def get(self, request):
        form = LeavenForm()
        return render(request, "leaven/l.html", {'form': form})

    def post(self, request):
        form = LeavenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("show_leavens"))
        return render(request, 'leaven/l.html', {'form': form})



class ShowLeavensView(ListView):
    model = Leaven
    template_name = 'leaven/show_leaven.html'
    queryset = Leaven.objects.all()


class RemoveLeavenView(DeleteView):
    model = Leaven
    template_name = 'leaven/remove_leaven.html'
    success_url = reverse_lazy('show_leavens')


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
