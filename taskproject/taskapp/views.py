from django.shortcuts import render,redirect
from .forms import TaskForm
from django.contrib.auth.decorators import login_required 
@login_required
def create_task(request):
    form=TaskForm()
    if request.method == "POST":
        form=TaskForm(request.POST)
        if form.is_valid():
            task=form.save(commit=False)
            task.user=request.user
            task.save()
            return redirect('task_list')
    return render(request,'create_task.html',{'form':form})

from .models import Task
@login_required
def task_list(request):
    tasks=Task.objects.filter(user=request.user)
    return render(request,'task_list.html',{'tasks':tasks})

@login_required
def update_task(request,id):
    task = Task.objects.get(id=id)
    form=TaskForm(instance=task)
    if request.method=="POST":
        form=TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    return render(request,'create_task.html',{'form':form})

@login_required
def delete_task(request,id):
    task=Task.objects.get(id=id)
    if request.method=="POST":
        task.delete()
        return redirect("task_list")
    return render(request,'delete_task.html',{'task':task})

@login_required
def delete_account(request):
    if request.method=="POST":
        user=request.user
        logout(request)
        user.delete()
        return redirect('signup_page')
    return render(request,'delete_account.html')

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout 

def signup_page(request):
    form = UserCreationForm()
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('task_list')
    return render(request,'signup.html',{'form':form})

def login_page(request):
    form=AuthenticationForm()
    if request.method=="POST":
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('task_list')
    return render(request,'login.html',{'form':form})

def logout_page(request):
    logout(request)
    return redirect('login_page')


#API

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TaskSerializer

@api_view(['GET','POST'])
def api_task_list(request,task_id=None):
    if request.method=='GET':
        #task_id=request.GET.get('task_id')
        if task_id:
            task=Task.objects.get(id=task_id)
            serializer=TaskSerializer(task)
        else:
            tasks=Task.objects.all()
            serializer=TaskSerializer(tasks,many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=TaskSerializer(data=request.data)
        if serializer.is_valid():
          #serializer.save(user=request.user)
          serializer.save()
          return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['PUT'])
def api_update_task(request,task_id):
    task=Task.objects.get(id=task_id)
    serializer=TaskSerializer(task,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['DELETE'])
def api_delete_task(request,task_id):
    task=Task.objects.get(id=task_id)
    task.delete()
    return Response("Task Deleted")




 






