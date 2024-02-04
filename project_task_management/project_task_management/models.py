from django.db import models

class User(models.Model):
    id = models.BigIntegerField(primary_key = True)
    username = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200)

    def __str__(self):
        return str(self.id) + '_' + self.username

class Role(models.Model):
    user = models.ForeignKey(User, related_name='roles', on_delete=models.CASCADE)
    role = models.CharField(max_length = 200)

    


class Project(models.Model):
    projectId = models.BigIntegerField(primary_key=True)
    projectName = models.CharField(max_length = 200)
    description = models.CharField(max_length = 1000)
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return str(self.projectId) + '_' + self.projectName


class TaskStatus(models.TextChoices):
    TODO = 'TODO', 'TODO'
    IN_PROGRESS = 'IN_PROGRESS', 'IN_PROGRESS'
    DONE = 'DONE', 'DONE'

class Task(models.Model):
    taskId = models.BigIntegerField(primary_key=True)
    taskName = models.CharField(max_length = 500)
    description = models.CharField(max_length = 1000)
    dueDate = models.DateField(null = True)
    status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.TODO)
    user = models.ForeignKey(User, null=True, related_name = 'user', on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, null=True, related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.taskId) + '_' + self.taskName

