from django.shortcuts import render,render
from django.http import HttpResponse
from youtubesearchpython import VideosSearch
import requests
import wikipedia
import wikipediaapi
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

def update_todo(request, pk):
    todo = get_object_or_404(Todo, id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

def delete_todo(request,pk):
    todo = get_object_or_404(Todo, id=pk)
    todo.delete()
    return redirect('todo')

def books(request):
    form = DashBoardForm()
    context ={
        'form':form
    }
    return render(request,'dashboard/books.html',context)


# def books(request):
#     form = DashBoardForm()  # Initialize the form at the start
#     result_list = []

#     if request.method == 'POST':  # Check for POST method
#         form = DashBoardForm(request.POST)
#         if form.is_valid():  # Validate the form
#             text = form.cleaned_data['text']
#             url ="https://www.googleapis.com/books/v1/volumes?q="+text
#             r = requests.get(url)
#             answer = r.json()
#             for i in range(10):
#                 result_dict = {
#                     'title': answer['items'][i]['volumeInfo']['title'],
#                     'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
#                     'description': answer['items'][i]['volumeInfo'].get('description'),
#                     'count': answer['items'][i]['volumeInfo'].get('pageCount'),
#                     'categories': answer['items'][i]['volumeInfo'].get('categories'),
#                     'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
#                     'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks'),
#                     'preview': answer['items'][i]['volumeInfo'].get('previewLink'),    
#                 }
                
#                 result_list.append(result_dict)

#             context = {
#                 'form': form,
#                 'results': result_list
#             }
#             return render(request, 'dashboard/books.html', context)

#     # For GET request or invalid POST
#     context = {'form': form}  # Pass empty results for GET
#     return render(request, 'dashboard/books.html', context)

def books(request):
    form = DashBoardForm()  # Initialize the form at the start
    result_list = []

    if request.method == 'POST':  # Check for POST method
        form = DashBoardForm(request.POST)
        if form.is_valid():  # Validate the form
            text = form.cleaned_data['text']
            url = "https://www.googleapis.com/books/v1/volumes?q=" + text
            r = requests.get(url)
            answer = r.json()
            for i in range(min(10, len(answer.get('items', [])))):  # Safeguard against fewer than 10 items
                volume_info = answer['items'][i]['volumeInfo']
                thumbnail_url = volume_info.get('imageLinks')
                
                # Check if thumbnail_url is not None and has a thumbnail
                if thumbnail_url and 'thumbnail' in thumbnail_url:
                    thumbnail_url = thumbnail_url['thumbnail']
                else:
                    thumbnail_url = 'path/to/default/image.jpg'  # Path to a default image if no thumbnail

                result_dict = {
                    'title': volume_info['title'],
                    'subtitle': volume_info.get('subtitle'),
                    'description': volume_info.get('description'),
                    'count': volume_info.get('pageCount'),
                    'categories': volume_info.get('categories'),
                    'rating': volume_info.get('averageRating'),  # Corrected to 'averageRating'
                    'thumbnail': thumbnail_url,
                    'preview': volume_info.get('previewLink'),
                }
                
                result_list.append(result_dict)

            context = {
                'form': form,
                'results': result_list
            }
            return render(request, 'dashboard/books.html', context)

    # For GET request or invalid POST
    context = {'form': form}  # Pass empty results for GET
    return render(request, 'dashboard/books.html', context)


# def dictionary(request):
#     if request.method == 'POST':  # Check for POST method
#         form = DashBoardForm(request.POST)
#         if form.is_valid():  # Validate the form
#             text = form.cleaned_data['text']
#             url = "https://api.dictionaryapi.dev/api/v2/entries/en_US?q=" + text
#             r = requests.get(url)
#             answer = r.json()
#             try:
#                 phonetics =answer[0]['phonetics']['texts'],
#                 audio =answer[0]['phonetics'][0]['audio'],
#                 definition =answer[0]['meanings'][0]['definitions'][0]['definition'],
#                 example =answer[0]['meanings'][0]['definitions'][0]['example'],
#                 synonyms =answer[0]['meanings'][0]['definitions'][0]['synonyms']
#                 context ={
#                     'form' : form,
#                     'input' :text,
#                     'phonetics':phonetics,
#                     'audio':audio,
#                     'definition':definition,
#                     'example':example,
#                     'synonyms':synonyms
                    
#                 }
#             except:
#                 context={
#                     'form':form,
#                     'input':""
#                 }
#             return render(request, 'dashboard/dictionary.html', context)
#         else:
#             form = DashBoardForm() 
#             context={'form':form}
#     return render(request, 'dashboard/dictionary.html', context)


import requests
from django.shortcuts import render
from .form import DashBoardForm  # Adjust according to your project structure

def dictionary(request):
    form = DashBoardForm()
    context = {'form': form}

    if request.method == 'POST':
        form = DashBoardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{text}"
            r = requests.get(url)

            if r.status_code == 200:
                try:
                    answer = r.json()
                    
                    # Extract phonetics
                    phonetics = answer[0]['phonetics'][0]['text'] if answer[0]['phonetics'] else 'No phonetics available.'
                    audio = answer[0]['phonetics'][0].get('audio', '')

                    # Extract definitions and examples
                    definitions = answer[0]['meanings'][0]['definitions']
                    if definitions:
                        definition = definitions[0].get('definition', 'No definition available.')
                        example = definitions[0].get('example', 'No example available.')
                        synonyms = definitions[0].get('synonyms', [])
                    else:
                        definition = 'No definition available.'
                        example = 'No example available.'
                        synonyms = []

                    context.update({
                        'input': text,
                        'phonetics': phonetics,
                        'audio': audio,
                        'definition': definition,
                        'example': example,
                        'synonyms': synonyms,
                    })
                except (ValueError, IndexError) as e:
                    context['error'] = f"Error parsing data: {str(e)}"
            else:
                context['error'] = f"Error: Received status code {r.status_code}"

    return render(request, 'dashboard/dictionary.html', context)


def wiki(request):
    if request.method == 'POST':
        text=request.POST['text']
        form = DashBoardForm(request.POST)
        search = wikipedia.page(text)
        context ={
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,'dashboard/wiki.html',context)
    else:
        form =DashBoardForm()
        context={
            'form':form
        }
    return render(request,'dashboard/wiki.html',context)