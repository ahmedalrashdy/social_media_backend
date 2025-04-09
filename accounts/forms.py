from django import forms
from .models import User

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'is_active', 'is_staff', 'is_superuser', 'verified')
        error_messages = {
            'email': {
                'required': 'يجب إدخال البريد الإلكتروني',
                'invalid': 'يرجى إدخال بريد إلكتروني صحيح',
                'unique': 'هذا البريد الإلكتروني مستخدم بالفعل'
            },
            'name': {
                'max_length': 'الاسم طويل جداً'
            }
            
        }
