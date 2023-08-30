from django.shortcuts import render,redirect
from .models import *
from datetime import datetime
import calendar
from django.core.paginator import Paginator
from .forms import CommentForm, ContactForm
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.cache import cache_page

# ==================================================================
# 1. home
# ==================================================================
@cache_page(60*5)  # Cache the view for 5 minutes
def home(request):
    carousels = Carousel.objects.all()
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
        'carousels': carousels
    }
    return render(request, 'base/home.html', context)

# ==================================================================
# 2. About
# ==================================================================
@cache_page(60*5)  # Cache the view for 5 minutes
def about(request):
    context = {}
    return render(request, 'base/about.html', context)

# ==================================================================
# 3. Faq
# ==================================================================
@cache_page(60*5)  # Cache the view for 5 minutes
def faq(request):
    context = {}
    return render(request, 'base/faq.html', context)

# ==================================================================
# 4. Pastor
# ==================================================================
@cache_page(60*5)  # Cache the view for 5 minutes
def leaders(request):
    leaders_by_category = Leader.objects.values('category').distinct()
    leaders = {}
    
    for category in leaders_by_category:
        leaders[category['category']] = Leader.objects.filter(category=category['category'])

    context = {'leaders_by_category': leaders}
    return render(request, 'base/leaders.html', context)

# ==================================================================
# 5. Member
# ==================================================================
@cache_page(60*5)  # Cache the view for 5 minutes
def member(request):
    context = {}
    return render(request, 'base/member.html', context)

# ==================================================================
# 6. Vaccancy
# ==================================================================
@cache_page(60*5)  # Cache the view for 5 minutes
def vaccancy(request):
    context = {}
    return render(request, 'base/vaccancy.html', context)

# ==================================================================
# 7. Contact
# ==================================================================
@cache_page(60*5)  # Cache the view for 5 minutes
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the comment
            messages.success(request, 'Comment send successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Error: Please check the form for errors.')
    else:
        form = ContactForm()
    context = {'form':form}
    return render(request, 'base/contact.html', context)

# ==================================================================
# 8. Livestream
# ==================================================================
@cache_page(60*5)  # Cache the view for 5 minutes
def livestream(request):
    context = {}
    return render(request, 'base/livestream.html', context)

# ==================================================================
# 9. Blogs
# ==================================================================
@cache_page(60*5)  # Cache the view for 5 minutes
def blogs(request):
    blogs = Blog.objects.all()
    categories = Category.objects.all()
    context = {'blogs':blogs,'categories':categories}
    return render(request, 'base/blogs.html', context)

# ==================================================================
# 10. Blog
# ==================================================================
@cache_page(60*5)  # Cache the view for 5 minutes
def blog(request, slug):
    blog = Blog.objects.get(slug=slug)
    categories = Category.objects.all()
    blogs = Blog.objects.all()
    comments = Comment.objects.filter(blog=blog)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # Create a comment object but don't save it yet
            comment.blog = blog  # Set the blog post for the comment
            comment.save()  # Save the comment
            messages.success(request, 'Comment added successfully!')
            return redirect('blog', slug=blog.slug)
        else:
            messages.error(request, 'Error: Please check the form for errors.')
    else:
        form = CommentForm()

    context = {'blog':blog,'blogs':blogs,'categories':categories,'form':form,'comments':comments}
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
@cache_page(60*5)  # Cache the view for 5 minutes
def ministries(request):
    ministries = Ministry.objects.all()
    context = {'ministries':ministries}
    return render(request, 'base/ministries.html', context)

@cache_page(60*5)  # Cache the view for 5 minutes
def ministry(request, slug):
    ministry = Ministry.objects.get(slug=slug)
    context = {'ministry':ministry}
    return render(request, 'base/ministry.html', context)

# ==================================================================
# 15. Events
# ==================================================================
@cache_page(60*5)  # Cache the view for 5 minutes
def events(request):
    events = Event.objects.all()
    context = { 'events': events,}
    return render(request, 'base/events.html', context)

@cache_page(60*5)  # Cache the view for 5 minutes
def event(request, slug):
    event = Event.objects.get(slug=slug)
    context = {'event':event}
    return render(request, 'base/event.html', context)

# ==================================================================
# 16. Events
# ==================================================================
@cache_page(60*5)  # Cache the view for 5 minutes
def gallary(request):
    all_galleries = Gallery.objects.all()
    activities =  Event.objects.all()
    ministries =  Ministry.objects.all()

    # Filter by ministry
    ministry_id = request.GET.get('ministry')
    if ministry_id:
        all_galleries = all_galleries.filter(department_id=ministry_id)

    # Filter by activity
    activity_id = request.GET.get('activity')
    if activity_id:
        all_galleries = all_galleries.filter(activity_id=activity_id)

    # Filter by date
    date = request.GET.get('date')
    if date:
        all_galleries = all_galleries.filter(date=date)

    paginator = Paginator(all_galleries, 12)  # Show 12 galleries per page

    page = request.GET.get('page')
    gallaries = paginator.get_page(page)

    context = {
        'gallaries': gallaries,
        'total_galleries': all_galleries.count(),
        'activities': activities,
        'ministries': ministries
    }
    return render(request, 'base/gallary.html', context)

# ==================================================================
# 17. sermon
# ==================================================================
@cache_page(60*5)  # Cache the view for 5 minutes
def sermon(request):
    all_galleries = Sermon.objects.all()
    activities =  Event.objects.all()
    ministries =  Ministry.objects.all()

    # Filter by ministry
    ministry_id = request.GET.get('ministry')
    if ministry_id:
        all_galleries = all_galleries.filter(department_id=ministry_id)

    # Filter by activity
    activity_id = request.GET.get('activity')
    if activity_id:
        all_galleries = all_galleries.filter(activity_id=activity_id)

    # Filter by date
    date = request.GET.get('date')
    if date:
        all_galleries = all_galleries.filter(date=date)

    paginator = Paginator(all_galleries, 12)  # Show 4 galleries per page

    page = request.GET.get('page')
    gallaries = paginator.get_page(page)

    context = {
        'gallaries': gallaries,
        'total_galleries': all_galleries.count(),
        'activities': activities,
        'ministries': ministries
    }
    return render(request, 'base/sermon.html', context)

# ==================================================================
# 18. song
# ==================================================================
@cache_page(60*5)  # Cache the view for 5 minutes
def song(request):
    all_galleries = Song.objects.all()
    activities =  Event.objects.all()
    ministries =  Ministry.objects.all()

    # Filter by ministry
    ministry_id = request.GET.get('ministry')
    if ministry_id:
        all_galleries = all_galleries.filter(department_id=ministry_id)

    # Filter by activity
    activity_id = request.GET.get('activity')
    if activity_id:
        all_galleries = all_galleries.filter(activity_id=activity_id)

    # Filter by date
    date = request.GET.get('date')
    if date:
        all_galleries = all_galleries.filter(date=date)

    paginator = Paginator(all_galleries, 12)  # Show 4 galleries per page

    page = request.GET.get('page')
    gallaries = paginator.get_page(page)

    context = {
        'gallaries': gallaries,
        'total_galleries': all_galleries.count(),
        'activities': activities,
        'ministries': ministries
    }
    return render(request, 'base/song.html', context)

# ==================================================================
# 19. livestream
# ==================================================================
@cache_page(60*5)  # Cache the view for 5 minutes
def livestream(request):
    all_galleries = LiveStream.objects.all()
    paginator = Paginator(all_galleries, 12)  # Show 4 galleries per page

    page = request.GET.get('page')
    gallaries = paginator.get_page(page)

    context = {
        'gallaries': gallaries,
        'total_galleries': all_galleries.count(),
    }
    return render(request, 'base/livestream.html', context)

# ==================================================================
# 19. livestream
# ==================================================================
def youtube(request):
    context = {}
    return render(request, 'base/youtube.html', context)