from django.shortcuts import render, get_object_or_404, redirect
from .models import Place
from .forms import PlaceForm

def index(request):
    places = Place.objects.all()
    context = {'places': places}
    return render(request, 'places/index.html', context)

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