from django.urls import path
from . import views

urlpatterns = [
    path('<int:roadmap_id>/', views.roadmap_view, name='roadmap'),
]