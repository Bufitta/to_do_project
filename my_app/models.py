from __future__ import unicode_literals

from django.db import models

class ToDoList(models.Model):
    number = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    work_title = models.CharField(max_length=100)