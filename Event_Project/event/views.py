from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from event.models import Event


def home(request):
    events = Event.objects.all()  # najdeme všechny místnosti

    context = {'events': events}
    return render(request, 'event/home.html', context)
