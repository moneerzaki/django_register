from django.urls import path

from . import views

app_name = 'project2'

urlpatterns = [
    # path("<int:id>", views.index, name="index"),
    path('ebtda2y/', views.ebtda2y, name="ebtda2y"),
    path('ebtda2y/info/', views.info, name="info"),
    path('ebtda2y/info/add_student/', views.add_student, name="add_student"),
    path('ebtda2y/info/edit_student/<int:student_id>/', views.edit_student, name="edit_student"),

]