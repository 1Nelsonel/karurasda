from django.shortcuts import render, redirect
from django.contrib import messages #import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import *
from base.models import *
from django.db.models import Count
from django.views.decorators.cache import cache_page

# ===========================================================
# authentication
# ===========================================================
class CustomLoginView(LoginView):
    template_name = 'adminpanel/login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')  # Redirect to the dashboard URL


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

# ==================================================================
# 1. dashboard
# ==================================================================
# @login_required(login_url='login')
# @cache_page(60*5)  # Cache the view for 5 minutes
def dashboard(request):
    event_count = Event.objects.count()
    ministries = Ministry.objects.all()
    events = Event.objects.all()
    blogs = Blog.objects.all()
    
    context = {
        'ministries': ministries,
        'blogs': blogs,
        'events': events,
        'event_count': event_count
    }
    return render(request, 'adminpanel/dashboard.html', context)

# ==================================================================
# 2. events
# ==================================================================
def event_list(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'adminpanel/event_list.html', context)

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event added successfully!')
            return redirect('event_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')

    else:
        form = EventForm()
    context = {'form': form}
    return render(request, 'adminpanel/add.html', context)

def update_event(request, slug):
    event = Event.objects.get(slug=slug)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    context = {'form': form, 'event': event}
    return render(request, 'adminpanel/update.html', context)

def delete_event(request, slug):
    event = Event.objects.get(slug=slug)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('event_list')
    context = {'obj': event}
    return render(request, 'adminpanel/delete.html', context)
