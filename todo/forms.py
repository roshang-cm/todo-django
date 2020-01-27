from django import forms
from todo.constants import STATUS_CHOICES


class AddTodoForm(forms.Form):
    todo_text = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': 'Enter the todo text'}))


class ChangeStatusForm(forms.Form):
    status = forms.ChoiceField(choices=STATUS_CHOICES)
