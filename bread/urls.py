from django.urls import path
from bread import views

urlpatterns = [
    path("grain/add_grain/", views.AddGrainView.as_view(), name='add_grain'),
    path("grain/remove_grain/<int:pk>", views.RemoveGrainView.as_view(), name='remove_grain'),

    path("flour/add_flour/", views.AddFlourView.as_view(), name='add_flour'),
    path("flour/remove_flour/<int:pk>", views.RemoveFlourView.as_view(), name='remove_flour'),
    path("flour/edit_flour/<int:pk>", views.EditFlourView.as_view(), name='edit_flour'),

    path("leaven/add_leaven/", views.AddLeavenView.as_view(), name='add_leaven'),
    path("leaven/flour_in_leaven/<int:pk>", views.FlourInLeavenView.as_view(), name='flour_in_leaven'),
    path("leaven/remove_leaven/<int:pk>", views.RemoveLeavenView.as_view(), name='remove_leaven'),
    path("leaven/show_leavens/", views.ShowLeavensView.as_view(), name='show_leavens'),
    path("leaven/edit_leaven/<int:pk>", views.EditLeavenView.as_view(), name='edit_leaven'), #CLUMSY

    path("leaven/add_bread/", views.AddBreadView.as_view(), name='add_bread'),
    path("leaven/flour_in_bread/<int:pk>", views.FlourInBreadView.as_view(), name='flour_in_bread'),
    path("leaven/remove_bread/<int:pk>", views.RemoveBreadView.as_view(), name='remove_bread'),
    path("leaven/show_breads/", views.ShowBreadsView.as_view(), name='show_breads'),
    # path("leaven/edit_bread/<int:pk>", views.EditBreadView.as_view(), name='edit_bread'), #CLUMSY

]