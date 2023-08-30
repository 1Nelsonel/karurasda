from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages #import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import *
from base.models import *
from django.db.models import Count
from django.views.decorators.cache import cache_page
from django.http import Http404

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
@login_required(login_url='login')
@cache_page(60*5)  # Cache the view for 5 minutes
def dashboard(request):
    blogs = Blog.objects.all()
    members = Member.objects.all()
    events = Event.objects.all()
    ministries = Ministry.objects.all()
    leaders = Leader.objects.all()
    event_count = events.count() 
    member_count = members.count()
    ministry_count = ministries.count()
    blog_count = blogs.count()
    leader_count = leaders.count()
    ministry_count = ministries.count()
    article_count = blogs.count()
    
    context = {
        'ministries': ministries,
        'blogs': blogs,
        'events': events,
        'members': members,
        'event_count': event_count,
        'member_count': member_count,
        'ministry_count': ministry_count,
        'blog_count': blog_count,
        'leader_count': leader_count,
        'article_count': article_count,
    }
    return render(request, 'adminpanel/dashboard.html', context)

# ==================================================================
# 2. members
# ==================================================================
@login_required(login_url='login')
@cache_page(60*5)  # Cache the view for 5 minutes
def members(request):
    members = Member.objects.all()
    context = {'members':members}
    return render(request, 'adminpanel/members.html', context)

@login_required(login_url='login')
def addMember(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Family added successfully!')
            return redirect('members')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
        
    else:
        form = MemberForm()
    context = {'form':form}
    return render(request, 'adminpanel/addMembers.html', context)

@login_required(login_url='login')
def updateMember(request, slug):
    member = Member.objects.get(slug=slug)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Family updated successfully!')
            return redirect('members')
    else:
        form = MemberForm(instance=member)
    context = {'form': form,'member':member}
    return render(request, 'adminpanel/update.html', context)

@login_required(login_url='login')
def deleteMember(request, slug):
    member = Member.objects.get(slug=slug)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Family deleted successfully!')
        return redirect('members')
    context = {'obj': member}
    return render(request, 'adminpanel/delete.html', context)

# ==================================================================
# 3. family
# ==================================================================
@login_required(login_url='login')
@cache_page(60*5)  # Cache the view for 5 minutes
def family(request):
    families = Family.objects.annotate(member_count=Count('member'))
    
    context = {'families':families}
    return render(request, 'adminpanel/family.html', context)

@login_required(login_url='login')
def addFamily(request):
    if request.method == 'POST':
        form = FamilyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Family added successfully!')
            return redirect('family') 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')       
    else:
        form = FamilyForm()

    context = {'form':form}
    return render(request, 'adminpanel/add.html', context)

@login_required(login_url='login')
def updateFamily(request, slug):
    family = Family.objects.get(slug=slug)
    if request.method == 'POST':
        form = FamilyForm(request.POST, instance=family)
        if form.is_valid():
            form.save()
            messages.success(request, 'Family updated successfully!')
            return redirect('family')
    else:
        form = FamilyForm(instance=family)

    context = {'form': form, 'family': family}
    return render(request, 'adminpanel/update.html', context)

@login_required(login_url='login')
def deleteFamily(request, slug):
    family = Family.objects.get(slug=slug)
    if request.method == 'POST':
        family.delete()
        messages.success(request, 'Family deleted successfully!')
        return redirect('family')

    context = {'obj': family}
    return render(request, 'adminpanel/delete.html', context)

# ==================================================================
# 4. department
# ==================================================================
@login_required(login_url='login')
@cache_page(60*5)  # Cache the view for 5 minutes
def department_list(request):
    departments = Ministry.objects.all()
    context = {'departments': departments}
    return render(request, 'adminpanel/department_list.html', context)

@login_required(login_url='login')
def department_detail(request, slug):
    department = Ministry.objects.get(slug=slug)
    context = {'department': department}
    return render(request, 'adminpanel/department_detail.html', context)

@login_required(login_url='login')
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added successfully!')
            return redirect('department_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')

    else:
        form = DepartmentForm()
    context = {'form': form}
    return render(request, 'adminpanel/add.html', context)

@login_required(login_url='login')
def update_department(request, slug):
    department = Ministry.objects.get(slug=slug)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    context = {'form': form, 'department': department}
    return render(request, 'adminpanel/update.html', context)

@login_required(login_url='login')
@cache_page(60*5)  # Cache the view for 5 minutes
def delete_department(request, slug):
    department = Ministry.objects.get(slug=slug)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully!')
        return redirect('department_list')
    context = {'obj': department}
    return render(request, 'adminpanel/delete.html', context)


# ==================================================================
# 6. events
# ==================================================================
@login_required(login_url='login')
@cache_page(60*5)  # Cache the view for 5 minutes
def event_list(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'adminpanel/event_list.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def delete_event(request, slug):
    event = Event.objects.get(slug=slug)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('event_list')
    context = {'obj': event}
    return render(request, 'adminpanel/delete.html', context)

# ==================================================================
# 7. blogs
# ==================================================================
@login_required(login_url='login')
@cache_page(60*5)  # Cache the view for 5 minutes
def blog_list(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render(request, 'adminpanel/blogs.html', context)

@login_required(login_url='login')
def blog_add(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')

    else:
        form = BlogForm()    
    context = {'form': form}
    return render(request, 'adminpanel/add.html', context)

@login_required(login_url='login')
def blog_update(request, slug):
    # blog = Blog.objects.get(slug=slug)
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        raise Http404("Blog does not exist")
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogForm(instance=blog)
        context = {'form': form, 'blog': blog}
    return render(request, 'adminpanel/update.html', context)

@login_required(login_url='login')
def blog_delete(request, slug):
    blog = Blog.objects.get(slug=slug)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    
    context = {'obj': blog}
    return render(request, 'adminpanel/delete.html', context)

# ==================================================================
# 8. patron
# ==================================================================
@login_required(login_url='login')
@cache_page(60*5)  # Cache the view for 5 minutes
def patron_list(request):
    patrons = Leader.objects.all()
    if request.method == 'POST':
        form = PatronForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('patron_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')

    else:
        form = PatronForm()
    context = {'patrons': patrons,'form': form}
    return render(request, 'adminpanel/patrons.html', context)

@login_required(login_url='login')
def patron_update(request, pk):
    patron = Leader.objects.get(id=pk)
    if request.method == 'POST':
        form = PatronForm(request.POST, request.FILES, instance=patron)
        if form.is_valid():
            form.save()
            return redirect('patron_list')
    else:
        form = PatronForm(instance=patron)
    context = {'form': form, 'patron': patron}
    return render(request, 'adminpanel/update.html', context)

@login_required(login_url='login')
def patron_delete(request, pk):
    patron = Leader.objects.get(id=pk)
    if request.method == 'POST':
        patron.delete()
        return redirect('patron_list')
    context = {'obj': patron}
    return render(request, 'adminpanel/delete.html', context)

# ==================================================================
# 9. video
# ==================================================================
@login_required(login_url='login')
@cache_page(60*5)  # Cache the view for 5 minutes
def video_list(request):
    videos = Song.objects.all()
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('video_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')

    else:
        form = VideoForm()
    context = {'videos': videos,'form': form}
    return render(request, 'adminpanel/video_list.html', context)


@login_required(login_url='login')
def video_update(request, pk):
    video = Song.objects.get(id=pk)
    if request.method == 'POST':
        form = VideoForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            return redirect('video_list')
    else:
        form = VideoForm(instance=video)
    context = {'form': form}
    return render(request, 'adminpanel/update.html', context)


@login_required(login_url='login')
def video_delete(request, pk):
    video = Song.objects.get(id=pk)
    if request.method == 'POST':
        video.delete()
        return redirect('video_list')
    
    context = {'obj': video}
    return render(request, 'adminpanel/delete.html', context)

# ==================================================================
# 10. gallary
# ==================================================================
@login_required(login_url='login')
@cache_page(60*5)  # Cache the view for 5 minutes
def gallary_list(request):
    gallaries = Gallery.objects.all()
    if request.method == 'POST':
        form = GallaryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallary_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')

    else:
        form = GallaryForm()
    context = {'gallaries': gallaries,'form': form}
    return render(request, 'adminpanel/gallary_list.html', context)


@login_required(login_url='login')
def gallary_update(request, pk):
    gallary = Gallery.objects.get(pk=pk)
    if request.method == 'POST':
        form = GallaryForm(request.POST, request.FILES, instance=gallary)
        if form.is_valid():
            form.save()
            return redirect('gallary_list')
    else:
        form = GallaryForm(instance=gallary)
    context = {'form': form}
    return render(request, 'adminpanel/update.html', context)

@login_required(login_url='login')
def gallary_delete(request, pk):
    gallary = Gallery.objects.get(pk=pk)
    if request.method == 'POST':
        gallary.delete()
        return redirect('gallary_list')
    context = {'obj': gallary}
    return render(request, 'adminpanel/delete.html', context)


# ======================================================================
# contact
# ======================================================================
@login_required(login_url='login')
@cache_page(60*5)  # Cache the view for 5 minutes
def contact(request):
    contacts = Contact.objects.all()
    context = {'contacts': contacts}
    return render(request, 'adminpanel/messages.html', context)

# =======================================================================
# livestream
# =======================================================================
@login_required(login_url='login')
@cache_page(60*5)  # Cache the view for 5 minutes
def live_video_list(request):
    videos = LiveStream.objects.all()
    if request.method == 'POST':
        form = LiveVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('live_video_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = LiveVideoForm()
    context = {'form': form, 'videos': videos}
    return render(request, 'adminpanel/livestream.html', context)

@login_required(login_url='login')
def live_video_update(request, pk):
    video = LiveStream.objects.get(id=pk)
    if request.method == 'POST':
        form = LiveVideoForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            return redirect('live_video_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = LiveVideoForm(instance=video)
    context = {'form': form}
    return render(request, 'adminpanel/update.html', context)

@login_required(login_url='login')
def live_video_delete(request, pk):
    video = LiveStream.objects.get(id=pk)
    if request.method == 'POST':
        video.delete()
        return redirect('live_video_list')
    context = {'obj': video}
    return render(request, 'adminpanel/delete.html', context)

# =======================================================================
# sermon
# =======================================================================
@login_required(login_url='login')
@cache_page(60*5)  # Cache the view for 5 minutes
def sermon(request):
    sermons = Sermon.objects.all()
    if request.method == 'POST':
        form = SermonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sermon_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = SermonForm()
    context = {'form': form, 'sermons': sermons}
    return render(request, 'adminpanel/sermon.html', context)


@login_required(login_url='login')
def sermon_update(request, pk):
    sermon = Sermon.objects.get(id=pk)
    if request.method == 'POST':
        form = SermonForm(request.POST, instance=sermon)
        if form.is_valid():
            form.save()
            return redirect('sermon_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = SermonForm(instance=sermon)
    context = {'form': form}
    return render(request, 'adminpanel/update.html', context)


@login_required(login_url='login')
def sermon_delete(request, pk):
    sermon = Sermon.objects.get(id=pk)
    if request.method == 'POST':
        sermon.delete()
        return redirect('sermon_list')
    context = {'obj': sermon}
    return render(request, 'adminpanel/delete.html', context)


# =======================================================================
# sermon
# =======================================================================
@login_required(login_url='login')
@cache_page(60*5)  # Cache the view for 5 minutes
def create_carousel(request):
    carousels = Carousel.objects.all()
    if request.method == 'POST':
        form = CarouselForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('carousel')  # Replace 'carousel_list' with your actual URL name for listing carousels
    else:
        form = CarouselForm()

    context = {'form': form, 'carousels':carousels}
    return render(request, 'adminpanel/carousel.html', context)


@login_required(login_url='login')
def update_carousel(request, pk):
    carousel = get_object_or_404(Carousel, id=pk)
    if request.method == 'POST':
        form = CarouselForm(request.POST, request.FILES, instance=carousel)
        if form.is_valid():
            form.save()
            return redirect('carousel')  # Replace 'carousel_list' with your actual URL name for listing carousels
    else:
        form = CarouselForm(instance=carousel)

    context = {'form': form, 'carousel': carousel}
    return render(request, 'adminpanel/update.html', context)


@login_required(login_url='login')
def delete_carousel(request, pk):
    carousel = get_object_or_404(Carousel, id=pk)
    if request.method == 'POST':
        carousel.delete()
        return redirect('carousel')  # Replace 'carousel_list' with your actual URL name for listing carousels
    context = {'obj': carousel}
    return render(request, 'adminpanel/delete.html', context)

