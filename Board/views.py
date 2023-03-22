from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic.detail import SingleObjectMixin, DetailView, BaseDetailView, SingleObjectTemplateResponseMixin
from django.views.generic.edit import CreateView, FormView, UpdateView, BaseUpdateView, DeleteView, FormMixin, \
    ProcessFormView, ModelFormMixin

from .forms import SignupForm, CodeConfirmForm
from .models import BoardUserActivateCode


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

class ttt(UpdateView):
    pass

# class CodeConfirmView(SingleObjectMixin, DetailView):
# class CodeConfirmView(SingleObjectMixin, UpdateView):
# class CodeConfirmView(SingleObjectMixin, BaseUpdateView):
# class CodeConfirmView(SingleObjectTemplateResponseMixin, FormMixin, BaseDetailView):
# class CodeConfirmView(SingleObjectTemplateResponseMixin, FormMixin, ProcessFormView):
class CodeConfirmView(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    model = User
    form_class = CodeConfirmForm
    template_name = 'registration/confirmation_code.html'

    def post(self, request, *args, **kwargs):
        pass