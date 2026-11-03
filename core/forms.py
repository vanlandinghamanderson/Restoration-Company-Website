from django import forms
from django.forms import ModelForm
from .models import Customer, Service

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

    # It retreives the active services for the requested_service field,
    # phone_number, and requested_service required
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['requested_service'].queryset = Service.objects.filter(is_active=True)
        self.fields['phone_number'].required = True
        self.fields['requested_service'].required = True
