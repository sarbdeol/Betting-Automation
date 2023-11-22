from django import forms
from .models import UserAccount, ExcelFile


class UserAccountForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ('username', 'email', 'password', 'website')
        website = forms.ChoiceField(
            widget=forms.RadioSelect,  # Use RadioSelect widget for radio buttons
            choices=UserAccount.WEBSITE_CHOICES,  # Replace 'WEBSITE_CHOICES' with your choices
        )


class ExcelFileForm(forms.ModelForm):
    class Meta:
        model = ExcelFile
        fields = ('file',)
