from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('pastor/', views.pastor, name='pastor'),
    path('member/', views.member, name='member'),
    path('calender/', views.calender, name='calender'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('tender/', views.tender, name='tender'),
    path('vaccancy/', views.vaccancy, name='vaccancy'),
    path('contact/', views.contact, name='contact'),
    path('giving/', views.giving, name='giving'),
    path('announcement/', views.announcement, name='announcement'),
    path('livestream/', views.livestream, name='livestream'),
    path('blogs/', views.blogs, name='blogs'),
    path('blog/', views.blog, name='blog'),    
    path('egwwrittings/', views.egwwrittings, name='egwwrittings'),
    path('lesson/', views.lesson, name='lesson'),
    path('media/', views.media, name='media'),
]