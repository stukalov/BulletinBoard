import datetime

from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, SingleObjectTemplateResponseMixin
from django.views.generic.edit import CreateView, FormMixin

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


class CodeConfirmView(SingleObjectTemplateResponseMixin, FormMixin, SingleObjectMixin, View):
    model = User
    form_class = CodeConfirmForm
    template_name = 'registration/confirmation_code.html'

    def __init__(self):
        super(CodeConfirmView, self).__init__()
        self.object = None
        self.code_object = None

    def get_code_object(self):
        self.object = self.get_object()
        query = BoardUserActivateCode.objects.filter(
            user=self.object.pk,
            valid_till__gte=datetime.datetime.now()
        )
        self.code_object = query.first()
        return self.code_object

    def get(self, request, *args, **kwargs):
        if self.get_code_object() is None:
            return HttpResponseNotFound(render(request, '404.html'))

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if self.get_code_object() is None:
            return HttpResponseNotFound(render(request, '404.html'))

        form = self.get_form()
        code = request.POST.get('code', '')
        if code.strip() != self.code_object.code:
            form.add_error('code', 'Неправильный код подтверждения')

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object.is_active = True
        self.object.save()
        self.code_object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('login')
