from django import forms
from dining_hall.food.models import Food, Reservation


class FoodAddForm(forms.ModelForm):

    class Meta:
        model = Food
        fields = [
            'description', 'total_quantity', 'date', 'type_food',
            'registered_user'
        ]


class PendingRemoveForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ['motive']
        widgets = {
            'motive': forms.Textarea(attrs={'rows': 3}),
        }
