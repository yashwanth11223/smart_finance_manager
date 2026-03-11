"""
Smart expense analysis and suggestions
Uses rule-based logic - no API needed, completely free!
"""
from decimal import Decimal
from datetime import datetime, timedelta
from collections import defaultdict


def analyze_expenses_with_ai(transactions, account, api_key=None, use_gemini=False):
    """
    Analyze expenses using smart rule-based logic (no API needed).
    
    Args:
        transactions: QuerySet of Transaction objects
        account: UserExpenseAccount object
        api_key: Not used (kept for compatibility)
        use_gemini: Not used (kept for compatibility)
    
    Returns:
        dict with smart suggestions and insights
    """
    # Prepare expense data
    expense_data = prepare_expense_data(transactions)
    
    # Detect anomalies
    anomalies = detect_anomalies(transactions)
    
    # Generate rule-based suggestions
    insights = generate_rule_based_suggestions(expense_data, account, anomalies)
    
    return insights


def prepare_expense_data(transactions):
    """Prepare expense data for analysis."""
    data = {
        'total_expenses': Decimal('0'),
        'by_category': defaultdict(Decimal),
        'by_week': defaultdict(Decimal),
        'expense_count': 0,
        'average_expense': Decimal('0'),
        'last_7_days': Decimal('0'),
        'last_30_days': Decimal('0'),
    }
    
    now = datetime.now()
    last_7_days = now - timedelta(days=7)
    last_30_days = now - timedelta(days=30)
    
    expenses = transactions.filter(transaction_type='expense')
    
    for transaction in expenses:
        amount = transaction.amount
        data['total_expenses'] += amount
        data['expense_count'] += 1
        
        # Category breakdown
        category = getattr(transaction, 'category', 'Other')
        data['by_category'][category] += amount
        
        # Time-based breakdown
        if transaction.created_at.replace(tzinfo=None) >= last_7_days:
            data['last_7_days'] += amount
        if transaction.created_at.replace(tzinfo=None) >= last_30_days:
            data['last_30_days'] += amount
        
        # Weekly breakdown
        week_num = transaction.created_at.isocalendar()[1]
        data['by_week'][f'Week {week_num}'] += amount
    
    if data['expense_count'] > 0:
        data['average_expense'] = data['total_expenses'] / data['expense_count']
    
    return data


def detect_anomalies(transactions):
    """Detect unusual spending patterns (anomalies)."""
    anomalies = []
    
    expenses = transactions.filter(transaction_type='expense').order_by('-created_at')
    
    if expenses.count() < 5:
        return anomalies
    
    # Calculate average
    amounts = [float(e.amount) for e in expenses]
    avg = sum(amounts) / len(amounts)
    
    # Simple anomaly: expenses > 2x average
    threshold = avg * 2
    
    for expense in expenses[:10]:  # Check last 10 expenses
        if float(expense.amount) > threshold:
            anomalies.append({
                'amount': expense.amount,
                'description': expense.description or 'Expense',
                'date': expense.created_at.strftime('%d %b %Y'),
                'category': getattr(expense, 'category', 'Other'),
                'message': f'Unusually high expense: ₹{expense.amount} (Avg: ₹{avg:.2f})'
            })
    
    return anomalies


def generate_rule_based_suggestions(expense_data, account, anomalies):
    """Generate smart suggestions based on spending patterns."""
    tips = []
    warnings = []
    praise = []
    overspending_categories = []
    budget_suggestions = {}
    
    # Calculate percentages
    if account.total_amount > 0:
        expense_percentage = (float(expense_data['total_expenses']) / float(account.total_amount)) * 100
    else:
        expense_percentage = 0
    
    # 1. Overall Spending Rate Analysis
    if expense_percentage > 70:
        warnings.append(f"🚨 You've spent {expense_percentage:.1f}% of your total funds!")
        tips.append("Try to reduce daily expenses by 15-20% to stay within budget")
    elif expense_percentage > 50:
        warnings.append(f"⚠️ Your spending is at {expense_percentage:.1f}% - watch your expenses")
        tips.append("Consider cutting non-essential expenses by 10%")
    elif expense_percentage > 0:
        praise.append(f"✅ Good job! You're spending {expense_percentage:.1f}% - keep it controlled")
    
    # 2. Category-wise Analysis
    total_exp = float(expense_data['total_expenses'])
    if total_exp > 0:
        for category, amount in expense_data['by_category'].items():
            cat_amount = float(amount)
            cat_percentage = (cat_amount / total_exp) * 100
            
            # Identify overspending categories (>30% of total)
            if cat_percentage > 30:
                overspending_categories.append(category)
                warnings.append(f"{category} is {cat_percentage:.0f}% of your total spending")
                
                # Category-specific tips
                if category == 'Food':
                    tips.append("🍔 Try meal planning and cooking at home to save 20-30% on food")
                    budget_suggestions[category] = f"₹{cat_amount * 0.7:.0f} (reduce by 30%)"
                elif category == 'Shopping':
                    tips.append("🛍️ Use the 30-day rule: wait 30 days before buying non-essentials")
                    budget_suggestions[category] = f"₹{cat_amount * 0.6:.0f} (reduce by 40%)"
                elif category == 'Entertainment':
                    tips.append("🎬 Look for free events or share subscription costs with family")
                    budget_suggestions[category] = f"₹{cat_amount * 0.7:.0f} (reduce by 30%)"
                elif category == 'Transport':
                    tips.append("🚗 Consider carpooling or public transport for daily commute")
                    budget_suggestions[category] = f"₹{cat_amount * 0.8:.0f} (reduce by 20%)"
                else:
                    tips.append(f"Review your {category} expenses and identify savings opportunities")
                    budget_suggestions[category] = f"₹{cat_amount * 0.8:.0f} (reduce by 20%)"
    
    # 3. Small Frequent Expenses Detection
    if expense_data['expense_count'] > 0:
        avg_exp = float(expense_data['average_expense'])
        if avg_exp < 200 and expense_data['expense_count'] > 10:
            tips.append("☕ Small expenses add up! Track daily coffee/snacks - can save ₹2000+/month")
    
    # 4. Weekly Trend Analysis
    if expense_data['last_7_days'] > 0 and expense_data['expense_count'] > 7:
        daily_avg = float(expense_data['last_7_days']) / 7
        monthly_projection = daily_avg * 30
        warnings.append(f"📈 At current rate, you'll spend ₹{monthly_projection:.0f} this month")
    
    # 5. Anomaly Warnings
    if anomalies:
        warnings.append(f"⚡ Found {len(anomalies)} unusually high expenses - review them!")
        tips.append("Check your high-value transactions to identify one-time vs recurring expenses")
    
    # 6. Savings Goal Progress
    if account.target_amount > 0:
        target_progress = (float(account.current_balance) / float(account.target_amount)) * 100
        if target_progress >= 100:
            praise.append(f"🎉 Congratulations! You've achieved your savings goal of ₹{account.target_amount}!")
        elif target_progress >= 75:
            remaining = float(account.target_amount - account.current_balance)
            praise.append(f"🏃 You're {target_progress:.0f}% to your goal! Just ₹{remaining:.0f} more!")
        elif target_progress >= 50:
            praise.append(f"💪 Halfway to your ₹{account.target_amount} goal - keep going!")
        else:
            remaining = float(account.target_amount - account.current_balance)
            tips.append(f"🎯 Save ₹{remaining:.0f} more to reach your target")
    
    # 7. General Smart Tips (if not enough specific tips)
    default_tips = [
        "💡 Follow the 50/30/20 rule: 50% needs, 30% wants, 20% savings",
        "📝 Review your subscriptions - cancel unused ones",
        "🏦 Set up automatic savings transfers on payday",
        "🛒 Make a shopping list and stick to it to avoid impulse buys",
        "💳 Use cash for daily expenses to better control spending",
    ]
    
    # Add default tips if we don't have enough
    while len(tips) < 4 and default_tips:
        tips.append(default_tips.pop(0))
    
    # Create summary
    summary = f"Total spending: ₹{expense_data['total_expenses']} across {expense_data['expense_count']} transactions. "
    if expense_data['expense_count'] > 0:
        summary += f"Average: ₹{expense_data['average_expense']:.0f}. "
    if anomalies:
        summary += f"⚠️ {len(anomalies)} high-value expenses detected. "
    if expense_percentage > 60:
        summary += "Consider reducing expenses!"
    else:
        summary += "Keep up the good spending habits!"
    
    return {
        'summary': summary,
        'tips': tips[:5],  # Top 5 tips
        'overspending': overspending_categories,
        'budget_suggestions': budget_suggestions,
        'warnings': warnings[:5],  # Top 5 warnings
        'praise': praise[:3],  # Top 3 praises
        'anomalies': anomalies,
        'category_breakdown': dict(expense_data['by_category']),
    }
