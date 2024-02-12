from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking
from .models import Rating
from django import forms 

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields= ['username','email','password1','password2']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date'] 
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

        
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'comment']        