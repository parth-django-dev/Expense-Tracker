from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from .forms import ExpenseForm
from .models import Expense

@login_required
def addExpense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            if not expense.date:
                expense.date = timezone.now().date()
            expense.save()
            return redirect('show_expenses')
    else:
        form = ExpenseForm()

    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    # Fetch unique categories for this user
    categories = Expense.objects.filter(user=request.user).values_list('category', flat=True).distinct()

    # Time filter
    timeframe = request.GET.get('timeframe', 'all')
    curtime = timezone.now().date()

    # Note the double underscores (__) below:
    if timeframe == "Last Week":
        expenses = expenses.filter(date__gte=curtime - timedelta(days=7))
    elif timeframe == "Last Month":
        expenses = expenses.filter(date__gte=curtime - timedelta(days=30))
    elif timeframe == "Last 6 Months":
        expenses = expenses.filter(date__gte=curtime - timedelta(days=180))
    elif timeframe == "Last Year":
        expenses = expenses.filter(date__gte=curtime - timedelta(days=365))

    # Category filter 
    selected_category = request.GET.get('category', 'all')
    if selected_category != 'all' and selected_category:
        expenses = expenses.filter(category=selected_category)

    # Calculating totals on the filtered query
    total_income = expenses.filter(type="I").aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expenses.filter(type="E").aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    return render(request, 'show_expenses.html', {
        'form': form,
        'expenses': expenses,
        'categories': categories,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'selected_timeframe': timeframe,
        'selected_category': selected_category
    })

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == "POST":
        expense.delete()
    
    return redirect('show_expenses')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('show_expenses')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
