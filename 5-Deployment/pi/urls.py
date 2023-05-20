from django.urls import path
from . import views

urlpatterns = [
    path('jobs', views.job_recommend),
    path('pfe', views.pfe_recommend)
]