from django.http import JsonResponse
from .models import User, Role, Task, Project
from .serializers import UserSerializer, TaskSerializer, ProjectSerializer, TaskSerializer2, ProjectSerializer2
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import date
# def user_list(request):
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return JsonResponse({"users":serializer.data}, safe=False)
    
@api_view(['GET','POST'])
def tasks(request):
    if request.method == 'POST':
        # print(request)
        # return Response(status=status.HTTP_201_CREATED)
        data = request.data
        project = data['project']['projectId']
        user = data['user']['id']
        data['project'] = project
        data['user'] = user
        # print(data)
        serializer = TaskSerializer2(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("ERROR")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse({'tasks' : serializer.data}, safe=False)

@api_view(['GET','PUT','DELETE'])
def task_details(request, id):
    try:
        task = Task.objects.get(taskId = id)
    except Task.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return JsonResponse({'task':serializer.data})
    if request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        task.delete()
        return Response("Deleted",status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def projects(request):
    if request.method == 'POST':
        # print(request)
        # return Response(status=status.HTTP_201_CREATED)
        # print(request.data)
        data = request.data
        project_id = data['projectId']
        print(f'Project id : {project_id}')
        tasks = data['tasks']
        del data['tasks']
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            
            for task in tasks:
                task['user'] = task['user']['id']
                task['project'] = int(project_id)
                serializer2 = TaskSerializer2(data=task)
                # print(task)
                if serializer2.is_valid():
                    serializer2.save()
                else:
                    print(serializer2.errors)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("ERROR")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer2(projects, many=True)
        return JsonResponse({'projects' : serializer.data}, safe=False)


@api_view(['GET','PUT','DELETE'])
def project_details(request, id):
    try:
        project = Project.objects.get(projectId = id)
    except Project.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProjectSerializer2(project)
        return JsonResponse({'project':serializer.data})
    if request.method == 'PUT':
        data = request.data
        project_id = data['projectId']
        print(f'Project id : {project_id}')
        tasks = data['tasks']
        del data['tasks']
        serializer = ProjectSerializer(project, data=data)
        if serializer.is_valid():
            serializer.save()
            
            for task in tasks:
                task_id = int(task['taskId'])
                print(task_id)
                task['user'] = task['user']['id']
                task['project'] = int(project_id)
                try:
                    saved_task = Task.objects.get(taskId = task_id)
                    
                    serializer2 = TaskSerializer2(saved_task, data=task)
                    if serializer2.is_valid():
                        serializer2.save()
                    else:
                        print(serializer2.errors)
                except Task.DoesNotExist:
                    serializer2 = TaskSerializer2(data=task)
                    if serializer2.is_valid():
                        serializer2.save()
                    else:
                        print(serializer2.errors)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print("ERROR")
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        project.delete()
        return Response("deleted", status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
def in_progress_or_todo_beyond_due_date(request):
    current_date = date.today()
    tasks = Task.objects.filter(status='TODO', dueDate__lte=current_date)
    tasks2 = Task.objects.filter(status='IN_PROGRESS')
    tasks = tasks.union(tasks2)
    print(tasks2)
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse({'tasks' : serializer.data}, safe=False)


@api_view(['GET'])
def admin_tasks(request):
    users = User.objects.filter(roles__role='ADMIN')
    admin_users = list(users.values_list(flat=True))
    tasks = Task.objects.filter(user__in=admin_users)
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse({'tasks' : serializer.data}, safe=False)

@api_view(['GET'])
def task_search(request):
    task_name = request.GET.get('taskName', '')  
    tasks = Task.objects.filter(taskName__icontains=task_name)
    serializer = TaskSerializer(tasks, many=True)

    return JsonResponse({'task' : serializer.data}, safe=False)



@api_view(['GET'])
def project_tasks(request, id):
    try:
        tasks = Task.objects.filter(project = id)
    except Project.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        tasks_list = []
        for task in tasks:
            serializer = TaskSerializer(task)
            tasks_list.append(serializer.data)
        return JsonResponse({'tasks_in_project':tasks_list})