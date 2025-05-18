from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from polls.models import Order, Product

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Електронна пошта')
    first_name = forms.CharField(max_length=100, required=True, label='Ім\'я')
    last_name = forms.CharField(max_length=100, required=True, label='Прізвище')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Логін',
            'password1': 'Пароль',
            'password2': 'Підтвердження паролю',
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'phone']
        labels = {
            'address': 'Адреса доставки',
            'phone': 'Телефон',
        }
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProductQuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, label='Кількість')
    product_id = forms.IntegerField(widget=forms.HiddenInput())

class AdminOrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        labels = {
            'status': 'Статус замовлення',
        }
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class AdminProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'available']
        labels = {
            'name': 'Назва товару',
            'description': 'Опис',
            'price': 'Ціна',
            'image': 'Зображення',
            'category': 'Категорія',
            'available': 'Доступний',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class AdminPasswordChangeForm(PasswordChangeForm):
    """Форма для зміни пароля користувача адміністратором"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Видаляємо перевірку старого пароля, щоб адміністратор міг змінювати пароль без його знання
        self.fields.pop('old_password', None)