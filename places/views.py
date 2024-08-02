from django.shortcuts import render, get_object_or_404, redirect
from .models import Place
from .forms import PlaceForm

def index(request):
    return render(request, 'places/index.html')

def place_list(request):
    places = Place.objects.all()
    return render(request, 'places/place_list.html', {'places': places})

def place_detail(request, pk):
    place = get_object_or_404(Place, pk=pk)
    return render(request, 'places/place_detail.html', {'place': place})

def place_new(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            place = form.save()
            return redirect('place_detail', pk=place.pk)
    else:
        form = PlaceForm()
    return render(request, 'places/place_form.html', {'form': form})
