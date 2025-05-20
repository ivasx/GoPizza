from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from polls import views
from polls.views import admin_user_list, admin_change_user_password, admin_product_edit, admin_product_delete, \
    admin_product_create, admin_order_list, admin_order_status

urlpatterns = [
    path('admin/users/', admin_user_list, name='admin_user_list'),
    path('admin/users/<int:user_id>/change-password/', admin_change_user_password, name='admin_change_user_password'),
    path('admin/orders/', admin_order_list, name='admin_order_list'),
    path('admin/orders/<int:order_id>/status/', admin_order_status, name='admin_order_status'),
    path('admin/products/<int:product_id>/edit/', admin_product_edit, name='admin_product_edit'),
    path('admin/products/create/', admin_product_create, name='admin_product_create'),
    path('admin/products/<int:product_id>/delete/', admin_product_delete, name='admin_product_delete'),
    path('admin/products/', views.admin_product_list, name='admin_product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('admin/', admin.site.urls),
    path('', include('polls.urls')),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
# Додаємо обробку статичних та медіа файлів для режиму розробки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
