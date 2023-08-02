from django.urls import path

from . import views

urlpatterns = [
    # path("<int:id>", views.index, name="index"),
    path('homepage/', views.homepage, name="homepage"),
]