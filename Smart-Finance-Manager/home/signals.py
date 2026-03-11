"""
Django Signals for automatic profile and expense account creation.

When a new User is created in Django, these signals automatically:
1. Create a UserProfile linked to the User
2. Create a UserExpenseAccount linked to the User

This ensures every new user has both a profile and an expense account ready to use.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, UserExpenseAccount


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler that creates a UserProfile when a new User is created.
    
    Args:
    - sender: The model class that triggered the signal (User)
    - instance: The actual instance being saved (the new User)
    - created: Boolean indicating if this is a new instance
    - **kwargs: Additional keyword arguments
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal handler that saves the UserProfile when a User is saved.
    Ensures profile is updated whenever user data changes.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(post_save, sender=User)
def create_user_expense_account(sender, instance, created, **kwargs):
    """
    Signal handler that creates a UserExpenseAccount when a new User is created.
    This initializes an empty expense account for the new user.
    
    Args:
    - sender: The model class that triggered the signal (User)
    - instance: The actual instance being saved (the new User)
    - created: Boolean indicating if this is a new instance
    - **kwargs: Additional keyword arguments
    """
    if created:
        UserExpenseAccount.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_expense_account(sender, instance, **kwargs):
    """
    Signal handler that saves the UserExpenseAccount when a User is saved.
    Ensures expense account data is synced with user changes.
    """
    if hasattr(instance, 'expense_account'):
        instance.expense_account.save()
