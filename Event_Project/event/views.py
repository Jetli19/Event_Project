from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from event.models import Event, Comment
from datetime import *
from profiles.models import Profile


def home(request):
    events = Event.objects.all()  # najdeme všechny místnosti

    context = {'events': events}

    return render(request, 'event/home.html', context)


def signup(request):
    if not request.method == 'POST':
        return render(request, 'accounts/signup.html')  # TODO: warning: changed: account/ -- > accounts/
    elif request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email__contains=email):
            return render(request, 'accounts/signup.html')  # TODO: warning: changed: account/ -- > accounts/
        else: # TODO - not functioning
            # User.objects.create()
            ## user = User.objects.create(
            ## user = request.user
            ##)
            return render(request, 'event/home.html') # 'registration/login.html'

    # return render(request, 'accounts/signup.html') # TODO: warning: changed: account/ -- > accounts/


@login_required
def search(request):
    if request.method == 'POST':  # pokud pošleme dotaz z formuláře
        s = request.POST.get('search')                       # z odeslané proměnné si vytáhnu, co chci hledat
        s = s.strip()                                        # ořízneme prázdné znaky
        if len(s) > 0:                                       # pkud s obsahuje alespoň jeden znak
            events = Event.objects.filter(name__contains=s)        # vyfiltruji místnosti dle zadaného řetězce
            # comments = Comment.objects.filter(body__contains=s)  # vyfiltruji zprávy dle zadaného řetezce

            context = {'events': events, 'search': s}     # výsledky uložím do kontextu
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
        if request.FILES.get('upload'):                    # pokud jsme poslali soubor
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
    try:
        profile = Profile.objects.get(user=request.user)
        admin = profile.admin
    except:
        admin = False

    context = {'events': events, 'admin': admin}
    return render(request, "event/events.html", context)


@login_required
def create_event(request):
    today = date.today()
    if request.method == 'POST':
        file_url = ''
        if request.FILES.get('upload_cre'):  # pokud jsme poslali soubor
            upload = request.FILES['upload_cre']  # z requestu si vytáhnu soubor
            file_storage = FileSystemStorage()  # práce se souborovým systémem
            file = file_storage.save(upload.name, upload)  # uložíme soubor na disk
            file_url = file_storage.url(file)  # vytáhnu ze souboru url adresu a uložím

        name = request.POST.get('name').strip()

        if not name:
            empty_name = 'The title of the event cannot be empty.'
            context = {'empty_name': empty_name}
            return render(request, 'event/create_event.html', context)

        descr = request.POST.get('descr').strip()

        if not descr:
            empty_descr = 'The description of the event cannot be empty.'
            context = {'empty_descr': empty_descr}
            return render(request, 'event/create_event.html', context)

        if len(descr) < 20:
            short_descr = 'The description has to have in the minimum 20 characters.'
            context = {'short_descr': short_descr}
            return render(request, 'event/create_event.html', context)

        if len(descr) > 500:
            long_descr = 'The description has to have in the maximum 500 characters.'
            context = {'long_descr': long_descr}
            return render(request, 'event/create_event.html', context)

        location = request.POST.get('location').strip()
        if not location:
            empty_location = 'The location of the event cannot be empty.'
            context = {'empty_location': empty_location}
            return render(request, 'event/create_event.html', context)

        if not request.POST.get('start_date'):
            return render(request, 'event/create_event.html')

        start_event = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()

        if not request.POST.get('end_date'):
            return render(request, 'event/create_event.html')

        end_event = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d').date()

        if len(name) > 0 and len(descr) > 0 and start_event >= today and end_event >= today and start_event <= end_event and request.FILES.get('upload_cre'):
            event = Event.objects.create(
                host=request.user,
                name=name,
                description=descr,
                location=location,
                start_event=start_event,
                end_event=end_event,
                file = file_url
            )

            return redirect('event', pk=event.id)  # # NEW PA 17-1-v2
            # return HttpResponseRedirect(request.path_info)

        elif len(name) > 0 and len(descr) > 0 and start_event >= today and end_event >= today and start_event <= end_event and not request.FILES.get('upload_cre'):
            event = Event.objects.create(
                host=request.user,
                name=name,
                description=descr,
                location=location,
                start_event=start_event,
                end_event=end_event
            )

            return redirect('event', pk=event.id)  # # NEW PA 17-1-v2
            # return HttpResponseRedirect(request.path_info)

        elif start_event < today:
            message = 'Start of the event is set in the past.'
            context = {'message': message}
            return render(request, 'event/create_event.html', context)
        elif end_event < today:
            message = 'End of the event is set in the past.'
            context = {'message': message}
            return render(request, 'event/create_event.html', context)
        elif start_event > end_event:
            message = 'Start of the event is set after the end of the event.'
            context = {'message': message}
            return render(request, 'event/create_event.html', context)
        else:
            pass

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


# @method_decorator(login_required, name='dispatch')
# class JoinEvent(UpdateView):
#     template_name = 'event/event.html'
#     model = Event
#     form_class = EventEditForm
#     success_url = reverse_lazy('events')
#
#     def __init__(self):
#         self.event = None
#         self.user = None
#
#     @login_required
#     def join_event(self, pk1, pk2):
#         self.event = Event.objects.get(id=pk1)
#         self.user = User.objects.get(id=pk2)
#         self.event.participants.add(self.user)
#         return redirect('events')
#
#     @login_required
#     def unjoin_event(self, pk1, pk2):
#         self.event = Event.objects.get(id=pk1)
#         self.user = User.objects.get(id=pk2)
#         self.event.participants.remove(self.user)
#         return redirect('events')

@login_required
def join_event(request, pk1, pk2):
    event = Event.objects.get(id=pk1)
    user = User.objects.get(id=pk2)
    event.participants.add(user)
    return redirect('event', pk=event.id)

@login_required
def unjoin_event(request, pk1, pk2):
    event = Event.objects.get(id=pk1)
    user = User.objects.get(id=pk2)
    context = {'event': event}
    return render(request, 'event/unjoin_event.html', context)

@login_required
def unjoin_event_yes(request, pk1, pk2):
    event = Event.objects.get(id=pk1)
    user = User.objects.get(id=pk2)
    event.participants.remove(user)
    return redirect('events')
