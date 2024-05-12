from django.db import models  
from django.contrib.auth.models import User, AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique

    class Meta:
        permissions = []

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_users_groups',  # Unique related name for groups
        related_query_name='custom_user_group',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_users_permissions',  # Unique related name for user permissions
        related_query_name='custom_user_permission',
        help_text='Specific permissions for this user.',
    )

class IncomeCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    
class Token(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    token = models.CharField(max_length=48)
    def __str__(self):
        return "{}-token".format(self.user)

class BankAccount(models.Model):
    name = models.CharField(max_length=100)
    balance = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}".format(self.name, self.balance)

class Income(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateField()
    amount = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}".format(self.amount, self.date)

class Expense(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateField()
    amount = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE,null=True)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE,null=True)  # ForeignKey to BankAccount model

    def __str__(self):
        return "{}-{}-{}".format(self.amount, self.bank_account, self.date)

class MonthlyExpense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.BigIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)  # ForeignKey to BankAccount model
    
    def __str__(self):
        return "{}-{}".format(self.name, self.amount)