from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from polls import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('polls.urls')),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]

# Додаємо обробку статичних та медіа файлів для режиму розробки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)