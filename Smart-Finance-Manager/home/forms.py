from django import forms
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


class SignUpForm(UserCreationForm):
    """
    Extended user registration form.
    
    Features:
    - Username validation (unique)
    - Email validation (unique)
    - Password strength requirements
    - Password confirmation
    - First name and last name
    
    Fields:
    - first_name: User's first name
    - last_name: User's last name
    - email: User's email address
    - username: Unique username
    - password1: Password
    - password2: Password confirmation
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style password and username fields
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

    def clean_email(self):
        """
        Validate that email is unique.
        Raises validation error if email already exists.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered!')
        return email

    def clean_username(self):
        """
        Validate that username is unique and not taken.
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken!')
        return username


class LoginForm(AuthenticationForm):
    """
    Custom login form with styled Bootstrap inputs.
    
    Fields:
    - username: User's username
    - password: User's password
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )


class UserProfileForm(forms.ModelForm):
    """
    Form to edit user profile information.
    
    Allows users to update their personal information
    like phone, address, city, and bio.
    """
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'bio')
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your city'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about yourself',
                'rows': 4
            })
        }


class ExpenseForm(forms.Form):
    """
    Form to add expense amount.
    
    Fields:
    - expense_amount: Amount to deduct as expense
    - category: Category of the expense
    - description: Description of the expense (optional)
    - receipt_image: Receipt/photo upload (optional)
    """
    expense_amount = forms.DecimalField(
        label='Expense Amount',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter expense amount',
            'step': '0.01',
            'min': '0',
            'id': 'expense_amount_input'
        })
    )
    category = forms.ChoiceField(
        label='Category',
        choices=[
            ('', '-- Select Category (Optional) --'),
            ('Food', '🍔 Food & Dining'),
            ('Transport', '🚗 Transport'),
            ('Shopping', '🛍️ Shopping'),
            ('Bills', '💡 Bills & Utilities'),
            ('Entertainment', '🎬 Entertainment'),
            ('Health', '🏥 Health & Fitness'),
            ('Education', '📚 Education'),
            ('Other', '📦 Other'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'expense_category_input'
        })
    )
    description = forms.CharField(
        label='Description',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Grocery, Transport (optional)',
            'id': 'expense_description_input'
        })
    )
    receipt_image = forms.ImageField(
        label='Receipt/Photo',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'id': 'receipt_image_input'
        })
    )


class AddAmountForm(forms.Form):
    """
    Form to add balance amount.
    
    Fields:
    - add_amount: Amount to add to balance
    """
    add_amount = forms.DecimalField(
        label='Add Amount',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount to add',
            'step': '0.01',
            'min': '0'
        })
    )


class TargetAmountForm(forms.Form):
    """
    Form to set target savings amount.
    
    Fields:
    - target_amount: Monthly savings goal amount
    """
    target_amount = forms.DecimalField(
        label='Target Savings Amount',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter target savings amount',
            'step': '0.01',
            'min': '0'
        })
    )


class RecurringExpenseForm(forms.Form):
    """
    Form to add recurring expenses (subscriptions, EMI, loans).
    
    Fields:
    - expense_type: Type of recurring expense
    - name: Name of subscription/EMI/loan
    - amount: Monthly payment amount
    - billing_date: Day of month for payment
    - start_date: Start date
    - end_date: End date (optional for subscriptions)
    - reminder_days: Days before to remind
    - auto_deduct: Auto-create expense transaction
    - notes: Additional notes
    """
    expense_type = forms.ChoiceField(
        label='Type',
        choices=[
            ('subscription', '📱 Subscription (Netflix, Spotify, etc.)'),
            ('emi', '💳 EMI (Monthly Installments)'),
            ('loan', '🏦 Loan Payment'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'expense_type_input'
        })
    )
    name = forms.CharField(
        label='Name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Netflix Premium, Car EMI, Home Loan',
            'id': 'recurring_name_input'
        })
    )
    amount = forms.DecimalField(
        label='Monthly Amount',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter monthly payment amount',
            'step': '0.01',
            'min': '0',
            'id': 'recurring_amount_input'
        })
    )
    billing_date = forms.IntegerField(
        label='Billing Date',
        min_value=1,
        max_value=31,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Day of month (1-31)',
            'min': '1',
            'max': '31',
            'id': 'billing_date_input'
        }),
        help_text='Day of month when payment is due'
    )
    start_date = forms.DateField(
        label='Start Date',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'start_date_input'
        }),
        required=False
    )
    end_date = forms.DateField(
        label='End Date',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'end_date_input'
        }),
        required=False,
        help_text='Leave empty for ongoing subscriptions'
    )
    reminder_days = forms.IntegerField(
        label='Reminder Days',
        initial=3,
        min_value=0,
        max_value=30,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '3',
            'min': '0',
            'max': '30',
            'id': 'reminder_days_input'
        }),
        help_text='Get reminder X days before due date'
    )
    auto_deduct = forms.BooleanField(
        label='Auto-create expense on due date',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'auto_deduct_input'
        })
    )
    notes = forms.CharField(
        label='Notes',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Additional notes (optional)',
            'rows': 3,
            'id': 'recurring_notes_input'
        })
    )
