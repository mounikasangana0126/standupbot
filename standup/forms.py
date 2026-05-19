from django import forms
from .models import StandupEntry


class StandupForm(forms.ModelForm):
    class Meta:
        model = StandupEntry
        fields = ['did', 'doing', 'blockers']
        widgets = {
            'did': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'e.g. Finished the auth module, fixed the login bug...',
                'maxlength': 500,
                'x-model': 'did',
            }),
            'doing': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'e.g. Working on the dashboard, reviewing PRs...',
                'maxlength': 500,
                'x-model': 'doing',
            }),
            'blockers': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'e.g. Waiting on API keys from DevOps...',
                'maxlength': 300,
                'x-model': 'blockers',
            }),
        }
        labels = {
            'did': 'What did you do yesterday?',
            'doing': 'What are you doing today?',
            'blockers': 'Any blockers?',
        }


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('password2'):
            raise forms.ValidationError('Passwords do not match.')
        return cleaned
