from django.urls import path
from bread import views

urlpatterns = [
    path("grain/add_grain/", views.AddGrainView.as_view(), name='add_grain'),
    path("grain/remove_grain/<int:pk>", views.RemoveGrainView.as_view(), name='remove_grain'),

    path("flour/add_flour/", views.AddFlourView.as_view(), name='add_flour'),
    path("flour/remove_flour/<int:pk>", views.RemoveFlourView.as_view(), name='remove_flour'),
    path("flour/edit_flour/<int:pk>", views.EditFlourView.as_view(), name='edit_flour'),

    path("starter/add_starter/", views.AddStarterView.as_view(), name='add_starter'),
    path("starter/remove_starter/<int:pk>", views.RemoveStarterView.as_view(), name='remove_starter'),
    path("starter/edit_starter/<int:pk>", views.EditStarterView.as_view(), name='edit_starter'),
    #path("starter/flour_in_starter/", views.FlourInStarterView.as_view(), name='flour_in_starter'),
    path("starter/show_starters/", views.ShowStartersView.as_view(), name='show_starters'),

]