from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from polls.forms import RegistrationForm, OrderForm, ProductQuantityForm, AdminOrderStatusForm, AdminProductForm, \
    AdminPasswordChangeForm
from polls.models import Product, Cart, CartItem, Order, OrderItem, Category
from reportlab.lib.units import inch
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
from django.conf import settings


# Реєстрація користувача
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Створюємо корзину для нового користувача
            Cart.objects.create(user=user)
            # Автоматичний вхід після реєстрації
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f"Аккаунт створено для {username}!")
            return redirect('polls:product_list')
    else:
        form = RegistrationForm()
    return render(request, 'polls/registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'polls/registration/login.html', {'error': 'Невірний логін або пароль'})
    return render(request, 'polls/registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

# Список товарів - доступний для всіх
def product_list(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')

    products = Product.objects.filter(available=True)

    if category_id:
        products = products.filter(category_id=category_id)

    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    context = {
        'categories': categories,
        'products': products,
        'current_category': category_id,
        'search_query': search_query
    }
    return render(request, 'polls/product_list.html', context)


# Деталі товару - доступні для всіх
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    form = ProductQuantityForm(initial={'product_id': product_id})
    context = {
        'product': product,
        'form': form
    }
    return render(request, 'polls/product_detail.html', context)


# Додавання товару до корзини - тільки для авторизованих
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        form = ProductQuantityForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            quantity = form.cleaned_data['quantity']

            product = get_object_or_404(Product, id=product_id, available=True)
            cart, created = Cart.objects.get_or_create(user=request.user)

            # Перевірка, чи товар вже є в корзині
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )

            # Якщо товар вже є в корзині, оновлюємо кількість
            if not item_created:
                cart_item.quantity += quantity
                cart_item.save()

            messages.success(request, f"{product.name} додано до корзини!")
            return redirect('polls:cart_detail')

    return redirect('polls:product_list')


# Перегляд корзини - тільки для авторизованих
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'polls/cart_detail.html', {'cart': cart})


# Видалення товару з корзини
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f"{product_name} видалено з корзини!")
    return redirect('polls:cart_detail')


# Оформлення замовлення
@login_required
def create_order(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Перевіряємо, чи є товари в корзині
    if not cart.items.exists():
        messages.warning(request, "Ваша корзина порожня!")
        return redirect('polls:product_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Переносимо товари з корзини до замовлення
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )

            # Очищаємо корзину
            cart.items.all().delete()

            messages.success(request, "Замовлення успішно оформлено!")
            return redirect('polls:order_detail', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'polls/order_create.html', {'form': form, 'cart': cart})


# Перегляд деталей замовлення
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'polls/order_detail.html', {'order': order})


# Список замовлень користувача
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'polls/order_list.html', {'orders': orders})


# Генерація PDF квитанції
@login_required
def order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    font_path = os.path.join(settings.BASE_DIR, 'media/fonts', 'DejaVuSans.ttf')
    if os.path.isfile(font_path):
        pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
        font_name = 'DejaVuSans'
    else:
        font_name = 'Helvetica'

    p.setFont(font_name, 16)
    p.drawString(inch, 10 * inch, f"Квитанція замовлення #{order.id}")

    p.setFont(font_name, 12)
    p.drawString(inch, 9.5 * inch, f"Дата: {order.created_at.strftime('%d.%m.%Y %H:%M')}")
    p.drawString(inch, 9.2 * inch, f"Клієнт: {order.user.get_full_name() or order.user.username}")
    p.drawString(inch, 8.9 * inch, f"Адреса доставки: {order.address}")
    p.drawString(inch, 8.6 * inch, f"Телефон: {order.phone}")
    p.drawString(inch, 8.3 * inch, f"Статус: {dict(Order.STATUS_CHOICES).get(order.status)}")

    p.setFont(font_name, 12)
    p.drawString(inch, 7.7 * inch, "Товари:")

    p.setFont(font_name, 10)
    p.drawString(inch, 7.3 * inch, "Назва")
    p.drawString(4 * inch, 7.3 * inch, "Ціна")
    p.drawString(5 * inch, 7.3 * inch, "Кількість")
    p.drawString(6 * inch, 7.3 * inch, "Сума")

    p.line(inch, 7.2 * inch, 7 * inch, 7.2 * inch)

    y = 7.0 * inch
    for item in order.items.all():
        if y < 2 * inch:
            p.showPage()
            p.setFont(font_name, 10)
            y = 10 * inch

        p.drawString(inch, y, item.product.name[:30])
        p.drawString(4 * inch, y, f"{item.price} грн")
        p.drawString(5 * inch, y, f"{item.quantity}")
        p.drawString(6 * inch, y, f"{item.get_cost()} грн")
        y -= 0.3 * inch

    p.line(inch, y, 7 * inch, y)
    y -= 0.3 * inch
    p.setFont(font_name, 12)
    p.drawString(4 * inch, y, "Всього:")
    p.drawString(6 * inch, y, f"{order.get_total_cost()} грн")

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order.id}.pdf"'

    return response


# Адміністративні функції

# Список всіх замовлень для адміністратора
@login_required
def admin_order_list(request):
    # Перевірка чи користувач є адміністратором
    if not request.user.is_superuser:
        raise Http404("Доступ заборонено")

    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'admin/order_list.html', {'orders': orders})


# Зміна статусу замовлення для адміністратора
@login_required
def admin_order_status(request, order_id):
    if not request.user.is_superuser:
        raise Http404("Доступ заборонено")

    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = AdminOrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f"Статус замовлення #{order.id} змінено!")
            return redirect('polls:admin_order_list')
    else:
        form = AdminOrderStatusForm(instance=order)

    return render(request, 'admin/order_status.html', {'form': form, 'order': order})


# Список товарів для адміністратора
@login_required
def admin_product_list(request):
    if not request.user.is_superuser:
        raise Http404("Доступ заборонено")

    products = Product.objects.all()
    return render(request, 'admin/product_list.html', {'products': products})


# Додавання нового товару
@login_required
def admin_product_create(request):
    if not request.user.is_superuser:
        raise Http404("Доступ заборонено")

    if request.method == 'POST':
        form = AdminProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Товар успішно додано!")
            return redirect('polls:admin_product_list')
    else:
        form = AdminProductForm()

    return render(request, 'admin/product_form.html', {'form': form, 'title': 'Додати новий товар'})


# Редагування товару
@login_required
def admin_product_edit(request, product_id):
    if not request.user.is_superuser:
        raise Http404("Доступ заборонено")

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = AdminProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Товар '{product.name}' успішно оновлено!")
            return redirect('polls:admin_product_list')
    else:
        form = AdminProductForm(instance=product)

    return render(request, 'admin/product_form.html', {'form': form, 'title': 'Редагувати товар', 'product': product})


# Видалення товару
@login_required
def admin_product_delete(request, product_id):
    if not request.user.is_superuser:
        raise Http404("Доступ заборонено")

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f"Товар '{product_name}' успішно видалено!")
        return redirect('polls:admin_product_list')

    return render(request, 'admin/product_confirm_delete.html', {'product': product})


# Список користувачів для адміністратора
@login_required
def admin_user_list(request):
    if not request.user.is_superuser:
        raise Http404("Доступ заборонено")

    users = User.objects.all()
    return render(request, 'admin/user_list.html', {'users': users})


# Зміна пароля користувача адміністратором
@login_required
def admin_change_user_password(request, user_id):
    if not request.user.is_superuser:
        raise Http404("Доступ заборонено")

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = AdminPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Пароль користувача {user.username} успішно змінено!")
            return redirect('polls:admin_user_list')
    else:
        form = AdminPasswordChangeForm(user)

    return render(request, 'admin/change_password.html', {'form': form, 'user_to_change': user})