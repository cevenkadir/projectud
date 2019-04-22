from django.urls import path
from django.conf.urls import url

from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view()),
    path('data', views.DataView.as_view()),
    path('upload', login_required(views.UploadParticlesView.as_view())),
]