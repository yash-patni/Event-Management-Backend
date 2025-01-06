from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Event, Attendee
from .serializers import EventSerializer, AttendeeSerializer
import json

# Show all events
def show_all_events(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return JsonResponse(serializer.data, safe=False)

# Show all attendees
def show_all_attendees(request):
    attendees = Attendee.objects.all()
    serializer = AttendeeSerializer(attendees, many=True)
    return JsonResponse(serializer.data, safe=False)

# Add event
# @csrf_exempt
# def add_event(request):
#     if request.method == "POST":
#         print("added")
#         data = json.loads(request.body)
#         serializer = EventSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
@csrf_exempt
def add_event(request):
    if request.method == "POST":
        try:
            # Decode the request body (bytes to str) and parse it into a dictionary
            data = json.loads(request.body.decode('utf-8'))  # Convert byte data to dict
        except json.JSONDecodeError as e:
            return JsonResponse({"error": f"Invalid JSON format: {str(e)}"}, status=400)

        # Create serializer instance with the parsed data
        serializer = EventSerializer(data=data)

        if serializer.is_valid():  # Validate the data
            serializer.save()  # Save the event
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    # Return method not allowed if not POST
    return JsonResponse({"error": "This endpoint only supports POST requests"}, status=405)

# Add attendee
@csrf_exempt
def add_attendee(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        serializer = AttendeeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# Remove event
@csrf_exempt
def remove_event(request):
    if request.method == "DELETE":
        event_id = request.GET.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        return JsonResponse({"message": "Event deleted successfully"}, status=200)

# Remove attendee
@csrf_exempt
def remove_attendee(request):
    if request.method == "DELETE":
        attendee_id =  request.GET.get('attendee_id')
        attendee = get_object_or_404(Attendee, id=attendee_id)
        attendee.delete()
        return JsonResponse({"message": "Attendee deleted successfully"}, status=200)

# Filter events by location and date
def filter_events(request):
    location = request.GET.get('location')
    date = request.GET.get('date')
    events = Event.objects.all()

    if location:
        events = events.filter(location__icontains=location)
    if date:
        events = events.filter(date=date)

    serializer = EventSerializer(events, many=True)
    return JsonResponse(serializer.data, safe=False)

# Filter attendees by event
def filter_attendees(request):
    name = request.GET.get('name')
    if not name:
        return JsonResponse({"error": "name parameter is required"}, status=400)
    attendees = Attendee.objects.filter(name=name)
    serializer = AttendeeSerializer(attendees, many=True)
    return JsonResponse(serializer.data, safe=False)

###################################################################################

# from django.shortcuts import render

# # Create your views here.
# from rest_framework.viewsets import ModelViewSet
# from rest_framework import filters
# from django_filters.rest_framework import DjangoFilterBackend
# from .models import Event, Attendee
# from .serializers import EventSerializer, AttendeeSerializer

# class EventViewSet(ModelViewSet):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     filter_backends =  [DjangoFilterBackend, filters.SearchFilter]
#     filterset_fields = ['date', 'location']
#     search_fields = ['name']

# class AttendeeViewSet(ModelViewSet):
#     queryset = Attendee.objects.all()
#     serializer_class = AttendeeSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     filterset_fields = ['event']
#     search_fields = ['name']

# # def frontend(request):
# #     return render(request, 'index.html')