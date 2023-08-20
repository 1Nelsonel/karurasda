from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('leaders/', views.leaders, name='leaders'),
    path('member/', views.member, name='member'),
    path('contact/', views.contact, name='contact'),
    path('livestream/', views.livestream, name='livestream'),
    path('blogs/', views.blogs, name='blogs'),
    path('blog/', views.blog, name='blog'),    
    path('egwwrittings/', views.egwwrittings, name='egwwrittings'),
    path('lesson/', views.lesson, name='lesson'),
    path('media/', views.media, name='media'),
    path('ministries/', views.ministries, name='ministries'),
    path('ministry/<slug:slug>/', views.ministry, name='ministry'),
    path('events/', views.events, name='events'),
    path('event/<slug:slug>/', views.event, name='event'),
    path('gallary/', views.gallary, name='gallary'),
]