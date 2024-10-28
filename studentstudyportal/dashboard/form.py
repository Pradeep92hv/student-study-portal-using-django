from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

class NotesForm(forms.ModelForm):
    class Meta:
        model=Notes
        fields = ['title','description']
        
class DateInput(forms.DateInput):
    input_type = 'date'        
        
class HomeworkForm(forms.ModelForm):
    class Meta:
        model=Homework
        widgets = {'due' :DateInput()}
        fields = ['subject','title','description','due','is_finished']

class DashBoardForm(forms.Form):
    text=forms.CharField(max_length =100, label ="Enter Your Serach: ")

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields =['title','is_finished']


  # Ensure this is imported correctly

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User  # Remove the comma here
        fields = ['username', 'password1', 'password2']
