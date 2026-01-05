"""
Karura SDA Dashboard Callback
Dynamic dashboard with church statistics and recent activity
"""

from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
from django.urls import reverse_lazy, reverse, NoReverseMatch
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.core.cache import cache

from base.models import (
    Blog, Category, Comment, Event, Leader, Ministry,
    Gallery, Sermon, Song, LiveStream, Carousel, Family, Member
)


def get_admin_url_for_logentry(logentry):
    """Helper function to get admin URL for a LogEntry object"""
    if logentry.object_id and logentry.action_flag != DELETION:
        try:
            url_name = f"admin:{logentry.content_type.app_label}_{logentry.content_type.model}_change"
            return reverse(url_name, args=[logentry.object_id])
        except (NoReverseMatch, ValueError):
            try:
                url_name = f"admin:{logentry.content_type.app_label}_{logentry.content_type.model}_changelist"
                return reverse(url_name)
            except (NoReverseMatch, ValueError):
                return None
    return None


def safe_admin_url(app_label, model_name, action='changelist', object_id=None):
    """Safely generate admin URLs with fallback"""
    try:
        if action == 'change' and object_id:
            url_name = f"admin:{app_label}_{model_name}_change"
            return reverse(url_name, args=[object_id])
        else:
            url_name = f"admin:{app_label}_{model_name}_changelist"
            return reverse(url_name)
    except (NoReverseMatch, ValueError):
        return reverse('admin:index')


# Monkey patch LogEntry
LogEntry.get_admin_url = property(lambda self: get_admin_url_for_logentry(self))


def get_trend_data(current, previous):
    """Calculate trend percentage and direction"""
    if previous == 0:
        if current > 0:
            return {'percentage': 100, 'direction': 'up', 'class': 'positive'}
        return {'percentage': 0, 'direction': 'neutral', 'class': 'neutral'}

    percentage = ((current - previous) / previous) * 100
    direction = 'up' if percentage > 0 else 'down' if percentage < 0 else 'neutral'
    css_class = 'positive' if percentage > 0 else 'negative' if percentage < 0 else 'neutral'

    return {
        'percentage': abs(round(percentage, 1)),
        'direction': direction,
        'class': css_class
    }


def dashboard_callback(request, context):
    """
    Karura SDA Dashboard Callback
    Displays church statistics, recent content, and activity
    """
    now = timezone.now()
    today = now.date()
    last_week = now - timedelta(days=7)
    two_weeks_ago = now - timedelta(days=14)
    last_month = now - timedelta(days=30)

    # Cache key for dashboard data (5 minutes cache)
    cache_key = f'dashboard_data_{request.user.id}'
    cached_data = cache.get(cache_key)

    if cached_data and not request.GET.get('refresh'):
        context.update(cached_data)
        return context

    # ===== STATISTICS =====

    # Blog statistics
    blog_stats = Blog.objects.aggregate(
        total=Count('id'),
        this_week=Count('id', filter=Q(created__gte=last_week)),
        last_week=Count('id', filter=Q(created__gte=two_weeks_ago, created__lt=last_week)),
    )

    # Event statistics
    event_stats = Event.objects.aggregate(
        total=Count('id'),
        upcoming=Count('id', filter=Q(eventDate__gte=today)),
        past=Count('id', filter=Q(eventDate__lt=today)),
        this_week=Count('id', filter=Q(eventDate__gte=today, eventDate__lte=today + timedelta(days=7))),
    )

    # Comment statistics
    comment_stats = Comment.objects.aggregate(
        total=Count('id'),
        this_week=Count('id', filter=Q(created__gte=last_week)),
    )

    # Simple counts
    counts = {
        'categories': Category.objects.count(),
        'ministries': Ministry.objects.count(),
        'leaders': Leader.objects.count(),
        'families': Family.objects.count(),
        'members': Member.objects.count(),
        'gallery_images': Gallery.objects.count(),
        'sermons': Sermon.objects.count(),
        'songs': Song.objects.count(),
        'carousels': Carousel.objects.count(),
    }

    # ===== RECENT ACTIVITY =====

    # Recent admin logs
    recent_admin_logs = LogEntry.objects.select_related(
        'user', 'content_type'
    ).filter(
        action_time__gte=last_week
    ).order_by('-action_time')[:10]

    # Recent blogs
    recent_blogs = Blog.objects.select_related(
        'category'
    ).order_by('-created')[:5]

    # Recent events
    recent_events = Event.objects.order_by('-created')[:5]

    # Upcoming events
    upcoming_events = Event.objects.filter(
        eventDate__gte=today
    ).order_by('eventDate')[:5]

    # Recent comments
    recent_comments = Comment.objects.select_related(
        'blog'
    ).order_by('-created')[:5]

    # ===== TREND CALCULATIONS =====

    blog_trend = get_trend_data(
        blog_stats['this_week'] or 0,
        blog_stats['last_week'] or 0
    )

    # ===== ALERTS & NOTIFICATIONS =====

    alerts = []

    # Check for upcoming events
    if event_stats['this_week'] and event_stats['this_week'] > 0:
        alerts.append({
            'type': 'info',
            'icon': 'event',
            'title': f'{event_stats["this_week"]} Events This Week',
            'message': 'Upcoming events in the next 7 days',
            'url': safe_admin_url('base', 'event') + f'?eventDate__gte={today}',
        })

    # Check for recent comments
    if comment_stats['this_week'] and comment_stats['this_week'] > 0:
        alerts.append({
            'type': 'success',
            'icon': 'comment',
            'title': f'{comment_stats["this_week"]} New Comments',
            'message': 'New comments on blog posts this week',
            'url': safe_admin_url('base', 'comment'),
        })

    # ===== BUILD CONTEXT =====

    dashboard_data = {
        "dashboard_title": "Karura SDA Church Dashboard",
        "last_updated": now,

        # Key Performance Indicators
        "kpi_cards": {
            "events": {
                "title": "Upcoming Events",
                "value": event_stats['upcoming'] or 0,
                "subtitle": f"{event_stats['this_week'] or 0} this week",
                "icon": "event",
                "color": "blue",
                "url": safe_admin_url("base", "event") + f'?eventDate__gte={today}',
                "stats": {
                    "Total Events": event_stats['total'] or 0,
                    "Past Events": event_stats['past'] or 0,
                }
            },
            "blogs": {
                "title": "Blog Posts",
                "value": blog_stats['total'] or 0,
                "subtitle": f"{blog_stats['this_week'] or 0} this week",
                "icon": "article",
                "color": "green",
                "trend": blog_trend,
                "url": safe_admin_url("base", "blog"),
                "stats": {
                    "This Week": blog_stats['this_week'] or 0,
                }
            },
            "members": {
                "title": "Church Members",
                "value": counts['members'],
                "subtitle": f"{counts['families']} families",
                "icon": "people",
                "color": "purple",
                "url": safe_admin_url("base", "member"),
                "stats": {
                    "Families": counts['families'],
                    "Leaders": counts['leaders'],
                }
            },
            "media": {
                "title": "Media Library",
                "value": counts['sermons'] + counts['songs'],
                "subtitle": f"{counts['gallery_images']} photos",
                "icon": "video_library",
                "color": "orange",
                "url": safe_admin_url("base", "sermon"),
                "stats": {
                    "Sermons": counts['sermons'],
                    "Songs": counts['songs'],
                    "Gallery": counts['gallery_images'],
                }
            },
        },

        # Quick Stats Grid
        "quick_stats": {
            "ministries": {
                "title": "Ministries",
                "count": counts['ministries'],
                "icon": "groups",
                "url": safe_admin_url("base", "ministry"),
            },
            "leaders": {
                "title": "Leaders",
                "count": counts['leaders'],
                "icon": "engineering",
                "url": safe_admin_url("base", "leader"),
            },
            "comments": {
                "title": "Comments",
                "count": comment_stats['total'] or 0,
                "icon": "comment",
                "url": safe_admin_url("base", "comment"),
            },
            "categories": {
                "title": "Categories",
                "count": counts['categories'],
                "icon": "category",
                "url": safe_admin_url("base", "category"),
            },
        },

        # Alerts
        "alerts": alerts,

        # Recent Activity
        "recent_admin_logs": recent_admin_logs,

        # Recent Content Lists
        "recent_activity": {
            "recent_blogs": [{
                "data": blog,
                "url": safe_admin_url("base", "blog", "change", blog.id)
            } for blog in recent_blogs],

            "recent_events": [{
                "data": event,
                "url": safe_admin_url("base", "event", "change", event.id)
            } for event in recent_events],

            "recent_comments": [{
                "data": comment,
                "url": safe_admin_url("base", "comment", "change", comment.id)
            } for comment in recent_comments],
        },

        # Upcoming Content
        "upcoming_content": {
            "upcoming_events": [{
                "data": event,
                "url": safe_admin_url("base", "event", "change", event.id)
            } for event in upcoming_events],
        },

        # Church Info
        "church_info": {
            "name": "Karura SDA Church",
        },
    }

    # Cache for 5 minutes
    cache.set(cache_key, dashboard_data, 300)

    context.update(dashboard_data)
    return context
