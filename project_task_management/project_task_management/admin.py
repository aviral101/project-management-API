from django.contrib import admin
from .models import User, Role, Project, Task

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Project)
admin.site.register(Task)