from django import forms
from .models import Contact, Comment


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'mobile', 'body']

        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email', 'required': True}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subject', 'required': True}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Mobile Number', 'required': True}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write Message Here...', 'required': True}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'email', 'body']

        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email', 'required': True}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write Your Comment Here...', 'required': True}),
        }