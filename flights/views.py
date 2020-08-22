from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from .models import Flight, Passenger
# Create your views here.
def index(request):
    return render(request, "flights/index.html",  {
        "flights":Flight.objects.all()
    })
# flight.passenger.all() we can do this because of passenger is related name
def flight(request, flight_id):
    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight not found.")
    return render(request, "flights/flight.html", {
        "flight": flight, 
        "passengers": flight.passenger.all(),
        "non_passegers": Passenger.objects.exclude(flights=flight).all()
    })

def book(request, flight_id):
    if request.method == "POST":
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        flight = Flight.objects.get(pk=flight_id)        
        passenger.flights.add(flight)

        return HttpResponseRedirect(reverse("flight", args=(flight.id))) 