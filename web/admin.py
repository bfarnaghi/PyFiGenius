from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(Token)
admin.site.register(ExpenseCategory)
admin.site.register(IncomeCategory)
admin.site.register(BankAccount)
admin.site.register(MonthlyExpense)