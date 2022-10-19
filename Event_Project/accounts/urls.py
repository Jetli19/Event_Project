from django.urls import path

import event
from .views import SignUpView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"), # - original
    # path('signup/', event.views.signup, name='signup'), # - alternative, (2022-10-15-6 - not working properly)
]
