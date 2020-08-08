from django.urls import path
from bread import views
from bread.models import Grain

urlpatterns = [
    # path("add_bread/", views.AddBreadView.as_view(), name='add_bread'),
    path("grain/add_grain/", views.AddGrainView.as_view(), name='add_grain'),
    path("grain/show_grains/", views.ShowGrainsView.as_view(), name='show_grains'),
    path("grain/remove_grain/<int:pk>", views.RemoveGrainView.as_view(), name='remove_grain')
]