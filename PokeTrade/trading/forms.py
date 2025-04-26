import random
import re
from django import forms
from django.core.exceptions import ValidationError
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class CustomSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        base_username = self.cleaned_data['username']
        while User.objects.filter(username=base_username).exists():
            suffix = ''.join(random.choices(string.digits, k=4))
            base_username = f"{self.cleaned_data['username']}_{suffix}"
        return base_username


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'favorite_pokemon']