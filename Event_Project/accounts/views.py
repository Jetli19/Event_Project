# from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, get_user_model
from django.urls import reverse_lazy
from django.views import generic


class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = (  #"first_name", "last_name",
                  "email", "password1", "password2", "username")


class SignUpView(generic.CreateView):
    form_class = SignUpForm  # UserCreationForm
    success_url = reverse_lazy("home")
    template_name = 'accounts/signup.html'
