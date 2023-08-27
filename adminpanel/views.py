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
    blogs = Blog.objects.all()
    events = Event.objects.all()
    ministries = Ministry.objects.all()
    leaders = Leader.objects.all()
    event_count = events.count() 
    ministry_count = ministries.count()
    blog_count = blogs.count()
    leader_count = leaders.count()
    
    context = {
        'ministries': ministries,
        'blogs': blogs,
        'events': events,
        'event_count': event_count,
        'ministry_count': ministry_count,
        'blog_count': blog_count,
        'leader_count': leader_count
    }
    return render(request, 'adminpanel/dashboard.html', context)

# ==================================================================
# 2. members
# ==================================================================
@login_required(login_url='login')
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
def delete_department(request, slug):
    department = Ministry.objects.get(slug=slug)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully!')
        return redirect('department_list')
    context = {'obj': department}
    return render(request, 'adminpanel/delete.html', context)

# ==================================================================
# 5. announcements
# ==================================================================
# def announcement_list(request):
#     announcements = Announcement.objects.all()
#     context = {'announcements': announcements}
#     return render(request, 'dashboard/announcement_list.html', context)

# def add_announcement(request):
#     if request.method == 'POST':
#         form = AnnouncementForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Announcement added successfully!')
#             return redirect('announcement_list')
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f'Error in {field}: {error}')

#     else:
#         form = AnnouncementForm()
#     context = {'form': form}
#     return render(request, 'dashboard/add.html', context)

# def update_announcement(request, slug):
#     announcement = Announcement.objects.get(slug=slug)
#     if request.method == 'POST':
#         form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Announcement updated successfully!')
#             return redirect('announcement_list')
#     else:
#         form = AnnouncementForm(instance=announcement)
#     context = {'form': form, 'announcement': announcement}
#     return render(request, 'dashboard/update.html', context)

# def delete_announcement(request, slug):
#     announcement = Announcement.objects.get(slug=slug)
#     if request.method == 'POST':
#         announcement.delete()
#         messages.success(request, 'Announcement deleted successfully!')
#         return redirect('announcement_list')
#     context = {'obj': announcement}
#     return render(request, 'dashboard/delete.html', context)


# ==================================================================
# 6. events
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

# ==================================================================
# 7. blogs
# ==================================================================
def blog_list(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render(request, 'adminpanel/blogs.html', context)

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

def blog_update(request, slug):
    blog = Blog.objects.get(slug=slug)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogForm(instance=blog)
        context = {'form': form, 'blog': blog}
    return render(request, 'adminpanel/update.html', context)

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

def patron_update(request, slug):
    patron = Leader.objects.get(slug=slug)
    if request.method == 'POST':
        form = PatronForm(request.POST, request.FILES, instance=patron)
        if form.is_valid():
            form.save()
            return redirect('patron_list')
    else:
        form = PatronForm(instance=patron)
    context = {'form': form, 'patron': patron}
    return render(request, 'dashboard/update.html', context)

def patron_delete(request, slug):
    patron = Leader.objects.get(slug=slug)
    if request.method == 'POST':
        patron.delete()
        return redirect('patron_list')
    context = {'obj': patron}
    return render(request, 'adminpanel/delete.html', context)

# ==================================================================
# 9. video
# ==================================================================
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


def video_update(request, slug):
    video = Song.objects.get(slug=slug)
    if request.method == 'POST':
        form = VideoForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            return redirect('video_list')
    else:
        form = VideoForm(instance=video)
    context = {'form': form}
    return render(request, 'adminpanel/update.html', context)

def video_delete(request, slug):
    video = Song.objects.get(slug=slug)
    if request.method == 'POST':
        video.delete()
        return redirect('video_list')
    
    context = {'obj': video}
    return render(request, 'adminpanel/delete.html', context)

# ==================================================================
# 10. gallary
# ==================================================================
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

def gallary_delete(request, pk):
    gallary = Gallery.objects.get(pk=pk)
    if request.method == 'POST':
        gallary.delete()
        return redirect('gallary_list')
    context = {'obj': gallary}
    return render(request, 'adminpanel/delete.html', context)

# ==================================================================
# 11. mission
# ==================================================================


# ==================================================================
# 11. mission_list
# ==================================================================


# ======================================================================
# contact
# ======================================================================
def contact(request):
    contacts = Contact.objects.all()
    context = {'contacts': contacts}
    return render(request, 'adminpanel/messages.html', context)

# =======================================================================
# calender
# =======================================================================


# =======================================================================
# livestream
# =======================================================================
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

def live_video_update(request, slug):
    video = LiveStream.objects.get(slug=slug)
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

def live_video_delete(request, slug):
    video = LiveStream.objects.get(slug=slug)
    if request.method == 'POST':
        video.delete()
        return redirect('live_video_list')
    context = {'obj': video}
    return render(request, 'adminpanel/delete.html', context)

