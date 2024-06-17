from .models import Tour, Customer, Hotel,Comment,Reservation,ReservationHotel
from django.forms import ModelForm, TextInput, Textarea, NumberInput, DateInput


class TourForm(ModelForm):
    class Meta:
        model = Tour
        fields = "__all__"
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Enter the name'
            }),
            "description": Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Enter the description'
            }),
            "started": DateInput(attrs={
                'class': 'form-control', 'placeholder': 'Enter started date', 'type': 'date'
            }),
            "price": NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Enter price of the tour'
            }),
            "duration": NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Enter duration'
            }),
        }


class HotelForm(ModelForm):
    class Meta:
        model = Hotel
        fields = "__all__"
        # widgets = {
        #     "name": TextInput(attrs={
        #         'class': 'form-control', 'placeholder': 'Enter the name of Hotel'
        #     }),
        #     "city": Textarea(attrs={
        #         'class': 'form-control', 'placeholder': 'Enter the city'
        #     }),
        #     "hotelClass": DateInput(attrs={
        #         'class': 'form-control', 'placeholder': 'Enter the class of a hotel'
        #     }),
        #     "price": NumberInput(attrs={
        #         'class': 'form-control', 'placeholder': 'Enter price of the hotel to the one person'
        #     }),
        # }


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        widgets = {
            "phone": TextInput(attrs={'class':'form-control'}),
            "place": TextInput(attrs={'class': 'form-control'}),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','description')
        widgets = {
            "name": TextInput(attrs={'class':'form-control'}),
            "email": TextInput(attrs={'class': 'form-control'}),
            "description": TextInput(attrs={'class': 'form-control'}),
        }


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ('name','email','phone','number_card','Name_of_the_card_holder','cvc')
        widgets = {
            "name": TextInput(attrs={'class':'form-control','placeholder':'Аты-жөні'}),
            "email": TextInput(attrs={'class': 'form-control','placeholder':'email'}),
            "phone": TextInput(attrs={'class': 'form-control','placeholder':'Tелефон нөмірі'}),
            "number_card": TextInput(attrs={'class': 'form-control','placeholder':'Карта нөмірі'}),
            "Name_of_the_card_holder": TextInput(attrs={'class': 'form-control','placeholder':'Несие карточкасын иеленушісінің Аты'}),
            "cvc": TextInput(attrs={'class': 'form-control','placeholder':'cvc'}),
        }


class ReservationHotelForm(ModelForm):
    class Meta:
        model = ReservationHotel
        fields = ('name','email','phone','number_card','Name_of_the_card_holder','cvc')
        widgets = {
            "name": TextInput(attrs={'class':'form-control','placeholder':'Аты-жөні'}),
            "email": TextInput(attrs={'class': 'form-control','placeholder':'email'}),
            "phone": TextInput(attrs={'class': 'form-control','placeholder':'Tелефон нөмірі'}),
            "number_card": TextInput(attrs={'class': 'form-control','placeholder':'Карта нөмірі'}),
            "Name_of_the_card_holder": TextInput(attrs={'class': 'form-control','placeholder':'Несие карточкасын иеленушісінің Аты'}),
            "cvc": TextInput(attrs={'class': 'form-control','placeholder':'cvc'}),
        }