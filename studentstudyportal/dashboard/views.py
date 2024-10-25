from django.shortcuts import render,render
from django.http import HttpResponse

# Create your views here.

def homepage(request):
    return render(request,'dashboard/home.html')


def about(request):
    return HttpResponse("homepage about")

def hi(request):
    return render(request,'dashboard/index.html')





from django.shortcuts import render
# from . forms import NotesForm
from . form import *
from django.contrib import messages
from django.views import generic

# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')


def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        
        if form.is_valid():
            notes =Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
            
        messages.success(request,f"notes added from {request.user.username} Successfully")
        
    else:
        form=NotesForm()
    notes = Notes.objects.filter(user=request.user)
    
    context = { 'notes' :notes,'form': form}
    return render(request,'dashboard/notes.html',context)

class NotesDetailView(generic.DetailView):
    model =Notes
    template_name = 'dashboard/notes_detail.html'  # Specify the correct template
    context_object_name = 'note'
    
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Notes


def delete_note(request,id):
    note = get_object_or_404(Notes, id=id)
    note.delete()  # Delete the note
    return redirect("notes")

    
    
def homework(request):
    if request.method == 'POST':
        form =HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = Flase
            except:
                finished = False
            homeworks=HomeWork(
                user = request.user,subject = request.POST['subject'],
                title = request.POST['title'],
                description =request.POST['description'],
                due = request.POST['due'],is_finished = finished
            )  
            homeworks.save()
            messages.success(request,f'Homework Added from  {request.user.username}!!') 
    else:
        form = HomeworkForm()
    homework=Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
        
    context={'homeworks':homework,'homeworks_done':homework_done,'form' : form}
    return render(request,'dashboard/homework.html',context)
    


    



