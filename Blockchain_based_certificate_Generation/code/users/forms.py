from django import forms
from .models import Certificate

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['name', 'issued_to', 'email', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'From : Saikumar_velmula'}),
            'issued_to': forms.TextInput(attrs={'placeholder': 'Issuing To : Alex'}),
            'email': forms.EmailInput(attrs={'placeholder': 'enter valid email to recieve certificate'}),
            'description': forms.Textarea(attrs={'placeholder': 'Ex : Completed Refugee Support Training Program with excellence and dedication.'}),
        }
