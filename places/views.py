from django.shortcuts import render, get_object_or_404, redirect
from .models import Place, Booking
from .forms import PlaceForm
from django.db.models import Q
from .forms import SearchForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import BookingForm



def index(request):
    # Initialize the search form
    form = SearchForm()
    
    # Retrieve the search query from the GET parameters
    query = request.GET.get('query')
    
    # Start with all Place objects
    places = Place.objects.all()
    
    # If a query is present, filter the places based on the search criteria
    if query:
        places = places.filter(
            Q(name__icontains=query) | 
            Q(location__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Order the filtered places by the creation date (newest first) and limit to the top 10
    places = places.order_by('-created_at')[:10]

    # Pass the places and the form to the template context
    context = {
        'places': places,
        'form': form
    }
    
    # Render the index template with the context
    return render(request, 'places/index.html', context)


# def index(request):
#     places = Place.objects.all()
#     context = {'places': places}
#     return render(request, 'places/index.html', context)

def place_detail(request, pk):
    place = get_object_or_404(Place, pk=pk)
    context = {'place': place}
    return render(request, 'places/place_detail.html', context)

# def place_new(request):
#     if request.method == 'POST':
#         form = PlaceForm(request.POST)
#         if form.is_valid():
#             place = form.save()
#             return redirect('places:index')
#     else:
#         form = PlaceForm()
#     return render(request, 'places/place_form.html', {'form': form})
def place_new(request):
    if request.method == 'POST':
        print(request.FILES)  # Add this line to debug
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            place = form.save()
            print(place.picture.url)  # Add this line to debug
            return redirect('places:index')
    else:
        form = PlaceForm()
    return render(request, 'places/place_form.html', {'form': form})


@login_required
def make_booking(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.place = place
            booking.save()
            return redirect('places:booking_success', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'places/make_booking.html', {'form': form, 'place': place})

@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'places/booking_success.html', {'booking': booking})





