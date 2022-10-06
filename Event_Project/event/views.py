from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from event.models import Event, Comment


def home(request):
    events = Event.objects.all()  # najdeme všechny místnosti

    context = {'events': events}

    return render(request, 'event/home.html', context)


def login(request):
    return render(request, 'event/login.html')


def signup(request):
    return render(request, 'account/signup.html')

@login_required
def search(request):
    if request.method == 'POST': # pokial posleme dotaz z formulara
        s = request.POST.get('search') # z odeslane promenne si vytiahnem co chcem hladat
        s = s.strip()                    # ak da niekto do contextoveho okna prazdne a enter
        if len(s) > 0:
            events = Event.objects.filter(name__contains=s) # vyfiltruje miestnosti
            comments = Comment.objects.filter(body__contains=s) # vyfiltruje spravy

            context = {'events': events, 'comments': comments, 'search': s} # ulozi do contextu
            return render(request, 'event/search.html', context)  # a vyrenderuje a odosle na search.html
        else:
            context = {'events': None, 'comments': None} # ak by bol prazdnu formular alebo niekto len v url dal search
            # return redirect ('home') # alebo 2.alternativa vrati to na home
    return redirect('home') #  tu je pouzita uz 2. atlernativa


@login_required
def event(request, pk):
    event = Event.objects.get(id=pk)  # najdeme místnost se zadaným id
    comments = Comment.objects.filter(event=pk)  # vybereme všechny zprávy dané místnosti

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

    context = {'event': event, 'comments': comments}
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
        if len(name) > 0 and len(descr) > 0:
            event = Event.objects.create(
                host=request.user,
                name=name,
                description=descr
            )

            return redirect('event', pk=event.id)

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
