from django import forms
from dining_hall.food.models import Food

class FoodAddForm(forms.ModelForm):

    class Meta:
        model = Food
        fields = [
            'description', 'total_quantity', 'date', 'type_food',
            'registered_user'
        ]