from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('accounts/', include('django.contrib.auth.urls')),
]

