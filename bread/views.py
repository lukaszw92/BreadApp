from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django import forms
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from bread.models import Grain, Flour, Leaven, FlourInLeaven, Bread, FlourInBread
from bread.forms import LeavenForm, FlourInLeavenForm, BreadForm, FlourInBreadForm


class ShowBreadsView(View):
    def get(self, request):
        breads = Bread.objects.filter(user=request.user)
        return render(request, "bread/show_breads.html", {'object_list': breads})


class ShowAllBreadsView(ListView):
    model = Bread
    template_name = 'bread/show_breads.html'
    queryset = Bread.objects.all()


class AddBreadView(LoginRequiredMixin, View):

    def get(self, request):
        form = BreadForm()
        return render(request, "bread/add_bread.html", {'form': form})

    def post(self, request):
        form = BreadForm(request.POST)
        if form.is_valid():
            new_bread = form.save(commit=False)
            user = request.user
            new_bread.user = user
            form.save()
            return reverse('flour_in_bread', args=(new_bread.pk,))
        return render(request, 'bread/add_bread.html', {'form': form})


class FlourInBreadView(View):
    def get(self, request, pk):
        flours = Flour.objects.all()
        context = {'flours': flours}
        return render(request, "bread/flour_in_bread2.html", context)

    def post(self, request, pk):
        flours = request.POST.getlist('flour')
        grams = request.POST.getlist('grams')
        bread = Bread.objects.get(pk=pk)
        for flour, weight in zip(flours, grams):
            FlourInBread.objects.create(bread=bread, flour_id=flour, grams=weight)
        return redirect(reverse("show_breads"))

class RemoveFlourBreadView(LoginRequiredMixin, DeleteView):
    model = FlourInBread
    template_name = 'bread/remove_flour_bread.html'
    success_url = reverse_lazy('show_breads')

class EditFlourBreadView(LoginRequiredMixin, UpdateView):
    model = FlourInBread
    fields = ['flour', 'grams']
    template_name = 'bread/edit_flour_bread.html'
    success_url = reverse_lazy('show_breads')


class RemoveBreadView(LoginRequiredMixin, DeleteView):
    model = Bread
    template_name = 'bread/remove_bread.html'
    success_url = reverse_lazy('show_breads')


class EditBreadView(LoginRequiredMixin,  UpdateView):
    model = Bread
    fields = ['name', 'date', 'water', 'salt', 'leaven', 'first_proofing',
              'second_proofing', 'baking_time', 'baking_temperature', 'rating', 'notes']
    template_name = 'bread/edit_bread.html'
    success_url = reverse_lazy('show_breads')



"""
Leaven related views
"""


class FlourInLeavenView(LoginRequiredMixin, View):

    def get(self, request, pk):
        form = FlourInLeavenForm()
        return render(request, "leaven/flour_in_leaven.html", {'form': form})

    def post(self, request, pk):
        leaven = Leaven.objects.get(pk=pk)
        form = FlourInLeavenForm(request.POST)

        if form.is_valid():
            new_flour = form.save(commit=False)
            new_flour.leaven = leaven
            new_flour.save()
            return redirect(reverse("show_leavens")) #return reverse('flour_in_bread', args=(new_bread.pk,))
        return render(request, 'leaven/flour_in_leaven.html', {'form': form})


class AddLeavenView(LoginRequiredMixin, View):

    def get(self, request):
        form = LeavenForm()
        return render(request, "leaven/add_leaven.html", {'form': form})

    def post(self, request):
        form = LeavenForm(request.POST)
        if form.is_valid():
            new_leaven = form.save(commit=False)
            user = request.user
            new_leaven.user = user
            form.save()
            return redirect(reverse("show_leavens"))
        return render(request, 'leaven/add_leaven.html', {'form': form})


class ShowLeavensView(View):
    def get(self, request):
        leavens = Leaven.objects.filter(user=request.user)
        return render(request, "leaven/show_leaven.html", {'object_list': leavens })


class ShowAllLeavensView(ListView):
    model = Leaven
    template_name = 'leaven/show_leaven.html'
    queryset = Leaven.objects.all()


class RemoveLeavenView(LoginRequiredMixin, DeleteView):
    model = Leaven
    template_name = 'leaven/remove_leaven.html'
    success_url = reverse_lazy('show_leavens')


class EditLeavenView(LoginRequiredMixin, UpdateView):
    model = Leaven
    fields = ['name', 'sourdough', 'water', 'flour', 'proofing']
    template_name = 'leaven/edit_leaven.html'
    success_url = reverse_lazy('show_leavens')


"""
Grain related views
"""


class AddGrainView(LoginRequiredMixin, CreateView):
    model = Grain
    fields = '__all__'
    success_url = reverse_lazy('add_grain')
    template_name = 'grain/add_grain.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'object_list': Grain.objects.all()})
        return context


class RemoveGrainView(LoginRequiredMixin, DeleteView):
    model = Grain
    template_name = 'grain/remove_grain.html'
    success_url = reverse_lazy('add_grain')



"""
Flour related views
"""


class AddFlourView(LoginRequiredMixin, CreateView):
    model = Flour
    fields = '__all__'
    success_url = reverse_lazy('add_flour')
    template_name = 'flour/add_flour.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'object_list': Flour.objects.all()})
        return context


class RemoveFlourView(LoginRequiredMixin, DeleteView):
    model = Flour
    template_name = 'flour/remove_flour.html'
    success_url = reverse_lazy('add_flour')


class EditFlourView(LoginRequiredMixin, UpdateView):
    model = Flour
    fields = '__all__'
    template_name = 'flour/edit_flour.html'
    success_url = reverse_lazy('add_flour')
