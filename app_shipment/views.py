from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from app_shipment.models import Shipment
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import json
from .models import ShipmentStatus

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')


def search(request):
    query = request.GET.get('query', '').strip()
    results = Shipment.objects.filter(tracking_number__tracking_number__icontains=query) if query else []
    
    return render(request, 'track.html', {'results': results, 'query': query})

def track(request):
    query = request.GET.get('query', '').strip()  # Get and clean user input
    results = None  # Default: No query results

    if query:  # Only search when query is provided
        try:
            shipment = Shipment.objects.get(tracking_number=query)  # Get Shipment object
            results = ShipmentStatus.objects.filter(tracking_number=shipment)  # Get status updates
        except Shipment.DoesNotExist:
            results = []  # Return an empty list if no shipment is found

    return render(request, 'track.html', {'results': results, 'query': query})
@login_required
def dashboard(request):
    search_query = request.GET.get('search', '').strip()

    if request.user.is_superuser or request.user.is_staff:
        # Superusers and staff see all shipments
        shipments = Shipment.objects.filter(tracking_number__icontains=search_query) if search_query else Shipment.objects.all()
    else:
        # Regular users see only their shipments
        shipments = Shipment.objects.filter(user=request.user, tracking_number__icontains=search_query) if search_query else Shipment.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {'shipments': shipments, 'search_query': search_query})

@login_required
def changeStatus(request):
    statuses = ["Package Created", "Dispatched", "Arrived at Local Storage", "Out for Delivery", "Delivered", "Returned"]
    search_query = request.GET.get('search', '')
    shipments = []

    if request.user.is_superuser:
        if search_query:
            shipments = Shipment.objects.filter(tracking_number__icontains=search_query)
        else:
            shipments = Shipment.objects.all()

    return render(request, 'changeStatus.html', {'shipments': shipments, 'search_query': search_query, 'statuses': statuses})

@login_required
def update_status(request, shipment_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_status = data.get("status")
            
            # Ensure status is a valid option
            valid_statuses = ["Package Created", "Dispatched", "Arrived at Local Storage", "Out for Delivery", "Delivered", "Returned"]
            if new_status not in valid_statuses:
                return JsonResponse({"success": False, "error": "Invalid status"})

            # Fetch the shipment and update its status
            shipment = Shipment.objects.get(id=shipment_id)
            shipment.current_status = new_status
            shipment.save()

            return JsonResponse({"success": True})
        except Shipment.DoesNotExist:
            return JsonResponse({"success": False, "error": "Shipment not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"success": False, "error": "Invalid request"})
