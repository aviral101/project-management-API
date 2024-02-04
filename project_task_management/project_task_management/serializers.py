from rest_framework import serializers
from .models import User, Role, Project, Task

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role']

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'roles']



class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['projectId', 'projectName', 'description', 'startDate', 'endDate']


class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    class Meta:
        model = Task
        fields = ['taskId', 'taskName', 'description', 'dueDate', 'status', 'user', 'project']



class TaskSerializer3(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Task
        fields = ['taskId', 'taskName', 'description', 'dueDate', 'status', 'user']


class ProjectSerializer2(serializers.ModelSerializer):
    tasks = TaskSerializer3(many=True,read_only=True)
    class Meta:
        model = Project
        fields = ['projectId', 'projectName', 'description', 'startDate', 'endDate', 'tasks']

class TaskSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['taskId', 'taskName', 'description', 'dueDate', 'status', 'user', 'project']

