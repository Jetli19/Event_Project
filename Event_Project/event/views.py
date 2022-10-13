from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import AbstractUser, User
from event.models import Event, Comment
from datetime import *


def home(request):
    events = Event.objects.all()  # najdeme všechny místnosti

    context = {'events': events}

    return render(request, 'event/home.html', context)


def signup(request):
    return render(request, 'account/signup.html')


@login_required
def search(request):
    if request.method == 'POST':  # pokud pošleme dotaz z formuláře
        s = request.POST.get('search')                       # z odeslané proměnné si vytáhnu, co chci hledat
        s = s.strip()                                        # ořízneme prázdné znaky
        if len(s) > 0:                                       # pkud s obsahuje alespoň jeden znak
            events = Event.objects.filter(name__contains=s)        # vyfiltruji místnosti dle zadaného řetězce
            comments = Comment.objects.filter(body__contains=s)  # vyfiltruji zprávy dle zadaného řetezce

            context = {'events': events, 'comments': comments, 'search': s}     # výsledky uložím do kontextu
            return render(request, "event/search.html", context)  # vykreslíme stránku s výsledky
        return redirect('home')
        # pokud POST nebyl odeslán
    # context = {'rooms': None, 'messages': None}        # místnosti i zprávy budou prázdné
    return redirect('home')                              # případně lze přesměrovat na jinou stránku


@login_required
def event(request, pk):
    event = Event.objects.get(id=pk)  # najdeme místnost se zadaným id
    comments = Comment.objects.filter(event=pk)  # vybereme všechny zprávy dané místnosti
    participants = event.participants

    # pokud zadáme novou zprávu, musíme ji zpracovat
    if request.method == 'POST':
        file_url = ""
        if request.FILES.get('upload'):                        # pokud jsme poslali soubor
            upload = request.FILES['upload']               # z requestu si vytáhnu soubor
            file_storage = FileSystemStorage()             # práce se souborovým systémem
            file = file_storage.save(upload.name, upload)  # uložíme soubor na disk
            file_url = file_storage.url(file)              # vytáhnu ze souboru url adresu a uložím
        body = request.POST.get('body').strip()
        if len(body) > 0 or request.FILES.get('upload'):
            comment = Comment.objects.create(
                user=request.user,
                event=event,
                body=body,
                file=file_url                              # vložíme url souboru do databáze
            )
        return HttpResponseRedirect(request.path_info)

    context = {'event': event, 'comments': comments, 'participants': participants}
    return render(request, "event/event.html", context)


@login_required
def events(request):
    events = Event.objects.all()

    context = {'events': events}
    return render(request, "event/events.html", context)


@login_required
def create_event(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        descr = request.POST.get('descr').strip()

        if not request.POST.get('start_date'):
            return render(request, 'event/create_event.html')

        start_event = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()

        if not request.POST.get('end_date'):
            return render(request, 'event/create_event.html')

        end_event = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d').date()

        # TODO: next if back to the version of mine:

        if len(name) > 0 and len(descr) > 0 and start_event <= end_event:
            event = Event.objects.create(
                host=request.user,
                name=name,
                description=descr,
                start_event=start_event,
                end_event=end_event,
            )

            return redirect('event', pk=event.id)

        elif start_event > end_event:
            message = 'Start of the event is set after the end of the event.'
            context = {'message': message}
            return render(request, 'event/create_event.html', context)

    return render(request, 'event/create_event.html')

@login_required
def delete_event(request, pk):
    event = Event.objects.get(id=pk)
    if event.comments_count() == 0:  # pokud v místnosti není žádná zpráva
        event.delete()               # tak místnost smažeme

        return redirect('events')

    context = {'event': event, 'comment_count': event.comments_count()}
    return render(request, 'event/delete_event.html', context)


@login_required
def delete_event_yes(request, pk):
    event = Event.objects.get(id=pk)
    event.delete()
    return redirect('events')


class EventEditForm(ModelForm):

    class Meta:
        model = Event
        fields = '__all__'


@method_decorator(login_required, name='dispatch')
class EditEvent(UpdateView):
    template_name = 'event/edit_event.html'
    model = Event
    form_class = EventEditForm
    success_url = reverse_lazy('events')


@method_decorator(login_required, name='dispatch')
class JoinEvent(UpdateView):
    template_name = 'event/event.html'
    model = Event
    form_class = EventEditForm
    success_url = reverse_lazy('events')

    def __init__(self):
        self.event = None
        self.user = None

    def join_event(self, pk1, pk2):
        self.event = Event.objects.get(id=pk1)
        self.user = User.objects.get(id=pk2)
        self.event.participants.add(self.user)
        return redirect('events')
