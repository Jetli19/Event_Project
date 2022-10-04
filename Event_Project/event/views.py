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


def login(request): # TODO - asi docasne
    return render(request, 'event/login-page.html')

def signup(request):  # TODO - asi docasne
    return render(request, 'event/signup.html')

'''
@login_required
def search(request):
    if request.method == 'POST': # pokial posleme dotaz z formulara
        s = request.POST.get('search') # z odeslane promenne si vytiahnem co chcem hladat
        s = s.strip()                    # ak da niekto do contextoveho okna prazdne a enter
        if len(s) > 0:
            rooms = Room.objects.filter (name__contains=s) # vyfiltruje miestnosti
            messages = Message.objects.filter (body__contains=s) # vyfiltruje spravy

            context = {'rooms': rooms, 'messages': messages, 'search': s} # ulozi do contextu
            return render(request, 'chatterbox/search.html', context)  # a vyrenderuje a odosle na search.html
        else:
            context = {'rooms': None, 'messages': None} # ak by bol prazdnu formular alebo niekto len v url dal search
            # return redirect ('home') # alebo 2.alternativa vrati to na home
    return redirect('home') #  tu je pouzita uz 2. atlernativa
'''

# # API na search
# # povodne bez templates
# '''def search(request,s):
#     rooms = Room.objects.filter(name__contains=s) # namiesto s budeme davat uz co sa bude hladat
#     response = "Rooms: "
#     for room in rooms:
#         response += room.name + ", "
#     # return HttpResponse(rooms)
#
#     messages = Message.objects.filter(body__contains=s) # namiesto s budeme davat uz co sa bude hladat
#     response += "<br>Messages: "
#     for message in messages:
#         response += message.body[0:10] + " ... , " # [0:10] zobrazi len zaciatok spravy a zbytok spravi ...
#
#     return render(request, "chatterbox/search.html", context)'''
#
# #  pak sme prerobili na toto s pomocou uz search html, odkial sa odkazujeme na context
# # @login_required
# # def search(request, s):
# #     rooms = Room.objects.filter(name__contains=s)  # namiesto 's' budeme davat uz co sa bude hladat
# #     messages = Message.objects.filter(body__contains=s)  # namiesto 's' budeme davat uz co sa bude hladat
# #
# #     context = {'rooms': rooms, 'messages': messages} # vysledok=context a zobrazi rooms a messages s hladanym slovom
# #     return render(request, "chatterbox/search.html", context)
'''
@login_required
def room(request, pk):
    room = Room.objects.get(id=pk) # najde miestnost pomocou ID miestnosti resp PK
    messages = Message.objects.filter(room=pk) # zobrazi spravy v danej miestnosti

    # pokud zadame novou spravu, musim ju spracovat
    if request.method == 'POST': # ak odoslem spravu, pouzije sa prikaz POST z room.html
        file_url = ""
        if request.FILES.get('upload'):                    # pokial sme poslali subor
            upload = request.FILES['upload']            # z requestu si vytiahnem subor
            file_storage = FileSystemStorage()          # praca so suborovym systemom
            file = file_storage.save(upload.name, upload) # ulozime subor na disk
            file_url = file_storage.url(file)               # vytiahne zo suboru url adresu a ulozi
        body = request.POST.get ('body').strip() # osetri nam aby nesli odoslat prazdne spravy pripadne s medzernikom

        if len(body) > 0 or request.FILES.get('upload'):
            message = Message.objects.create(
                user = request.user,
                room = room,
                body = body,
                file=file_url,                       # vlozime url suboru do databaze
            )
        return HttpResponseRedirect(request.path_info) # refresh stranky, aby sa sprava zobrazila

    context = {'room': room,'messages': messages}
    return render(request, "chatterbox/room.html", context) '''
'''
@login_required # zakaze zobrazenie pre neprihlasenych user
def rooms(request):
    rooms = Room.objects.all()

    context = {'rooms': rooms}
    return render(request, 'chatterbox/rooms.html', context)
'''
'''
@login_required
def create_room(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        descr = request.POST.get('descr').strip()
        if len(name) > 0 and len(descr) > 0:
            room = Room.objects.create(
                host=request.user,
                name=name,
                description=descr

            )

            return redirect('room', pk=room.id)

    return render(request, 'chatterbox/create_room.html')
''' '''
@login_required
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if room.messages_count() == 0:  # pokud v místnosti není žádná zpráva
        room.delete()               # tak místnost smažeme

        return redirect('rooms')

    context = {'room': room, 'message_count': room.messages_count()}
    return render(request, 'chatterbox/delete_room.html', context)
''' '''
@login_required
def delete_room_yes(request, pk):
    room = Room.objects.get(id=pk)
    room.delete()
    return redirect('rooms')
''' '''
# formular
# implemantovane priamo v Django
# tu nemusime davat metod decorator, lebo sa pouziva v EditRoom a tam je to zadefinovane
class RoomEditForm(ModelForm):

    class Meta:
        model = Room
        fields = '__all__'

@method_decorator(login_required, name='dispatch') # uz nefunguje ked dame @login_required
class EditRoom(UpdateView):
    template_name = 'chatterbox/edit_room.html'
    model = Room
    form_class = RoomEditForm # prepoji ma z formularom hore
    success_url = reverse_lazy('home') # takto vyzera prikaz
'''
