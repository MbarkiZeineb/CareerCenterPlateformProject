from django.urls import path
from . import views

urlpatterns = [
    path('jobs', views.jobrecommendation, name="recommendjob"),
    path('pfe', views.pferecommendation, name="recommendpfe"),
    path('', views.index, name="index_cv"),
    path('upload', views.upload_file, name="upload_cv")
    
]