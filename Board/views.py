from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, FormView

from .forms import SignupForm, CodeConfirmForm


def index(request):
    return render(request, 'default.html')


class SignUpView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        user = self.object
        url = reverse('board_code_confirmation', kwargs={'pk': user.pk})
        return url


class CodeConfirmView(FormView):
    form_class = CodeConfirmForm
    template_name = 'registration/confirmation_code.html'

