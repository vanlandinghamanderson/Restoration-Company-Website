from django import forms
from django.forms import ModelForm
from .models import Customer

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'email', 'phone_number', 'requested_service', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please Enter Your Name...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Please Enter Your Email...'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please Enter Your Phone Number... (e.g. (555) 555-5555)'}),
            'requested_service': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Please Choose a Service...'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Please describe your situation...', 
                'rows': 5
            }),
        }