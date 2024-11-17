from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

USER_TYPE_CHOICES = [
    ('individual', 'Individual'),
    ('organization', 'Organization')
]

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)
    organization_name = forms.CharField(required=False)
    organization_address = forms.CharField(required=False)
    individual_full_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type', 'organization_name', 'organization_address', 'individual_full_name']

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")

        if user_type == "organization":
            if not cleaned_data.get("organization_name"):
                self.add_error('organization_name', 'This field is required for organizations.')
            if not cleaned_data.get("organization_address"):
                self.add_error('organization_address', 'This field is required for organizations.')
        elif user_type == "individual":
            if not cleaned_data.get("individual_full_name"):
                self.add_error('individual_full_name', 'This field is required for individuals.')
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            profile = Profile.objects.create(
                user=user,
                user_type=self.cleaned_data.get('user_type'),
                organization_name=self.cleaned_data.get('organization_name'),
                organization_address=self.cleaned_data.get('organization_address'),
                individual_full_name=self.cleaned_data.get('individual_full_name')
            )
        return user
