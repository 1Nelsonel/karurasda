from django.shortcuts import render
from .models import *
from datetime import datetime
import calendar

# ==================================================================
# 1. home
# ==================================================================
def home(request):
    today = datetime.today()
    current_year = today.year
    current_month = today.month

    if 'year' in request.GET and 'month' in request.GET:
        year = int(request.GET['year'])
        month = int(request.GET['month'])
        events = Event.objects.filter(eventDate__year=year, eventDate__month=month)
    else:
        year = current_year
        month = current_month
        events = Event.objects.filter(eventDate__year=current_year, eventDate__month=current_month)

    context = {
        'events': events,
        'current_year': year,
        'current_month': month,
        'current_month_name': calendar.month_name[month],  # Get month name
    }
    return render(request, 'base/home.html', context)

# ==================================================================
# 2. About
# ==================================================================
def about(request):
    context = {}
    return render(request, 'base/about.html', context)

# ==================================================================
# 3. Faq
# ==================================================================
def faq(request):
    context = {}
    return render(request, 'base/faq.html', context)

# ==================================================================
# 4. Pastor
# ==================================================================
def leaders(request):
    context = {}
    return render(request, 'base/leaders.html', context)

# ==================================================================
# 5. Member
# ==================================================================
def member(request):
    context = {}
    return render(request, 'base/member.html', context)

# ==================================================================
# 6. Vaccancy
# ==================================================================
def vaccancy(request):
    context = {}
    return render(request, 'base/vaccancy.html', context)

# ==================================================================
# 7. Contact
# ==================================================================
def contact(request):
    context = {}
    return render(request, 'base/contact.html', context)

# ==================================================================
# 8. Livestream
# ==================================================================
def livestream(request):
    context = {}
    return render(request, 'base/livestream.html', context)

# ==================================================================
# 9. Blogs
# ==================================================================
def blogs(request):
    context = {}
    return render(request, 'base/blogs.html', context)

# ==================================================================
# 10. Blog
# ==================================================================
def blog(request):
    context = {}
    return render(request, 'base/blog.html', context)

# ==================================================================
# 11. egwwrittings
# ==================================================================
def egwwrittings(request):
    context = {}
    return render(request, 'base/egwwrittings.html', context)

# ==================================================================
# 12. Lesson
# ==================================================================
def lesson(request):
    context = {}
    return render(request, 'base/lesson.html', context)

# ==================================================================
# 13. Media
# ==================================================================
def media(request):
    context = {}
    return render(request, 'base/media.html', context)

# ==================================================================
# 14. Ministries
# ==================================================================
def ministries(request):
    context = {}
    return render(request, 'base/ministries.html', context)

def ministry(request):
    context = {}
    return render(request, 'base/ministry.html', context)

# ==================================================================
# 15. Events
# ==================================================================
def events(request):
    events = Event.objects.all()
    context = { 'events': events,}
    return render(request, 'base/events.html', context)

def event(request, slug):
    event = Event.objects.get(slug=slug)
    context = {'event':event}
    return render(request, 'base/event.html', context)
