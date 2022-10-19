"""Event_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import event.views
import profiles.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', event.views.home, name='home'),
    # path('login/', event.views.login, name='login'),
    path('signup/', event.views.signup, name='signup'),
    path('search/', event.views.search, name='search'),

    path('event/<str:pk>/', event.views.event, name="event"),
    path('events/', event.views.events, name='events'),

    #PROFILES APLIKACE
    path('users/', profiles.views.profiles_list, name='profiles'),
    path('user/<pk>/', profiles.views.user_profile, name='profile'),
    path('edituser/', profiles.views.edit_profile, name='editprofile'),
    path('createprofile/', profiles.views.create_profile, name='createprofile'),

    #create room
    path('create_event/', event.views.create_event, name="create_event"),

    path('delete_event/<str:pk>/', event.views.delete_event, name='delete_event'),
    path('delete_event_yes/<pk>/', event.views.delete_event_yes, name="delete_event_yes"),
    path('edit_event/<pk>/', event.views.EditEvent.as_view(), name='edit_event'),

    # accounts aplikace
    path("accounts/", include("accounts.urls")),  # vygeneruje signup
    path("accounts/", include("django.contrib.auth.urls")),  # vsetky ostatne authorizacne urls
    # path('accounts/', profiles.views.SignUpView.len_username, name='len_username'),
    # path('accounts/', profiles.views.SignUpView.form_valid, name='form_valid'),

    # join event
    path('join_event/<pk1>/<pk2>/', event.views.JoinEvent.join_event, name='join_event'),

    # unjoin_event
    path('unjoin_event/<pk1>/<pk2>/', event.views.JoinEvent.unjoin_event, name='unjoin_event'),

    path("__reload__/", include("django_browser_reload.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # add static
