from django.db import models
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.models import User

# User Profile Model - extends Django's built-in User model
class UserProfile(models.Model):
    """
    Extended user profile to store additional user information.
    Links to Django's built-in User model via OneToOneField.
    
    Fields:
    - user: OneToOneField to Django User model
    - phone: User's contact number
    - address: User's residential address
    - city: User's city
    - profile_picture: User's profile photo
    - bio: Short bio/description
    - created_at: Account creation timestamp
    - updated_at: Last profile update timestamp
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Profile"

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


# User Expense Account Model
class UserExpenseAccount(models.Model):
    """
    Track user's financial data including balance, expenses, and savings target.
    Links to Django User model to associate expense accounts with registered users.
    
    Fields:
    - user: ForeignKey to Django User model
    - total_amount: Total amount added to account
    - current_balance: Current available balance (total - expenses)
    - target_amount: User's savings goal for the month
    - created_at: Account creation date
    - updated_at: Last update date
    
    Methods:
    - __str__: Returns user info with current balance
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='expense_account')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Balance: {self.current_balance}"

    class Meta:
        db_table = 'user_expense_account'
        verbose_name = 'User Expense Account'
        verbose_name_plural = 'User Expense Accounts'


class Transaction(models.Model):
    """
    Track all financial transactions (expenses and additions) for each user.
    
    Transaction Types:
    - 'expense': Money spent/deducted
    - 'addition': Money added/income
    
    Categories:
    - Food, Transport, Shopping, Bills, Entertainment, Health, Education, Other
    
    Fields:
    - user_account: ForeignKey to UserExpenseAccount
    - transaction_type: Type of transaction (expense or addition)
    - amount: Transaction amount
    - description: Description of the transaction
    - category: Category of expense
    - receipt_image: Receipt/photo for the transaction (optional)
    - created_at: Transaction timestamp
    
    Ordering:
    - Ordered by created_at in descending order (newest first)
    """
    TRANSACTION_TYPE = [
        ('expense', 'Expense'),
        ('addition', 'Addition'),
    ]
    
    CATEGORY_CHOICES = [
        ('Food', '🍔 Food & Dining'),
        ('Transport', '🚗 Transport'),
        ('Shopping', '🛍️ Shopping'),
        ('Bills', '💡 Bills & Utilities'),
        ('Entertainment', '🎬 Entertainment'),
        ('Health', '🏥 Health & Fitness'),
        ('Education', '📚 Education'),
        ('Other', '📦 Other'),
    ]
    
    user_account = models.ForeignKey(UserExpenseAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    receipt_image = models.ImageField(upload_to='receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user_account.user.username} - {self.transaction_type}: {self.amount}"

    class Meta:
        db_table = 'transactions'
        ordering = ['-created_at']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'


class RecurringExpense(models.Model):
    """
    Track recurring expenses like subscriptions, EMI, and loans.
    
    Expense Types:
    - 'subscription': Monthly subscriptions (Netflix, Spotify, etc.)
    - 'emi': Equated Monthly Installments
    - 'loan': Loan payments
    
    Fields:
    - user: ForeignKey to User
    - expense_type: Type of recurring expense
    - name: Name/description (e.g., "Netflix Premium", "Car Loan")
    - amount: Monthly payment amount
    - billing_date: Day of month when payment is due (1-31)
    - start_date: When this recurring expense started
    - end_date: When it ends (optional, for EMI/loans)
    - reminder_days: Days before to show reminder (default 3)
    - is_active: Whether this recurring expense is still active
    - auto_deduct: Whether to auto-create transaction on billing date
    - notes: Additional notes
    - created_at: Record creation timestamp
    
    Methods:
    - days_until_next_payment: Calculate days until next payment
    - is_due_soon: Check if payment is due within reminder_days
    - is_due_today: Check if payment is due today
    """
    EXPENSE_TYPE_CHOICES = [
        ('subscription', '📱 Subscription'),
        ('emi', '💳 EMI'),
        ('loan', '🏦 Loan'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recurring_expenses')
    expense_type = models.CharField(max_length=20, choices=EXPENSE_TYPE_CHOICES)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_date = models.IntegerField(help_text="Day of month (1-31)")  # Day of month
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True, help_text="Leave empty for subscriptions")
    reminder_days = models.IntegerField(default=3, help_text="Remind X days before due date")
    is_active = models.BooleanField(default=True)
    auto_deduct = models.BooleanField(default=False, help_text="Auto-create expense transaction on due date")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def days_until_next_payment(self):
        """Calculate days until next payment"""
        from datetime import date
        import calendar
        
        today = date.today()
        current_month = today.month
        current_year = today.year
        
        # Get the next billing date
        try:
            # Try current month first
            next_payment = date(current_year, current_month, min(self.billing_date, calendar.monthrange(current_year, current_month)[1]))
            
            # If billing date has passed this month, get next month
            if next_payment < today:
                if current_month == 12:
                    next_month = 1
                    next_year = current_year + 1
                else:
                    next_month = current_month + 1
                    next_year = current_year
                
                next_payment = date(next_year, next_month, min(self.billing_date, calendar.monthrange(next_year, next_month)[1]))
            
            return (next_payment - today).days
        except:
            return 999
    
    def is_due_soon(self):
        """Check if payment is due within reminder days"""
        days = self.days_until_next_payment()
        return 0 <= days <= self.reminder_days
    
    def is_due_today(self):
        """Check if payment is due today"""
        return self.days_until_next_payment() == 0
    
    def next_payment_date(self):
        """Get the next payment date"""
        from datetime import date
        import calendar
        
        today = date.today()
        current_month = today.month
        current_year = today.year
        
        try:
            next_payment = date(current_year, current_month, min(self.billing_date, calendar.monthrange(current_year, current_month)[1]))
            
            if next_payment < today:
                if current_month == 12:
                    next_month = 1
                    next_year = current_year + 1
                else:
                    next_month = current_month + 1
                    next_year = current_year
                
                next_payment = date(next_year, next_month, min(self.billing_date, calendar.monthrange(next_year, next_month)[1]))
            
            return next_payment
        except:
            return None
    
    def __str__(self):
        return f"{self.user.username} - {self.name} (₹{self.amount})"
    
    class Meta:
        db_table = 'recurring_expenses'
        ordering = ['billing_date']
        verbose_name = 'Recurring Expense'
        verbose_name_plural = 'Recurring Expenses'
