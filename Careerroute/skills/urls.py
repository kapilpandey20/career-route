from django.urls import path
from . import views


urlpatterns = [

    path(
        "upload/",
        views.upload_resume,
        name="upload_resume"
    ),

    path(
        "career/",
        views.choose_career,
        name="choose_career"
    ),

    path(
        "skill-gap/<int:career_id>/",
        views.skill_gap,
        name="skill_gap"
    ),

]