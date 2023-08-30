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
            title = cleaned_data.get('title')
            eventDate = cleaned_data.get('startTime')
            eventDate = cleaned_data.get('startTime')
            endTime = cleaned_data.get('endTime')
            description = cleaned_data.get('description')
            venue = cleaned_data.get('venue')
            topic = cleaned_data.get('topic')

            if not title:
                self.add_error('title', 'Please enter an event title.')
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

class BlogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_adding = 'instance' not in kwargs  # Check if the form is used for adding or updating

    class Meta:
        model = Blog
        fields = ['title', 'image', 'description','host','category']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blog Name'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'blog post image'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write Message Here...'}),
            'host': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write host name Here...'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Write category name Here...'}),

        }

    def clean(self):
        cleaned_data = super().clean()

        # If the form is used for adding, make all fields required
        if self.is_adding:
            title = cleaned_data.get('title')
            image = cleaned_data.get('image')
            description = cleaned_data.get('description')
            host = cleaned_data.get('host')
            category = cleaned_data.get('category')

            if not title:
                self.add_error('title', 'Please enter a blog name.')
            if not image:
                self.add_error('image', 'Please upload an image.')
            if not description:
                self.add_error('description', 'Please write a message.')
            if not host:
                self.add_error('host', 'Please enter host name.')
            if not category:
                self.add_error('category', 'Please enter category name.')

class FamilyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_adding = 'instance' not in kwargs  # Check if the form is used for adding or updating

    class Meta:
        model = Family
        fields = ['name',]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter family Name'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # If the form is used for adding, make the 'name' field required
        if self.is_adding:
            name = cleaned_data.get('name')
            if not name:
                self.add_error('name', 'Please enter a family name.')


class MemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_adding = 'instance' not in kwargs  # Check if the form is used for adding or updating

    class Meta:
        model = Member
        fields = ['name', 'family', 'memberNumber']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Member Name'}),
            'family': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select family'}),
            'memberNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter member number'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # If the form is used for adding, make all fields required
        if self.is_adding:
            name = cleaned_data.get('name')
            family = cleaned_data.get('family')
            memberNumber = cleaned_data.get('memberNumber')

            if not name:
                self.add_error('name', 'Please enter a member name.')
            if not family:
                self.add_error('family', 'Please select a family.')
            if not memberNumber:
                self.add_error('memberNumber', 'Please enter an member number.')


class DepartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_adding = 'instance' not in kwargs  # Check if the form is used for adding or updating

    class Meta:
        model = Ministry
        fields = ['name', 'image', 'content']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter minissrty Name'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'department image'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write Message Here...'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # If the form is used for adding, make all fields required
        if self.is_adding:
            name = cleaned_data.get('name')
            image = cleaned_data.get('image')
            content = cleaned_data.get('content')

            if not name:
                self.add_error('name', 'Please enter a department name.')
            if not image:
                self.add_error('image', 'Please upload an image.')
            if not content:
                self.add_error('content', 'Please write a message.')

class PatronForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_adding = 'instance' not in kwargs  # Check if the form is used for adding or updating

    class Meta:
        model = Leader
        fields = ['name', 'image', 'position', 'category']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Patron Name'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Patron image'}),
            'category': forms.Select(attrs={'class': 'form-control'}),  # Use forms.Select widget for ChoiceField
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter position Name'}),
        }


    def clean(self):
        cleaned_data = super().clean()

        # If the form is used for adding, make all fields required
        if self.is_adding:
            name = cleaned_data.get('name')
            image = cleaned_data.get('image')
            category = cleaned_data.get('category')
            position = cleaned_data.get('position')

            if not name:
                self.add_error('name', 'Please enter a Patron name.')
            if not image:
                self.add_error('image', 'Please upload an image.')
            if not category:
                self.add_error('category', 'Please enter category name.')
            if not position:
                self.add_error('position', 'Please enter position name.')

class VideoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_adding = 'instance' not in kwargs  # Check if the form is used for adding or updating

    class Meta:
        model = Song
        fields = ['videolink','department','activity','date' ]

        widgets = {
            'videolink': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter video link'}),
            'department': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select department Name'}),
            'activity': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select activity Name'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select date','type':'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # If the form is used for adding, make the 'name' field required
        if self.is_adding:
            name = cleaned_data.get('name')
            department = cleaned_data.get('department')
            activity = cleaned_data.get('activity')
            date = cleaned_data.get('date')
            if not name:
                self.add_error('name', 'Please enter a video name.')
            if not department:
                self.add_error('department', 'Please enter a department name.')
            if not activity:
                self.add_error('activity', 'Please enter a activity name.')
            if not date:
                self.add_error('date', 'Please enter a activity name.')
        # Handle video field separately as optional
        videolink = cleaned_data.get('videolink')
        if videolink:
            if not self.is_valid_url(videolink):
                self.add_error('video', 'Please enter a valid video URL.')

    def is_valid_url(self, url):
        try:
            url_validator = URLValidator()
            url_validator(url)
            backend = detect_backend(url)
            if not backend:
                return False
        except ValidationError:
            return False

        return True
    
class SermonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_adding = 'instance' not in kwargs  # Check if the form is used for adding or updating

    class Meta:
        model = Sermon
        fields = ['videolink','department','activity','date' ]

        widgets = {
            'videolink': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter video link'}),
            'department': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select department Name'}),
            'activity': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select activity Name'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select date','type':'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # If the form is used for adding, make the 'name' field required
        if self.is_adding:
            name = cleaned_data.get('name')
            department = cleaned_data.get('department')
            activity = cleaned_data.get('activity')
            date = cleaned_data.get('date')
            if not name:
                self.add_error('name', 'Please enter a video name.')
            if not department:
                self.add_error('department', 'Please enter a department name.')
            if not activity:
                self.add_error('activity', 'Please enter a activity name.')
            if not date:
                self.add_error('date', 'Please enter a activity name.')
        # Handle video field separately as optional
        videolink = cleaned_data.get('videolink')
        if videolink:
            if not self.is_valid_url(videolink):
                self.add_error('video', 'Please enter a valid video URL.')

    def is_valid_url(self, url):
        try:
            url_validator = URLValidator()
            url_validator(url)
            backend = detect_backend(url)
            if not backend:
                return False
        except ValidationError:
            return False

        return True


class GallaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_adding = 'instance' not in kwargs  # Check if the form is used for adding or updating

    class Meta:
        model = Gallery
        fields = ['image','department','activity','date']

        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'image'}),
            'department': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select department Name', 'type': 'select'}),
            'activity': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select activity Name'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select date', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # If the form is used for adding, make the 'name' field required
        if self.is_adding:
            department = cleaned_data.get('department')
            activity = cleaned_data.get('activity')
            date = cleaned_data.get('date')

            if not department:
                self.add_error('department', 'Please enter a department name.')
            if not activity:
                self.add_error('activity', 'Please enter a activity name.')
            if not date:
                self.add_error('date', 'Please enter a activity name.')

class LiveVideoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_adding = 'instance' not in kwargs  # Check if the form is used for adding or updating

    class Meta:
        model = LiveStream
        fields = ['videolink',]

        widgets = {
            'videolink': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'enter livestream link here'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # If the form is used for adding, make the 'name' field required
        if self.is_adding:
            videolink = cleaned_data.get('videolink')

            if not self.is_valid_url(videolink):
                self.add_error('video', 'Please enter a valid video URL.')


class CarouselForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_adding = 'instance' not in kwargs  # Check if the form is used for adding or updating
        
    class Meta:
        model = Carousel
        fields = ['title', 'subtitle', 'image']

        widgets = {            
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Carousel Name'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter carousel subtitle'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'image'}),
            
        }
    def clean(self):
        cleaned_data = super().clean()

        # If the form is used for adding, make the 'name' field required
        if self.is_adding:
            title = cleaned_data.get('title')
            subtitle = cleaned_data.get('subtitle')
            image = cleaned_data.get('image')

            if not title:
                self.add_error('title', 'Please enter a carousel name.')
            if not subtitle:
                self.add_error('subtitle', 'Please enter a carousel subtitle.')
            if not image:
                self.add_error('image', 'Please upload an image.')