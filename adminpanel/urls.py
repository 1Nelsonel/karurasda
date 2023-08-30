from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView

urlpatterns = [
    # =================================================================================
    # Auth
    # =================================================================================
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # =================================================================================
    path('', views.dashboard, name='dashboard'),

    # =================================================================================
    # members
    # =================================================================================
    path('members/', views.members, name='members'),
    path('AddMember/', views.addMember, name='addMember'),
    path('update-member/<slug:slug>/', views.updateMember, name='updateMember'),
    path('delete-member/<slug:slug>/', views.deleteMember, name='deleteMember'),

    # =================================================================================
    # family
    # =================================================================================
    path('family/', views.family, name='family'),
    path('addFamily/', views.addFamily, name='addFamily'),
    path('family/update/<slug:slug>/', views.updateFamily, name='updateFamily'),
    path('family/delete/<slug:slug>/', views.deleteFamily, name='deleteFamily'),

    # =================================================================================
    # department
    # =================================================================================
    path('departments/', views.department_list, name='department_list'),
    path('department', views.add_department, name='add_department'),
    path('department/update/<slug:slug>/', views.update_department, name='update_department'),
    path('department/delete/<slug:slug>/', views.delete_department, name='delete_department'),

    # =================================================================================
    # announcements
    # =================================================================================
    # path('announcements/', views.announcement_list, name='announcement_list'),
    # path('announcement/', views.add_announcement, name='add_announcement'),
    # path('announcement/update/<slug:slug>/', views.update_announcement, name='update_announcement'),
    # path('announcement/delete/<slug:slug>/', views.delete_announcement, name='delete_announcement'),

    # =================================================================================
    # announcements
    # =================================================================================
    path('events/', views.event_list, name='event_list'),
    path('event/', views.add_event, name='add_event'),
    path('event/update/<slug:slug>/', views.update_event, name='update_event'),
    path('event/delete/<slug:slug>/', views.delete_event, name='delete_event'),

    # =================================================================================
    # blog
    # =================================================================================
    path('blogs/', views.blog_list, name='blog_list'),
    path('blog/add/', views.blog_add, name='blog_add'),
    path('blog/update/<slug:slug>/', views.blog_update, name='blog-update'),
    path('blog/delete/<slug:slug>/', views.blog_delete, name='blog-delete'),

    # =================================================================================
    # blog
    # =================================================================================
    path('patrons/', views.patron_list, name='patron_list'),
    path('patrons/update/<str:pk>/', views.patron_update, name='patron_update'),
    path('patrons/delete/<str:pk>/', views.patron_delete, name='patron_delete'),

    # =================================================================================
    # video
    # =================================================================================
    path('videos/', views.video_list, name='video_list'),
    path('videos/update/<str:pk>/', views.video_update, name='video_update'),
    path('videos/delete/<str:pk>/', views.video_delete, name='video_delete'),

     # =================================================================================
    # video
    # =================================================================================
    path('sermons/', views.sermon, name='sermon_list'),
    path('sermon/update/<str:pk>/', views.sermon_update, name='sermon_update'),
    path('sermon/delete/<str:pk>/', views.sermon_delete, name='sermon_delete'),

    # =================================================================================
    # gallary
    # =================================================================================    
    path('gallaries/', views.gallary_list, name='gallary_list'),
    path('gallaries/update/<str:pk>/', views.gallary_update, name='gallary_update'),
    path('gallaries/delete/<str:pk>/', views.gallary_delete, name='gallary_delete'),

    # =================================================================================
    # mission
    # ================================================================================= 
    # path('missions/', views.mission_list, name='mission_list'),
    # path('missions/update/<slug:slug>/', views.mission_update, name='mission_update'),
    # path('missions/delete/<slug:slug>/', views.mission_delete, name='mission_delete'),

    # =================================================================================
    # giving
    # ================================================================================= 
    # path('givings/', views.giving_list, name='giving_list'),
    # path('givings/update/<slug:slug>/', views.giving_update, name='giving_update'),
    # path('givings/delete/<slug:slug>/', views.giving_delete, name='giving_delete'),

    # =================================================================================
    # messages
    # ================================================================================= 
    path('messages/', views.contact, name='messages'),

    # =================================================================================
    # giving
    # ================================================================================= 
    # path('calender/admin/', views.calenderAdmin, name='calender-admin'),
    # path('calender/update/<slug:slug>/', views.calender_update, name='calender_update'),
    # path('calender/delete/<slug:slug>/', views.calender_delete, name='calender_delete'),

    # =================================================================================
    # giving
    # ================================================================================= 
    path('live_videos/', views.live_video_list, name='live_video_list'),
    path('live_videos/<str:pk>/update/', views.live_video_update, name='live_video_update'),
    path('live_videos/<str:pk>/delete/', views.live_video_delete, name='live_video_delete'),

    # =================================================================================
    # carousels 
    # ================================================================================= 
    path('create/carousel/', views.create_carousel, name='carousel'),
    path('update/<int:pk>/', views.update_carousel, name='update_carousel'),
    path('delete/<int:pk>/', views.delete_carousel, name='delete_carousel'),

]