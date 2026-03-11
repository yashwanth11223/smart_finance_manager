from django.contrib import admin
from home.models import *
# Register your models here.
admin.site.register(UserExpenseAccount)
admin.site.register(Transaction)
admin.site.register(RecurringExpense)
