# forms.py
from django import forms
from .models import UserUpload

class UserUploadForm(forms.ModelForm):
    class Meta:
        model = UserUpload
        fields = ['img', 'link', 'days', 'currency']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currency'].widget = forms.Select(choices=UserUpload.CURRENCY_CHOICES)
