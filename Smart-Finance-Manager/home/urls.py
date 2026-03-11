from django.urls import path, include
from home.views import *

urlpatterns = [
    # Authentication URLs
    path('signup/', signup, name='signuppage'),
    path('', login_view, name='loginpage'),
    path('logout/', logout_view, name='logoutpage'),
    
    # Main application URLs
    # path('', finance, name='financepage'),
    path('home/', home, name='homepage'),
    path('transcations/', transcation, name='transcationpage'),
    path('transcations/download-pdf/', download_transactions_pdf, name='download_pdf'),
    path('receipts/', receipts_gallery, name='receiptspage'),
    path('pricing/', pricing, name='pricingpage'),
    path('analytics/', analytics, name='analyticspage'),
    
    # Recurring Expenses URLs
    path('recurring/', recurring_expenses, name='recurring_expenses'),
    path('recurring/add/', add_recurring_expense, name='add_recurring'),
    path('recurring/delete/<int:expense_id>/', delete_recurring_expense, name='delete_recurring'),
    path('api/recurring-alerts/', get_recurring_alerts, name='recurring_alerts'),
    path('api/process-recurring/', process_recurring_payments, name='process_recurring'),
    
    # API endpoints
    path('api/voice-expense/', process_voice_expense, name='voice_expense'),
    path('api/set-ai-key/', set_ai_api_key, name='set_ai_key'),
]
