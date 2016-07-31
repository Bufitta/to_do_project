#coding=utf-8
from django import forms

class ToDoForm(forms.Form):
    work_title = forms.CharField(label='Дело', max_length=100)