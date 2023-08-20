from django.shortcuts import render,redirect
from .models import *
from datetime import datetime
import calendar
from django.core.paginator import Paginator
from .forms import CommentForm, ContactForm
from django.contrib import messages

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
    leaders_by_category = Leader.objects.values('category').distinct()
    leaders = {}
    
    for category in leaders_by_category:
        leaders[category['category']] = Leader.objects.filter(category=category['category'])

    context = {'leaders_by_category': leaders}
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
def livestream(request):
    context = {}
    return render(request, 'base/livestream.html', context)

# ==================================================================
# 9. Blogs
# ==================================================================
def blogs(request):
    blogs = Blog.objects.all()
    categories = Category.objects.all()
    context = {'blogs':blogs,'categories':categories}
    return render(request, 'base/blogs.html', context)

# ==================================================================
# 10. Blog
# ==================================================================
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
def ministries(request):
    ministries = Ministry.objects.all()
    context = {'ministries':ministries}
    return render(request, 'base/ministries.html', context)

def ministry(request, slug):
    ministry = Ministry.objects.get(slug=slug)
    context = {'ministry':ministry}
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

# ==================================================================
# 16. Events
# ==================================================================
def gallary(request):
    all_galleries = Gallery.objects.all()
    paginator = Paginator(all_galleries, 12)  # Show 4 galleries per page

    page = request.GET.get('page')
    gallaries = paginator.get_page(page)

    context = {
        'gallaries': gallaries,
        'total_galleries': all_galleries.count(),
    }
    return render(request, 'base/gallary.html', context)

# ==================================================================
# 17. sermon
# ==================================================================
def sermon(request):
    all_galleries = Sermon.objects.all()
    paginator = Paginator(all_galleries, 12)  # Show 4 galleries per page

    page = request.GET.get('page')
    gallaries = paginator.get_page(page)

    context = {
        'gallaries': gallaries,
        'total_galleries': all_galleries.count(),
    }
    return render(request, 'base/sermon.html', context)

# ==================================================================
# 18. song
# ==================================================================
def song(request):
    all_galleries = Song.objects.all()
    paginator = Paginator(all_galleries, 12)  # Show 4 galleries per page

    page = request.GET.get('page')
    gallaries = paginator.get_page(page)

    context = {
        'gallaries': gallaries,
        'total_galleries': all_galleries.count(),
    }
    return render(request, 'base/song.html', context)

# ==================================================================
# 19. livestream
# ==================================================================
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