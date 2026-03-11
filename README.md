# Smart Finance Manager - Complete Documentation

## 📋 Overview

Smart Finance Manager is a powerful Django web application for tracking personal expenses, managing savings goals, and monitoring financial analytics. Users can register accounts, log in securely, record expenses and additions, set savings targets, and view detailed transaction history with interactive charts.

---

## 🎯 Features

### 1. **User Authentication**
- Secure user registration (signup)
- User login with session management
- Logout functionality
- Automatic UserProfile and ExpenseAccount creation for new users

### 2. **Expense Tracking**
- Record expenses with descriptions
- Add balance/income to account
- Real-time balance updates
- Transaction history with timestamps

### 3. **Savings Goals**
- Set monthly savings targets
- Track progress towards goals
- See remaining amount to save

### 4. **Analytics & Reports**
- Interactive doughnut chart showing balance breakdown
- View all transactions with filtering
- Delete transactions (reverses the impact on balance)
- Calculate total expenses and additions

### 5. **Responsive Design**
- Mobile-friendly interface
- Bootstrap 5 styling
- Beautiful gradient backgrounds
- Smooth animations

---

## 🛠️ Technology Stack

- **Backend**: Django 5.2
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Charts**: Chart.js
- **Authentication**: Django's built-in auth system
- **Environment**: Python 3.8+

---

## 📁 Project Structure

```
mini/
├── home/
│   ├── migrations/          # Database migration files
│   ├── templates/home/      # HTML templates
│   │   ├── base.html
│   │   ├── homepage.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── transcations.html
│   │   ├── navbar.html
│   │   ├── finance.html
│   │   ├── analytics.html
│   │   └── pricing.html
│   ├── static/              # Static files (CSS, JS, images)
│   ├── admin.py             # Django admin configuration
│   ├── apps.py              # App configuration with signals
│   ├── forms.py             # Django forms for signup, login, expense
│   ├── models.py            # Database models
│   ├── signals.py           # Signal handlers for auto-creation
│   ├── urls.py              # URL routing
│   ├── views.py             # View logic
│   └── tests.py             # Unit tests
├── smart_finance/
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── manage.py                # Django management script
└── db.sqlite3               # SQLite database file
```

---

## 🗄️ Database Models

### 1. **UserProfile**
Extends Django's User model with additional user information.

```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Relationships**: 
- OneToOne with `django.contrib.auth.User`

### 2. **UserExpenseAccount**
Tracks financial data for each user.

```python
class UserExpenseAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Fields**:
- `total_amount`: Sum of all additions
- `current_balance`: total_amount - total_expenses
- `target_amount`: User's monthly savings goal

**Relationships**:
- OneToOne with `django.contrib.auth.User`
- ForeignKey from `Transaction` (reverse: `transactions`)

### 3. **Transaction**
Records all financial transactions (expenses and additions).

```python
class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('expense', 'Expense'),
        ('addition', 'Addition'),
    ]
    
    user_account = models.ForeignKey(UserExpenseAccount, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Fields**:
- `transaction_type`: Either 'expense' or 'addition'
- `amount`: Transaction amount
- `description`: Description of transaction
- `created_at`: Timestamp

**Ordering**: By `created_at` descending (newest first)

---

## 🔐 Authentication System

### Signup Process
1. User fills signup form with first name, last name, email, username, password
2. `SignUpForm` validates:
   - Password strength
   - Email uniqueness
   - Username uniqueness
3. User is created in database
4. **Signal** automatically creates:
   - `UserProfile` linked to User
   - `UserExpenseAccount` linked to User
5. User redirected to login page

### Login Process
1. User enters username and password
2. Django's `authenticate()` validates credentials
3. Session is created
4. User redirected to dashboard (homepage)

### Logout Process
1. User clicks logout
2. Session is destroyed
3. User redirected to finance page

---

## 🔄 Signal Handlers

Located in `home/signals.py`, these automatically handle data creation:

```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Creates UserProfile when new User is created"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_user_expense_account(sender, instance, created, **kwargs):
    """Creates UserExpenseAccount when new User is created"""
    if created:
        UserExpenseAccount.objects.create(user=instance)
```

---

## 📝 Forms

### 1. **SignUpForm**
Extends Django's `UserCreationForm` with additional fields.

**Fields**:
- `first_name`: User's first name
- `last_name`: User's last name
- `email`: Unique email address
- `username`: Unique username
- `password1`: Password
- `password2`: Password confirmation

**Validations**:
- Email must be unique
- Username must be unique
- Passwords must match
- Password strength requirements

### 2. **LoginForm**
Extends Django's `AuthenticationForm` with Bootstrap styling.

**Fields**:
- `username`: User's username
- `password`: User's password

### 3. **ExpenseForm**
For recording expense transactions.

**Fields**:
- `expense_amount`: Decimal amount
- `description`: Optional description

### 4. **AddAmountForm**
For adding balance to account.

**Fields**:
- `add_amount`: Decimal amount

### 5. **TargetAmountForm**
For setting monthly savings target.

**Fields**:
- `target_amount`: Decimal target amount

---

## 📄 Views Documentation

### Authentication Views

#### `signup(request)`
- **URL**: `/signup/`
- **Methods**: GET, POST
- **Requires Login**: No
- **Returns**: Renders signup form or redirects to login on success

#### `login_view(request)`
- **URL**: `/login/`
- **Methods**: GET, POST
- **Requires Login**: No
- **Returns**: Renders login form or redirects to homepage on success

#### `logout_view(request)`
- **URL**: `/logout/`
- **Methods**: GET
- **Requires Login**: No
- **Returns**: Redirects to finance page

### Dashboard Views

#### `home(request)` ⚠️ **@login_required**
- **URL**: `/home/`
- **Methods**: GET, POST
- **Features**:
  - Display expense tracking forms
  - Handle form submissions
  - Calculate analytics
  - Generate chart data
- **Context Variables**:
  - `account`: User's ExpenseAccount
  - `expense_form`: Form to add expense
  - `add_form`: Form to add balance
  - `target_form`: Form to set target
  - `last_transactions`: Last 5 transactions
  - `total_expenses`: Sum of all expenses
  - `total_additions`: Sum of all additions
  - `chart_data`: JSON for Chart.js

#### `transcation(request)` ⚠️ **@login_required**
- **URL**: `/transcations/`
- **Methods**: GET, POST
- **Features**:
  - Display all transactions
  - Handle transaction deletion
  - Reverse transaction effects on balance
- **POST Parameters**:
  - `delete_transaction`: Transaction ID to delete

#### `analytics(request)` ⚠️ **@login_required**
- **URL**: `/analytics/`
- **Methods**: GET
- **Features**:
  - Display detailed analytics
  - Calculate statistics

#### `finance(request)`
- **URL**: `/`
- **Methods**: GET
- **Features**:
  - Display landing page
  - No login required

#### `pricing(request)`
- **URL**: `/pricing/`
- **Methods**: GET
- **Features**:
  - Display pricing information

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Create Virtual Environment
```bash
python -m venv env
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install django==5.2.7
pip install pillow  # For image uploads
```

### Step 3: Navigate to Project
```bash
cd mini
```

### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Enter username, email, password
```

### Step 6: Collect Static Files (Production)
```bash
python manage.py collectstatic
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

---

## 📚 Usage Guide

### For New Users

1. **Sign Up**
   - Click "Sign Up" in navbar
   - Fill in details (first name, last name, email, username, password)
   - Click "Create Account"

2. **Login**
   - Enter username and password
   - Click "Login"
   - Redirected to dashboard

3. **Add Balance**
   - Enter amount in "Add Amount" form
   - Click "Add to Balance"
   - Balance and total_amount increase

4. **Record Expense**
   - Enter expense amount in "Add Expense" form
   - Optionally add description
   - Click "Deduct Expense"
   - Current balance decreases, transaction recorded

5. **Set Savings Goal**
   - Enter target amount in "Set Target Amount" form
   - Click "Set Target"
   - View progress on dashboard

6. **View Transactions**
   - Click "Transactions" in navbar
   - See all transactions with details
   - Delete unwanted transactions
   - Deletion reverses the transaction effect

7. **View Analytics**
   - Click "Analytics" in navbar
   - See detailed financial statistics
   - View interactive charts

---

## 🔒 Security Considerations

1. **Password Hashing**: Passwords are hashed using Django's PBKDF2 algorithm
2. **CSRF Protection**: All forms include CSRF tokens
3. **SQL Injection**: Django ORM prevents SQL injection
4. **Authentication**: Session-based authentication
5. **Login Required**: Dashboard views protected with `@login_required` decorator

---

## 🐛 Common Issues & Solutions

### Issue: "Module not found" error
**Solution**: Ensure virtual environment is activated and dependencies installed
```bash
pip install -r requirements.txt
```

### Issue: Database migrations not applied
**Solution**: Run migrations
```bash
python manage.py migrate
```

### Issue: Static files not loading
**Solution**: Collect static files
```bash
python manage.py collectstatic --noinput
```

### Issue: User created but ExpenseAccount not found
**Solution**: Signals might not be registered. Check `apps.py` has `ready()` method

---

## 📊 Database Queries Examples

### Get user's expense account:
```python
account = request.user.expense_account
```

### Get all user's transactions:
```python
transactions = account.transactions.all()
```

### Get only expenses:
```python
expenses = account.transactions.filter(transaction_type='expense')
```

### Calculate total expenses:
```python
total = sum(t.amount for t in account.transactions.filter(transaction_type='expense'))
```

### Delete a transaction and reverse its effect:
```python
transaction = Transaction.objects.get(id=1)
if transaction.transaction_type == 'expense':
    account.current_balance += transaction.amount
else:
    account.current_balance -= transaction.amount
    account.total_amount -= transaction.amount
account.save()
transaction.delete()
```

---

## 🎨 Customization

### Change Color Scheme
Edit `templates/home/homepage.html` CSS:
```css
.card-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Add New Transaction Types
Edit `models.py`:
```python
TRANSACTION_TYPE = [
    ('expense', 'Expense'),
    ('addition', 'Addition'),
    ('transfer', 'Transfer'),  # Add this
]
```

### Modify Dashboard Layout
Edit `templates/home/homepage.html` Bootstrap grid columns

---

## 📞 Support & Contact

For issues, questions, or suggestions:
- Check existing documentation
- Review Django documentation: https://docs.djangoproject.com/
- Check application logs: `python manage.py runserver`

---

## 📄 License

This project is open source and available for personal and educational use.

---

**Last Updated**: November 6, 2025  
**Version**: 1.0.0
