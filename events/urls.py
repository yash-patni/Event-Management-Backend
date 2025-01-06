from django.urls import path
from . import views


urlpatterns = [
    # Events routes
    path('events/', views.show_all_events, name='show_all_events'),
    path('events/add/', views.add_event, name='add_event'),
    path('events/remove/', views.remove_event, name='remove_event'),
    path('events/filter/', views.filter_events, name='filter_events'),
    path('events/update/', views.update_event, name='update_event'),
    # Attendees Routes
    path('attendees/', views.show_all_attendees, name='show_all_attendees'),
    path('attendees/add/', views.add_attendee, name='add_attendee'),
    path('attendees/remove/', views.remove_attendee, name='remove_attendee'),
    path('attendees/filter/', views.filter_attendees, name='filter_attendees'),
    path('attendees/update/', views.update_attendee, name='update_attendee'),
]
