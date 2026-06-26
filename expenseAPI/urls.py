from django.urls import path
from . import views

urlpatterns = [
    path('',views.addExpense,name='show_expenses'),
    path('delete/<int:pk>/',views.delete_expense,name='delete_expense'),
]
