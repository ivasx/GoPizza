from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from ..forms import RegistrationForm
from django.views.generic.edit import CreateView
from ..models import Cart


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    success_url = reverse_lazy('store:product_list')
    form_class = RegistrationForm
    success_message = "Your profile was created successfully"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        Cart.objects.create(user=user)
        login(self.request, user)
        return response


class LoginView(SuccessMessageMixin, DjangoLoginView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm
    success_message = "You have successfully logged in"
