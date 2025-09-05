from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),

    # Notes CRUD
    path("notes_list", views.notes_list, name="notes_list"),
    path("add_note", views.add_note, name="add_note"),
    path("edit_note", views.edit_note, name="edit_note"),         # Edit note
    path("delete_note", views.delete_note, name="delete_note"),   # Delete note
    path("summarize_note", views.summarize_note, name="summarize_note"),
]
