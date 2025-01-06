from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt
def add_event(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))  
        except json.JSONDecodeError as e:
            return JsonResponse({"error": f"Invalid JSON format: {str(e)}"}, status=400)

        # Creating serializer instance with the parsed data
        serializer = EventSerializer(data=data)

        if serializer.is_valid(): 
            serializer.save() 
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    

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

# Update event and related attendees
@csrf_exempt
def update_event(request):
    if request.method == "PUT":
        event_id = request.GET.get('event_id')
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError as e:
            return JsonResponse({"error": f"Invalid JSON format: {str(e)}"}, status=400)

        event = get_object_or_404(Event, id=event_id)
        serializer = EventSerializer(event, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()

            if 'name' in data or 'location' in data:
                Attendee.objects.filter(event=event).update(event=event)
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    return JsonResponse({"error": "This endpoint only supports PUT requests"}, status=405)

# Update attendee
@csrf_exempt
def update_attendee(request):
    if request.method == "PUT":
        attendee_id = request.GET.get('attendee_id')
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError as e:
            return JsonResponse({"error": f"Invalid JSON format: {str(e)}"}, status=400)

        attendee = get_object_or_404(Attendee, id=attendee_id)
        serializer = AttendeeSerializer(attendee, data=data, partial=True)  

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    return JsonResponse({"error": "This endpoint only supports PUT requests"}, status=405)

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

# Filter attendees by name
def filter_attendees(request):
    name = request.GET.get('name')
    if not name:
        return JsonResponse({"error": "name parameter is required"}, status=400)
    attendees = Attendee.objects.filter(name=name)
    serializer = AttendeeSerializer(attendees, many=True)
    return JsonResponse(serializer.data, safe=False)
