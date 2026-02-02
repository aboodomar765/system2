from django import forms
from .models import Car,Expense

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'name',
            'year',
            'chassis_number',
            'CLEARANCE_CHOICES',
            'purchase_date',
            'purchase_price',
        ]



# class ExpenseForm(forms.ModelForm):
#     class Meta:
#          model = Expense
#          fields = '__all__'