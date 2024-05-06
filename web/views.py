from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from web.models import User, Token, Expense, Income, IncomeCategory, ExpenseCategory, BankAccount, MonthlyExpense
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import BankAccount
from .forms import BankAccountForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm

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
    
    # List expenses
def list_expenses(request):
    if request.method == 'GET':
        try:
            this_token = request.GET['token']
            this_user = User.objects.filter(token__token=this_token).get()
            expenses = Expense.objects.filter(user=this_user)
            data = serializers.serialize('json', expenses)
            return JsonResponse(data, safe=False)
        except (KeyError, Token.DoesNotExist, User.DoesNotExist):
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid or expired token.',
            }, status=400)

# List incomes
def list_incomes(request):
    if request.method == 'GET':
        try:
            this_token = request.GET['token']
            this_user = User.objects.filter(token__token=this_token).get()
            incomes = Income.objects.filter(user=this_user)
            data = serializers.serialize('json', incomes)
            return JsonResponse(data, safe=False)
        except (KeyError, Token.DoesNotExist, User.DoesNotExist):
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid or expired token.',
            }, status=400)

# Update expense
@csrf_exempt
def update_expense(request, expense_id):
    if request.method == 'POST':
        try:
            this_token = request.POST['token']
            this_user = User.objects.filter(token__token=this_token).get()
            expense = get_object_or_404(Expense, pk=expense_id, user=this_user)
            expense.amount = request.POST['amount']
            expense.text = request.POST['text']
            expense.date = request.POST['date']
            expense.save()
            return JsonResponse({'status': 'ok'}, encoder=JSONEncoder)
        except (KeyError, Token.DoesNotExist, User.DoesNotExist, Expense.DoesNotExist):
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid or expired token or expense ID.',
            }, status=400)

# Update income
@csrf_exempt
def update_income(request, income_id):
    if request.method == 'POST':
        try:
            this_token = request.POST['token']
            this_user = User.objects.filter(token__token=this_token).get()
            income = get_object_or_404(Income, pk=income_id, user=this_user)
            income.amount = request.POST['amount']
            income.text = request.POST['text']
            income.date = request.POST['date']
            income.save()
            return JsonResponse({'status': 'ok'}, encoder=JSONEncoder)
        except (KeyError, Token.DoesNotExist, User.DoesNotExist, Income.DoesNotExist):
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid or expired token or income ID.',
            }, status=400)

# Delete expense
@csrf_exempt
def delete_expense(request, expense_id):
    if request.method == 'POST':
        try:
            this_token = request.POST['token']
            this_user = User.objects.filter(token__token=this_token).get()
            expense = get_object_or_404(Expense, pk=expense_id, user=this_user)
            expense.delete()
            return JsonResponse({'status': 'ok'}, encoder=JSONEncoder)
        except (KeyError, Token.DoesNotExist, User.DoesNotExist, Expense.DoesNotExist):
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid or expired token or expense ID.',
            }, status=400)

# Delete income
@csrf_exempt
def delete_income(request, income_id):
    if request.method == 'POST':
        try:
            this_token = request.POST['token']
            this_user = User.objects.filter(token__token=this_token).get()
            income = get_object_or_404(Income, pk=income_id, user=this_user)
            income.delete()
            return JsonResponse({'status': 'ok'}, encoder=JSONEncoder)
        except (KeyError, Token.DoesNotExist, User.DoesNotExist, Income.DoesNotExist):
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid or expired token or income ID.',
            }, status=400)

# List income categories
def list_income_categories(request):
    if request.method == 'GET':
        try:
            income_categories = IncomeCategory.objects.all()
            data = serializers.serialize('json', income_categories)
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)

# List expense categories
def list_expense_categories(request):
    if request.method == 'GET':
        try:
            expense_categories = ExpenseCategory.objects.all()
            data = serializers.serialize('json', expense_categories)
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)

# List tokens
def list_tokens(request):
    if request.method == 'GET':
        try:
            tokens = Token.objects.all()
            data = serializers.serialize('json', tokens)
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)

# List bank accounts
def list_bank_accounts(request):
    try:
        bank_accounts = BankAccount.objects.all()
        return render(request, 'dashboard.html', {'bank_accounts': bank_accounts})
    except Exception as e:
        return render(request, 'dashboard.html', {'error_message': str(e)})

# List monthly expenses
def list_monthly_expenses(request):
    if request.method == 'GET':
        try:
            monthly_expenses = MonthlyExpense.objects.all()
            data = serializers.serialize('json', monthly_expenses)
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)

# Submit income category
@csrf_exempt
def submit_income_category(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            income_category = IncomeCategory.objects.create(name=name)
            return JsonResponse({
                'status': 'ok',
                'income_category_id': income_category.id,
            }, encoder=JSONEncoder)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Only POST requests are allowed.',
        }, status=405)

# Submit expense category
@csrf_exempt
def submit_expense_category(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            expense_category = ExpenseCategory.objects.create(name=name)
            return JsonResponse({
                'status': 'ok',
                'expense_category_id': expense_category.id,
            }, encoder=JSONEncoder)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Only POST requests are allowed.',
        }, status=405)

# Update token
@csrf_exempt
def update_token(request, token_id):
    if request.method == 'POST':
        try:
            token = Token.objects.get(pk=token_id)
            token.token = request.POST['token']
            token.save()
            return JsonResponse({'status': 'ok'}, encoder=JSONEncoder)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)

# Update bank account
@csrf_exempt
def update_bank_account(request, account_id):
    if request.method == 'POST':
        try:
            bank_account = BankAccount.objects.get(pk=account_id)
            bank_account.name = request.POST['name']
            bank_account.balance = request.POST['balance']
            bank_account.save()
            return JsonResponse({'status': 'ok'}, encoder=JSONEncoder)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)

# Update monthly expense
@csrf_exempt
def update_monthly_expense(request, expense_id):
    if request.method == 'POST':
        try:
            monthly_expense = MonthlyExpense.objects.get(pk=expense_id)
            monthly_expense.name = request.POST['name']
            monthly_expense.amount = request.POST['amount']
            monthly_expense.start_date = request.POST['start_date']
            monthly_expense.end_date = request.POST['end_date']
            monthly_expense.save()
            return JsonResponse({'status': 'ok'}, encoder=JSONEncoder)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)

# Delete income category
@csrf_exempt
def delete_income_category(request, category_id):
    if request.method == 'POST':
        try:
            income_category = IncomeCategory.objects.get(pk=category_id)
            income_category.delete()
            return JsonResponse({'status': 'ok'}, encoder=JSONEncoder)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)

# Delete expense category
@csrf_exempt
def delete_expense_category(request, category_id):
    if request.method == 'POST':
        try:
            expense_category = ExpenseCategory.objects.get(pk=category_id)
            expense_category.delete()
            return JsonResponse({'status': 'ok'}, encoder=JSONEncoder)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)

# Delete token
@csrf_exempt
def delete_token(request, token_id):
    if request.method == 'POST':
        try:
            token = Token.objects.get(pk=token_id)
            token.delete()
            return JsonResponse({'status': 'ok'}, encoder=JSONEncoder)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)

# Delete bank account
@csrf_exempt
def delete_bank_account(request, account_id):
    if request.method == 'POST':
        try:
            bank_account = BankAccount.objects.get(pk=account_id)
            bank_account.delete()
            return JsonResponse({'status': 'ok'}, encoder=JSONEncoder)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)

# Delete monthly expense
@csrf_exempt
def delete_monthly_expense(request, expense_id):
    if request.method == 'POST':
        try:
            monthly_expense = MonthlyExpense.objects.get(pk=expense_id)
            monthly_expense.delete()
            return JsonResponse({'status': 'ok'}, encoder=JSONEncoder)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after successful login
        else:
            storage = messages.get_messages(request)
            storage.used = True
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate a password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # Send password reset email
            reset_link = request.build_absolute_uri(f'/reset_password/{uid}/{token}/')
            print(reset_link)
            subject = 'Password Reset Request'
            message = render_to_string('reset_password_email.html', {'reset_link': reset_link})
            send_mail(subject, message, 'from@example.com', [user.email])
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('login')  # Redirect to login page
        except User.DoesNotExist:
            messages.error(request, 'This email is not associated with any account.')
    return render(request, 'forgot_password.html')

def reset_password(request, uidb64, token):
    try:
        # Decode the user ID from base64
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Token is valid, allow user to reset password
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been reset successfully.')
                return render(request, 'password_reset_done.html')
        else:
            form = SetPasswordForm(user)
        return render(request, 'reset_password.html', {'form': form})
    else:
        # Token is invalid, show error message
        messages.error(request, 'The reset password link is invalid or has expired.')
        return render(request, 'password_reset_failed.html')
    
def create_account(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # If the form is valid, save the user's data
            form.save()
            # Authenticate and login the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Your account has been created successfully!')
                return redirect('dashboard')  # Redirect to dashboard after successful login
        else:
            # If the form is not valid, display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        # If it's a GET request, render the form
        form = UserCreationForm()
    return render(request, 'create_account.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

def dashboard(request):
    # Add logic to fetch data for the dashboard
    return render(request, 'dashboard.html')

def add_bank_account(request):
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bank account added successfully.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Failed to add bank account. Please check the form.')
    else:
        form = BankAccountForm()
    return render(request, 'add_bank_account.html', {'form': form})

def edit_bank_account(request):
    # Get the bank account object by primary key (pk)
    bank_account = get_object_or_404(BankAccount)

    if request.method == 'POST':
        # Populate the form with the existing bank account data
        form = BankAccountForm(request.POST, instance=bank_account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bank account updated successfully.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Failed to update bank account. Please check the form.')
    else:
        # Create a form instance with the existing bank account data
        form = BankAccountForm(instance=bank_account)
    return render(request, 'edit_bank_account.html', {'form': form})