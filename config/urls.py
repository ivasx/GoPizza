from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from store import views
from store.views import admin_user_list, admin_change_user_password, admin_product_edit, admin_product_delete, \
    admin_product_create, admin_order_list, admin_order_status, RegisterView, LoginView

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
    path('', include('store.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
