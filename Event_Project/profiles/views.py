from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.forms import ModelForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from profiles.models import Profile


@login_required
def profiles_list(request):
    # profiles = Profile.objects.all()
    allusers = User.objects.all()

    context = {'users': allusers}
    return render(request, 'profiles/users.html', context)


@login_required
def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    # user = profile.use

    context = {'profile': profile}  # 'user': user,
    return render(request, 'profiles/user.html', context)


# class EditProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('about_me', 'photo')  # TODO editovatelne name...
#
#
# class EditProfile(UpdateView):
#     template_name = 'profiles/edituser.html'
#     model = Profile
#     form_class = EditProfileForm
#     success_url = reverse_lazy('profiles')


# class CreateProfile(CreateView):
# template_name = 'profiles/createprofile.html'
# success_url = reverse_lazy('profiles')

@login_required
def create_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        email = request.POST.get('email').strip()
        aboutme = request.POST.get('aboutme').strip()
        file_url = ""
        if request.FILES.get('upload'):  # pokial sme poslali subor
            upload = request.FILES['upload']  # z requestu si vytiahnem subor
            file_storage = FileSystemStorage()  # praca so suborovym systemom
            file = file_storage.save(upload.name, upload)  # ulozime subor na disk
            file_url = file_storage.url(file)

        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        profile = Profile.objects.create(
            user=user,
            about_me=aboutme,
            photo=file_url,
        )

        return redirect('profiles')
    return render(request, 'profiles/createprofile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        email = request.POST.get('email').strip()
        aboutme = request.POST.get('aboutme').strip()
        user = User.objects.get(id=request.user.id)
        file_url = user.userprofile.photo
        if request.FILES.get('upload'):  # pokial sme poslali subor
            upload = request.FILES['upload']  # z requestu si vytiahnem subor
            file_storage = FileSystemStorage()  # praca so suborovym systemom
            file = file_storage.save(upload.name, upload)  # ulozime subor na disk
            file_url = file_storage.url(file)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        user.userprofile.about_me = aboutme
        user.userprofile.photo = file_url
        user.userprofile.save()
        profile = user.userprofile

        return redirect('profiles')
    user = User.objects.get(id=request.user.id)
    profile = user.userprofile
    context = {"profile": profile}
    return render(request, 'profiles/edituser.html', context)
