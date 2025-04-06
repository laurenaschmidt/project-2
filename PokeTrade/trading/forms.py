import re
from django import forms
from django.core.exceptions import ValidationError

from .models import UserProfile

def username_validator(value):
    if not re.match(r'^[\w-]+$', value):
        raise ValidationError('Username must only contain letters, numbers, and underscores or dashes.')

# In your model or form, apply this validator:
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        validators=[username_validator],  # Apply the custom validator here
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'favorite_pokemon']