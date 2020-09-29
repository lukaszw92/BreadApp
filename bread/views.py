
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from bread.models import Grain, Flour, Leaven, FlourInLeaven, Bread, FlourInBread
from bread.forms import LeavenForm, FlourInLeavenForm, BreadForm


"""Bread related views"""

"""ShowBreadsView displays all breads created by the user who is currently logged in"""


class ShowBreadsView(View):
    def get(self, request):
        if request.user.is_anonymous:
            return redirect(reverse('login'))
        breads = Bread.objects.filter(user=request.user)
        return render(request, "bread/show_breads.html", {'object_list': breads})


"""ShowAllBreadsView displays all breads in database regardless of whether user is logged in"""


class ShowAllBreadsView(ListView):
    model = Bread
    template_name = 'bread/show_breads.html'
    queryset = Bread.objects.all()


"""AddBreadView adds a bread to database. Added bread belongs to the user who is logged in at the moment of creation.
Due to intermediate table being used to assign flours to bread, flours are added in a separate view."""


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


"""FlourInBreadView adds flours and their amounts to given bread. User gets redirected to this view after creating 
the base bread. You can also add flours to the bread after the initial bread creation process. 

Because multiple flours can be added at the same time (see file static/js/flour_form.js)
the form had to be created and handled "manually" - not using generic views."""


class FlourInBreadView(LoginRequiredMixin, View):
    def get(self, request, pk):
        flours = Flour.objects.all()
        context = {'flours': flours}
        bread = Bread.objects.get(pk=pk)

        if bread.user != request.user:
            response = redirect(reverse('error'))
            response.set_cookie("error_message", "You cannot add flour to someone else's bread.", max_age=10)
            return response

        return render(request, "bread/flour_in_bread2.html", context)

    def post(self, request, pk):
        flours = request.POST.getlist('flour')
        grams = request.POST.getlist('grams')
        bread = Bread.objects.get(pk=pk)

        already_there = []
        for flour_in_bread in bread.get_flour_list():
            already_there.append(str(flour_in_bread.flour.id))

        added_flours = []
        for flour, weight in zip(flours, grams):

            if int(weight) <= 0:
                response = redirect(reverse('error'))
                response.set_cookie("error_message", "Value has to be positive.", max_age=10)
                return response

            elif flour in added_flours:
                response = redirect(reverse('error'))
                response.set_cookie("error_message", "You cannot add the same flour more than once.", max_age=10)
                return response

            elif flour in already_there:
                response = redirect(reverse('error'))
                response.set_cookie("error_message", "This flour is already there in the bread.", max_age=10)
                return response

            FlourInBread.objects.create(bread=bread, flour_id=flour, grams=weight)
            added_flours.append(flour)

        return redirect(reverse("show_breads"))


"""
RemoveFlourBreadView removes given flower from given bread
"""


class RemoveFlourBreadView(LoginRequiredMixin, DeleteView):
    model = FlourInBread
    template_name = 'bread/remove_flour_bread.html'
    success_url = reverse_lazy('show_breads')

    def dispatch(self, request, *args, **kwargs):
        flour_in_bread = self.get_object()
        if flour_in_bread.bread.user != self.request.user:

            response = redirect(reverse('error'))
            response.set_cookie("error_message", "You cannot edit someone else's bread.", max_age=10)
            return response

        return super().dispatch(request, *args, **kwargs)


"""EditFlourBreadView edits given flower in given bread"""


class EditFlourBreadView(LoginRequiredMixin, UpdateView):
    model = FlourInBread
    fields = ['flour', 'grams']
    template_name = 'bread/edit_flour_bread.html'
    success_url = reverse_lazy('show_breads')

    """Making sure that one will not edit a flour in 
    bread so that it is the same flour that's already there in the bread"""

    def form_valid(self, form):
        already_there = []
        for flour_in_bread in self.object.bread.get_flour_list():
            already_there.append(flour_in_bread.flour.id)

        if self.object.flour.id in already_there:

            response = redirect(reverse('error'))
            response.set_cookie("error_message", "This flour is already there in the bread.", max_age=10)
            return response

        self.object = form.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        enable_delete = super().dispatch(request, *args, **kwargs)
        flour_in_bread = self.get_object()
        if flour_in_bread.bread.user != self.request.user:

            response = redirect(reverse('error'))
            response.set_cookie("error_message", "You cannot edit someone else's bread.", max_age=10)
            return response

        return enable_delete


"""
RemoveBreadView removes given bread.
"""


class RemoveBreadView(LoginRequiredMixin, DeleteView):
    model = Bread
    template_name = 'bread/remove_bread.html'
    success_url = reverse_lazy('show_breads')

    def dispatch(self, request, *args, **kwargs):
        bread = self.get_object()
        if bread.user != self.request.user:

            response = redirect(reverse('error'))
            response.set_cookie("error_message", "You cannot delete someone else's bread.", max_age=10)
            return response

        return super().dispatch(request, *args, **kwargs)


"""EditBreadView edits given bread. Flours from given bread can be edited in a separate view."""


class EditBreadView(LoginRequiredMixin, UpdateView):
    model = Bread
    fields = ['name', 'date', 'water', 'salt', 'leaven', 'first_proofing',
              'second_proofing', 'baking_time', 'baking_temperature', 'rating', 'notes']
    template_name = 'bread/edit_bread.html'
    success_url = reverse_lazy('show_breads')

    def dispatch(self, request, *args, **kwargs):
        enable_edit = super().dispatch(request, *args, **kwargs)
        bread = self.get_object()
        if bread.user != self.request.user:

            response = redirect(reverse('error'))
            response.set_cookie("error_message", "You cannot edit someone else's bread.", max_age=10)
            return response

        return enable_edit


"""
Leaven related views
"""

"""AddLeavenView adds a leaven to database. Added leaven belongs to the user who is logged in at the moment of creation.
Due to intermediate table being used to assign flours to leaven, flours are added in a separate view."""


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


"""FlourInLeavenView adds flours and their amounts to given leaven. 

Because mixing multiple flours in one leaven is not a common practice
unlike with FlourInBreadView user can only add flours to the leaven one at the time."""


class FlourInLeavenView(LoginRequiredMixin, View):

    def get(self, request, pk):
        form = FlourInLeavenForm()
        leaven = Leaven.objects.get(pk=pk)

        if leaven.user != request.user:

            response = redirect(reverse('error_leaven'))
            response.set_cookie("error_message", "You cannot add flour to someone else's leaven.", max_age=10)
            return response

        return render(request, "leaven/flour_in_leaven.html", {'form': form})

    def post(self, request, pk):
        leaven = Leaven.objects.get(pk=pk)
        form = FlourInLeavenForm(request.POST)

        already_there = []
        for flour_in_leaven in leaven.get_flour_list():
            already_there.append(flour_in_leaven.flour.id)

        if form.is_valid():
            new_flour = form.save(commit=False)

            if new_flour.flour.id in already_there:
                response = redirect(reverse('error_leaven'))
                response.set_cookie("error_message", "This flour is already there in the bread.", max_age=10)
                return response

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

    def dispatch(self, request, *args, **kwargs):
        leaven = self.get_object()
        if leaven.user != self.request.user:

            response = redirect(reverse('error_leaven'))
            response.set_cookie("error_message", "You cannot delete someone else's leaven.", max_age=10)
            return response

        return super().dispatch(request, *args, **kwargs)


"""
EditLeavenView edits given leaven from database.
"""


class EditLeavenView(LoginRequiredMixin, UpdateView):
    model = Leaven
    fields = ['name', 'sourdough', 'water', 'proofing']
    template_name = 'leaven/edit_leaven.html'
    success_url = reverse_lazy('show_leavens')

    def dispatch(self, request, *args, **kwargs):
        leaven = self.get_object()
        if leaven.user != self.request.user:

            response = redirect(reverse('error_leaven'))
            response.set_cookie("error_message", "You cannot edit someone else's leaven.", max_age=10)
            return response

        return super().dispatch(request, *args, **kwargs)


"""
RemoveFlourLeavenView removes flour from given leaven from database.
"""


class RemoveFlourLeavenView(LoginRequiredMixin, DeleteView):
    model = FlourInLeaven
    template_name = 'bread/remove_flour_bread.html'
    success_url = reverse_lazy('show_leavens')

    def dispatch(self, request, *args, **kwargs):
        flour_in_leaven = self.get_object()
        if flour_in_leaven.leaven.user != self.request.user:

            response = redirect(reverse('error_leaven'))
            response.set_cookie("error_message", "You cannot edit someone else's leaven.", max_age=10)
            return response

        return super().dispatch(request, *args, **kwargs)


"""shows error message passed to the function argument for bread and leaven views"""


def error(request):
    error = request.COOKIES.get('error_message')
    return render(request, 'bread/error.html', context={'error': error})


def error_leaven(request):
    error = request.COOKIES.get('error_message')
    return render(request, 'leaven/error.html', context={'error': error})


"""Flour related views"""

"""AddFlourView adds flour to database. Note: flours are not assigned to any user and can be viewed by all users."""


class AddFlourView(LoginRequiredMixin, CreateView):
    model = Flour
    fields = '__all__'
    success_url = reverse_lazy('add_flour')
    template_name = 'flour/add_flour.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'object_list': Flour.objects.all()})
        return context


"""RemoveFlourView removes flour from database."""


class RemoveFlourView(PermissionRequiredMixin, DeleteView):
    permission_required = 'flour.delete_flour'

    model = Flour
    template_name = 'flour/remove_flour.html'
    success_url = reverse_lazy('add_flour')


"""EditFlourView edits flour given flour data."""


class EditFlourView(PermissionRequiredMixin, UpdateView):
    permission_required = 'flour.update_flour'

    model = Flour
    fields = '__all__'
    template_name = 'flour/edit_flour.html'
    success_url = reverse_lazy('add_flour')


"""Grain related views"""

"""AddsGrainView adds grain to database. Note: grains are not assigned to any user and can be viewed by all users."""


class AddGrainView(LoginRequiredMixin, CreateView):
    model = Grain
    fields = '__all__'
    success_url = reverse_lazy('add_grain')
    template_name = 'grain/add_grain.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'object_list': Grain.objects.all()})
        return context


"""RemoveGrainView removes grain from database. Edit view was not created for grains as grains only have one attribute
so deleting and adding a grain is simpler and more intuitive than editing it."""


class RemoveGrainView(PermissionRequiredMixin, DeleteView):
    permission_required = 'grain.delete_grain'

    model = Grain
    template_name = 'grain/remove_grain.html'
    success_url = reverse_lazy('add_grain')

