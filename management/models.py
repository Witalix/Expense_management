from django.db import models

from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(blank=True, null=True)
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # This should be here
    category_name = models.CharField(max_length=100, blank=True)  # Nowe pole

    def save(self, *args, **kwargs):
        if self.category:
            self.category_name = self.category.name
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.description} - {self.amount} USD"



class Budget(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Powiązanie z użytkownikiem
    categories = models.ManyToManyField(Category)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.amount} USD"


class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Powiązanie z użytkownikiem

    def __str__(self):
        return f"{self.description} - {self.amount} USD"

class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category)
    last_added_expense = models.OneToOneField(Expense, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # This should be in your model

    def __str__(self):
        return self.name


class Savings(models.Model):
    goal_name = models.CharField(max_length=255)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.goal_name} - {self.current_amount}/{self.goal_amount} USD"
