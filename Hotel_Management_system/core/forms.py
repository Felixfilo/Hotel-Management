from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Room, Reservation, Customer

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'type', 'price', 'status']

class ReservationForm(forms.ModelForm):
    customer_name = forms.CharField(max_length=100, required=True, help_text="Enter the customer's full name")
    room = forms.ModelChoiceField(queryset=Room.objects.all(), empty_label="Select a room")

    class Meta:
        model = Reservation
        fields = ['customer_name', 'room', 'check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        room = cleaned_data.get('room')

        if check_in and check_out and room:
            # Check if the room is available for the selected dates
            conflicting_reservations = Reservation.objects.filter(
                room=room,
                check_out__gt=check_in,
                check_in__lt=check_out
            ).exclude(pk=self.instance.pk)

            if conflicting_reservations.exists():
                raise forms.ValidationError("This room is not available for the selected dates.")

        return cleaned_data

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']