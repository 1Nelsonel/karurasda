from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from embed_video.backends import detect_backend
from base.models import *


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_adding = 'instance' not in kwargs  # Check if the form is used for adding or updating

    class Meta:
        model = Event
        fields = ['title', 'image', 'eventDate', 'startTime', 'endTime', 'description',  'venue', 'topic']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Event Name'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Event image'}),
            'eventDate': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select Date', 'type': 'date'}),
            'startTime': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Select Start Time', 'type': 'time'}),
            'endTime': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Select end Time', 'type': 'time'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write Message Here...'}),
            'venue': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter venue Name'}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter topic Name'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # If the form is used for adding, make all fields required
        if self.is_adding:
            name = cleaned_data.get('name')
            eventDate = cleaned_data.get('startTime')
            eventDate = cleaned_data.get('startTime')
            endTime = cleaned_data.get('endTime')
            description = cleaned_data.get('description')
            venue = cleaned_data.get('venue')
            topic = cleaned_data.get('topic')

            if not name:
                self.add_error('name', 'Please enter an event name.')
            if not eventDate:
                self.add_error('date', 'Please select a date.')
            if not eventDate:
                self.add_error('content', 'Please enter eventDate.')
            if not endTime:
                self.add_error('content', 'Please enter endTime.')
            if not description:
                self.add_error('content', 'Please write description.')
            if not venue:
                self.add_error('content', 'Please enter venue.')
            if not topic:
                self.add_error('content', 'Please enter topic.')