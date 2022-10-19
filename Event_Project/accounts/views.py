from django.contrib.auth.forms import UserCreationForm, get_user_model
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")
        User._meta.get_field('email')._unique = True
        User._meta.get_field('username').max_length = 50


class SignUpView(generic.CreateView):
    form_class = SignUpForm  # UserCreationForm
    success_url = reverse_lazy("home")
    template_name = 'accounts/signup2.html'
