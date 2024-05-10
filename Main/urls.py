from django.urls import include, path
from .views import *

extra_patterns = [
    path("", job_details, name="job_details"),
    path("aptitude_test", aptitude_test, name="aptitude_test"),
    path("personality_test", personality_test,
         name="personality_test"),  # type: ignore
    path("apply", apply_view, name="apply"),
    path("cv", cv_view, name="cv"),  # type: ignore
]

urlpatterns = [
    path("", index, name="index"),
    path("login", login_view, name="login"),
    path("jobs", view_jobs, name="view_jobs"),
    path("jobs/<int:pk>/", include(extra_patterns)),
    path("signup", signup_view, name="signup"),
    path("logout", logout_view, name="logout"),
    path("loading", loading_view, name="loading"),
    path("success", success_page, name="success"),
    path("error", error_page, name="error")
]
