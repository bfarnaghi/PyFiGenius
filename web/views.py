from django.shortcuts import render
from django.http import JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from web.models import User, Token, Expense, Income
from datetime import datetime

@csrf_exempt
def submit_expense(request):
    if request.method == 'POST':
        try:
            this_token = request.POST['token']
            this_user = User.objects.filter(token__token=this_token).get()
        except (KeyError, Token.DoesNotExist, User.DoesNotExist):
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid or expired token.',
            }, status=400)

        if 'amount' not in request.POST or 'text' not in request.POST:
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required fields.',
            }, status=400)

        try:
            amount = float(request.POST['amount'])
        except ValueError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid amount format.',
            }, status=400)

        date = request.POST.get('date', datetime.now())
        try:
            expense = Expense.objects.create(
                user=this_user,
                amount=amount,
                text=request.POST['text'],
                date=date
            )
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)

        return JsonResponse({
            'status': 'ok',
            'expense_id': expense.id,
        }, encoder=JSONEncoder)

    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Only POST requests are allowed.',
        }, status=405)

@csrf_exempt
def submit_income(request):
    if request.method == 'POST':
        try:
            this_token = request.POST['token']
            this_user = User.objects.filter(token__token=this_token).get()
        except (KeyError, Token.DoesNotExist, User.DoesNotExist):
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid or expired token.',
            }, status=400)

        if 'amount' not in request.POST or 'text' not in request.POST:
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required fields.',
            }, status=400)

        try:
            amount = float(request.POST['amount'])
        except ValueError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid amount format.',
            }, status=400)

        date = request.POST.get('date', datetime.now())
        try:
            income = Income.objects.create(
                user=this_user,
                amount=amount,
                text=request.POST['text'],
                date=date
            )
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)

        return JsonResponse({
            'status': 'ok',
            'expense_id': income.id,
        }, encoder=JSONEncoder)

    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Only POST requests are allowed.',
        }, status=405)