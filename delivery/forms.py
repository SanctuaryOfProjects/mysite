from django import forms
from .models import *

class EstablishmentForm(forms.ModelForm):
    class Meta:
        model = Establishment
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'adress': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'verification': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'bin': forms.TextInput(attrs={'class': 'form-control'}),
            'work_schedule': forms.TextInput(attrs={'class': 'form-control'}),
            'legal_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'documentation': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class EstCouriersForm(forms.ModelForm):
    class Meta:
        model = EstCouriers
        fields = ['courier']
        widgets = {
            'courier': forms.Select(attrs={'class': 'form-select'})
        }

class CourierForm(forms.ModelForm):
    class Meta:
        model = Courier
        fields = ['fullname', 'email', 'work_phone', 'photo', 'username', 'password']
        labels = {
            'fullname': 'ФИО',
            'email': 'Email',
            'work_phone': 'Телефон',
            'photo': 'Фото',
            'username': 'Логин',
            'password': 'Пароль',
        }
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ФИО'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите Email'}),
            'work_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите телефон'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['sender', 'recipient', 'origin', 'destination', 'comment']
        widgets = {
            'sender': forms.Select(attrs={'class': 'form-select'}),
            'recipient': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя получателя'}),
            'origin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Точка отправки'}),
            'destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Точка назначения'}),
            'origin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Точка отправки'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Комментарий'}),
        }

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['courier', 'est', 'date', 'start_time', 'end_time']
        widgets = {
            'courier': forms.Select(attrs={'class': 'form-select'}),
            'est':  forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class SalaryCalculatorForm(forms.Form):
    courier = forms.ModelChoiceField(
        queryset=Courier.objects.all(),
        label="Выберите курьера",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    money_per_hour = forms.IntegerField(
        label="Заработная плата за час работы",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

class OrderStatusFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', '--- Все статусы ---'),
        ('Обработан', 'Обработан'), # Пустое значение для выбора всех статусов
        ('Доставляется', 'Доставляется'),
        ('Доставлен', 'Доставлен'),
        ('Отменен', 'Отменен'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, 
                               label='Статус заказа', required=False, 
                               widget=forms.Select(attrs={'class': 'form-control'}))

class SetSalaryForm(forms.Form):
    money_per_hour = forms.DecimalField(label='Зарплата за час работы', 
                                        min_value=0, 
                                        max_digits=10, 
                                        decimal_places=2, 
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))

class EstablishmentChoiceForm(forms.Form):
    establishment = forms.ModelChoiceField(
        queryset=Establishment.objects.all(),
        label='Выберите заведение',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }