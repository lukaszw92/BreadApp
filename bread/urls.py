from django.urls import path
from bread import views
from bread.models import Grain

urlpatterns = [
    path("grain/add_grain/", views.AddGrainView.as_view(), name='add_grain'),
    path("grain/show_grains/", views.ShowGrainsView.as_view(), name='show_grains'),
    path("grain/remove_grain/<int:pk>", views.RemoveGrainView.as_view(), name='remove_grain'),

    path("flour/add_flour/", views.AddFlourView.as_view(), name='add_flour'),
    path("flour/show_flours/", views.AddFlourView.as_view(), name='add_flour'),
    path("flour/remove_flour/<int:pk>", views.RemoveFlourView.as_view(), name='remove_flour'),
    path("flour/edit_flour/<int:pk>", views.EditFlourView.as_view(), name='edit_flour'),

]