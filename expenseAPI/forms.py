from typing import Required
from django import forms
from django.forms import ModelForm
from .models import Expense

class ExpenseForm(ModelForm):
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}))

    class Meta:
        model = Expense
        fields = ['name', 'type', 'amount', 'category', 'date']

        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}