from django.shortcuts import render,render
from django.http import HttpResponse
from youtubesearchpython import VideosSearch
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
            homeworks=Homework(
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
    


def update_homework(request, pk):
    homework = Homework.objects.get(id=pk)
    
    # Toggle the completion status
    homework.is_finished = not homework.is_finished
    homework.save()
    
    print("saved")

    return redirect('homework')

def delete_homework(request,pk):
    homework=Homework.objects.get(id=pk)
    homework.delete()
    return redirect('homework')
def youtube(request):
    form = DashBoardForm()  # Initialize the form at the start
    result_list = []

    if request.method == 'POST':  # Check for POST method
        form = DashBoardForm(request.POST)
        if form.is_valid():  # Validate the form
            text = form.cleaned_data['text']
            video = VideosSearch(text, limit=10)

            for i in video.result().get('result', []):
                result_dict = {
                    'input': text,
                    'title': i['title'],
                    'duration': i['duration'],
                    'thumbnail': i['thumbnails'][0]['url'],
                    'channel': i['channel']['name'],
                    'link': i['link'],
                    'views': i['viewCount']['short'],
                    'published': i['publishedTime'],
                }
                desc = ''
                if 'descriptionSnippet' in i and i['descriptionSnippet']:
                    desc = ''.join(j['text'] for j in i['descriptionSnippet'])
                    result_dict['description'] = desc

                result_list.append(result_dict)

            context = {
                'form': form,
                'results': result_list
            }
            return render(request, 'dashboard/youtube.html', context)

    # For GET request or invalid POST
    context = {'form': form, 'results': result_list}  # Pass empty results for GET
    return render(request, 'dashboard/youtube.html', context)


def todo(request):
    if request.method == 'POST':  # Correctly check the request method
        form = TodoForm(request.POST)
        if form.is_valid():
            # Safely get the value for is_finished
            finished = request.POST.get('is_finished') == 'on'  # True if checked, else False

            # Create and save the new todo
            new_todo = Todo(
                user=request.user,
                title=form.cleaned_data['title'],  # Use cleaned data from the form
                is_finished=finished  # Correct spelling
            )
            new_todo.save()
            messages.success(request, f'Todo added from {request.user.username}!!')
            return redirect('todo')  # Redirect after POST to prevent resubmission

    else:
        form = TodoForm()
    
    todos = Todo.objects.filter(user=request.user)
    todos_done = len(todos) == 0  # Use boolean directly based on length

    context = {
        'form': form,
        'todos': todos,
        'todos_done': todos_done
    }
    return render(request, 'dashboard/todo.html', context)
