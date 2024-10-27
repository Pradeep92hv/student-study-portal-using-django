from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="home"),
     path('hi', views.hi, name="hi"),
    path('aboutpage', views.about, name="about"),
    
    
    path('notes/', views.notes, name="notes"),
    path('delete/<int:id>/', views.delete_note, name='delete-note'),  
    path('notes_detail/<int:pk>/', views.NotesDetailView.as_view(), name='notes-detail'),

    
    path('homework/', views.homework, name="homework"),

]