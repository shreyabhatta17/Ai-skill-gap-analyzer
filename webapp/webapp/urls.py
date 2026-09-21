"""URL configuration for the skill-gap analyzer."""

from django.urls import include, path

urlpatterns = [
    path("api/", include("webapp.api.urls")),
]
