from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from bread.models import Grain, Flour, Leaven, FlourInLeaven, Bread, FlourInBread
from bread.forms import LeavenForm, FlourInLeavenForm, BreadForm, FlourInBreadForm

"""
ShowBreadsView displays all breads created by the user who is currently logged in"
"""


class ShowBreadsView(View):
    def get(self, request):
        if request.user.is_anonymous:
            return redirect(reverse('login'))
        breads = Bread.objects.filter(user=request.user)
        return render(request, "bread/show_breads.html", {'object_list': breads})


"""
ShowAllBreadsView displays all breads in database regardless of whether user is logged in"
"""


class ShowAllBreadsView(ListView):
    model = Bread
    template_name = 'bread/show_breads.html'
    queryset = Bread.objects.all()


"""
AddBreadView adds a bread to database. Added bread belongs to the user who is logged in at the moment of creation.
Due to intermediate table being used to assign flours to bread, flours are added in a separate view.
"""


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
            return redirect(reverse('flour_in_bread', args=(new_bread.pk,)))
        return render(request, 'bread/add_bread.html', {'form': form})


"""
FlourInBreadView adds flours and their amounts to given bread. 
User gets redirected to this view after creating the base bread.
You can also add flours to the bread after the initial bread creation process. 

Because multiple flours can be added at the same time (see file static/js/flour_form.js)
the form had to be created and handled "manually" - not using generic views.
"""


class FlourInBreadView(LoginRequiredMixin, View):
    def get(self, request, pk):
        flours = Flour.objects.all()
        context = {'flours': flours}
        return render(request, "bread/flour_in_bread2.html", context)

    def post(self, request, pk):
        flours = request.POST.getlist('flour')
        grams = request.POST.getlist('grams')
        bread = Bread.objects.get(pk=pk)

        already_there = []
        for flour_in_bread in bread.get_flour_list():
            already_there.append(str(flour_in_bread.flour.id))

        for flour, weight in zip(flours, grams):
            added_flours = []

            if int(weight) <= 0:
                return redirect(reverse('error', args=["Value has to be positive"]))

            elif flour in added_flours:
                return redirect(reverse('error', args=["You cannot add the same flour more than once."]))

            elif flour in already_there:
                return redirect(reverse('error', args=["This flour is already there in the bread."]))

            FlourInBread.objects.create(bread=bread, flour_id=flour, grams=weight)
            added_flours.append(flour)

        return redirect(reverse("show_breads"))

"""
Due to the fact that FlourInBreadView had to be created manually
the validation for that form also had to be done manually - thus separate error function.
"""


def error(request, error_message):
    return render(request, 'bread/error.html', context={'error_message': error_message})


"""
RemoveFlourBreadView removes given flower from given bread
"""


class RemoveFlourBreadView(LoginRequiredMixin, DeleteView):
    model = FlourInBread
    template_name = 'bread/remove_flour_bread.html'
    success_url = reverse_lazy('show_breads')


"""
EditFlourBreadView edits given flower in given bread
"""

class EditFlourBreadView(LoginRequiredMixin, UpdateView):
    model = FlourInBread
    fields = ['flour', 'grams']
    template_name = 'bread/edit_flour_bread.html'
    success_url = reverse_lazy('show_breads')

"""
RemoveBreadView removes given bread.
"""


class RemoveBreadView(LoginRequiredMixin, DeleteView):
    model = Bread
    template_name = 'bread/remove_bread.html'
    success_url = reverse_lazy('show_breads')


"""
EditBreadView edits given bread. 
Flours from given bread can be edited in a separate view.
"""


class EditBreadView(LoginRequiredMixin, UpdateView):
    model = Bread
    fields = ['name', 'date', 'water', 'salt', 'leaven', 'first_proofing',
              'second_proofing', 'baking_time', 'baking_temperature', 'rating', 'notes']
    template_name = 'bread/edit_bread.html'
    success_url = reverse_lazy('show_breads')


"""
Leaven related views
"""

"""
AddLeavenView adds a leaven to database. Added leaven belongs to the user who is logged in at the moment of creation.
Due to intermediate table being used to assign flours to leaven, flours are added in a separate view.
"""


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


"""
FlourInLeavenView adds flours and their amounts to given leaven. 

Because mixing multiple flours in one leaven is not a common practice
unlike with FlourInBreadView user can only add flours to the leaven one at the time.
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
            return redirect(reverse("show_leavens"))
        return render(request, 'leaven/flour_in_leaven.html', {'form': form})

"""
ShowLeavensView displays all leavens created by the user who is currently logged in"
"""

class ShowLeavensView(View):
    def get(self, request):
        if request.user.is_anonymous:
            return redirect(reverse('login'))
        leavens = Leaven.objects.filter(user=request.user)
        return render(request, "leaven/show_leaven.html", {'object_list': leavens})

"""
ShowAllLeavensView displays all leavens in database regardless of whether user is logged in"
"""

class ShowAllLeavensView(ListView):
    model = Leaven
    template_name = 'leaven/show_leaven.html'
    queryset = Leaven.objects.all()

"""
RemoveLeavenView removes given leaven from database.
"""

class RemoveLeavenView(LoginRequiredMixin, DeleteView):
    model = Leaven
    template_name = 'leaven/remove_leaven.html'
    success_url = reverse_lazy('show_leavens')

"""
EditLeavenView edits given leaven from database.
"""

class EditLeavenView(LoginRequiredMixin, UpdateView):
    model = Leaven
    fields = ['name', 'sourdough', 'water', 'proofing']
    template_name = 'leaven/edit_leaven.html'
    success_url = reverse_lazy('show_leavens')

"""
RemoveFlourLeavenView removes flour from given leaven from database.
"""


class RemoveFlourLeavenView(LoginRequiredMixin, DeleteView):
    model = FlourInLeaven
    template_name = 'bread/remove_flour_bread.html'
    success_url = reverse_lazy('show_leavens')


"""
Grain related views
"""

"""
AddsGrainView adds grain to database. Note: grains are not assigned to any user and can be viewed by all users.
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

"""
RemoveGrainView removes grain from database. Edit view was not created for grains as grains only have one attribute
so deleting and adding a grain is simpler and more intuitive than editing it.
"""


class RemoveGrainView(PermissionRequiredMixin, DeleteView):

    permission_required = 'grain.delete_grain'

    model = Grain
    template_name = 'grain/remove_grain.html'
    success_url = reverse_lazy('add_grain')


"""
Flour related views
"""

"""
AddFlourView adds flour to database. Note: flours are not assigned to any user and can be viewed by all users.
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

"""
RemoveFlourView removes flour from database.
"""

class RemoveFlourView(PermissionRequiredMixin, DeleteView):

    permission_required = 'flour.delete_flour'

    model = Flour
    template_name = 'flour/remove_flour.html'
    success_url = reverse_lazy('add_flour')

"""
EditFlourView edits flour given flour data.
"""


class EditFlourView(PermissionRequiredMixin, UpdateView):

    permission_required = 'flour.update_flour'

    model = Flour
    fields = '__all__'
    template_name = 'flour/edit_flour.html'
    success_url = reverse_lazy('add_flour')
