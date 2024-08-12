from django import forms
from .models import Place
from .models import Booking

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'description', 'location', 'price', 'picture']
        
class SearchForm(forms.Form):
    query = forms.CharField(label='Search for places', max_length=255)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }