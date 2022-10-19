from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AbstractUser # added for the function: email_exists
from django.forms import models # added for the function: email_exists
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from profiles.models import Profile # added for the function: email_exists


class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = (  #"first_name", "last_name",
                  "username", "email", "password1", "password2")

        User._meta.get_field('email')._unique = True
        User._meta.get_field('username').max_length = 50


class SignUpView(generic.CreateView):
    form_class = SignUpForm  # UserCreationForm
    success_url = reverse_lazy("home")
    template_name = 'accounts/signup.html'

    def len_username(self, request):
        if len(User._meta.get_field('username')) > 50:
            error_username_len = 'The length of username has to be 50 characters in the maximum.'
            context = {'error_username_len': error_username_len}

            return render(request, 'accounts/signup.html', context)

        else:
            return render(request, 'accounts/signup.html')

    def form_valid(self, form):
        pass
        '''
        if request.method == 'POST':
                is_in_emails = request.POST.get('email')
                email_is = Profile.user.get(email=is_in_emails)

                if email_is:

                    error_email_exists = 'This e-mail address already in database - not allowed.'
                    context = {'error_email_exists': error_email_exists}

                    return render(request, 'accounts/signup.html', context)
                    # return HttpResponseRedirect(request.path_info)

                else:
                    return render(request, 'accounts/signup.html')
                    # raise forms.ValidationError("Email is not unique")
        '''
