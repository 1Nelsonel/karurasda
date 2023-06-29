from django.shortcuts import render


# ==================================================================
# 1. home
# ==================================================================
def home(request):
    context = {}
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
def pastor(request):
    context = {}
    return render(request, 'base/pastor.html', context)

# ==================================================================
# 5. Member
# ==================================================================
def member(request):
    context = {}
    return render(request, 'base/member.html', context)

# ==================================================================
# 6. Calender
# ==================================================================
def calender(request):
    context = {}
    return render(request, 'base/calender.html', context)

# ==================================================================
# 7. Newsletter
# ==================================================================
def newsletter(request):
    context = {}
    return render(request, 'base/newsletter.html', context)

# ==================================================================
# 8. Tender
# ==================================================================
def tender(request):
    context = {}
    return render(request, 'base/tender.html', context)

# ==================================================================
# 9. Vaccancy
# ==================================================================
def vaccancy(request):
    context = {}
    return render(request, 'base/vaccancy.html', context)

# ==================================================================
# 10. Contact
# ==================================================================
def contact(request):
    context = {}
    return render(request, 'base/contact.html', context)

# ==================================================================
# 11. Giving
# ==================================================================
def giving(request):
    context = {}
    return render(request, 'base/giving.html', context)

# ==================================================================
# 12. Announcement
# ==================================================================
def announcement(request):
    context = {}
    return render(request, 'base/announcement.html', context)

# ==================================================================
# 13. Livestream
# ==================================================================
def livestream(request):
    context = {}
    return render(request, 'base/livestream.html', context)

# ==================================================================
# 14. Blogs
# ==================================================================
def blogs(request):
    context = {}
    return render(request, 'base/blog.html', context)

# ==================================================================
# 14. Blog
# ==================================================================
def blog(request):
    context = {}
    return render(request, 'base/blog.html', context)