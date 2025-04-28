from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from .views import login_view, QuestionListView

app_name = 'polls'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('questions/', views.question_list, name='question_list'),
    path('register/', views.register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
