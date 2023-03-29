import datetime

from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, SingleObjectTemplateResponseMixin, DetailView
from django.views.generic.edit import CreateView, FormMixin, UpdateView, DeleteView

from .filters import ReplayFilter
from .forms import SignupForm, CodeConfirmForm, BulletinForm, ReplayForm
from .models import BoardUserActivateCode, Bulletin, Replay


def index_page(request):
    return HttpResponseRedirect(reverse('bulletin_list'))


class SignUpView(AccessMixin, CreateView):
    model = User
    form_class = SignupForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        user = self.object
        url = reverse('board_code_confirmation', kwargs={'pk': user.pk})
        return url

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CodeConfirmView(AccessMixin, SingleObjectTemplateResponseMixin, FormMixin, SingleObjectMixin, View):
    model = User
    form_class = CodeConfirmForm
    template_name = 'registration/confirmation_code.html'

    def __init__(self):
        super(CodeConfirmView, self).__init__()
        self.object = None
        self.code_object = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

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
        if not self.code_object.check_code(request.POST.get('code', '')):
            form.add_error('code', 'Неправильный код подтверждения')

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('login')


class BulletinList(ListView):
    model = Bulletin
    ordering = '-created'
    template_name = 'bulletin_list.html'
    context_object_name = 'bulletins'
    paginate_by = 10


class BulletinMyList(ListView):
    model = Bulletin
    ordering = '-created'
    template_name = 'bulletin_list.html'
    context_object_name = 'bulletins'
    paginate_by = 10

    def __init__(self):
        super().__init__()
        self.request = None

    def get(self, request, *args, **kwargs):
        self.request = request
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        query = super().get_queryset()
        return query.filter(author=self.request.user)


class BulletinDetail(DetailView):
    model = Bulletin
    template_name = 'bulletin_detail.html'
    context_object_name = 'bulletin'


class BulletinCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = BulletinForm
    model = Bulletin
    template_name = 'bulletin_edit.html'

    def __init__(self):
        super().__init__()
        self.object = None

    def form_valid(self, form):
        user = self.request.user
        self.object = form.save(commit=False)
        self.object.author = user
        self.object.save()
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())


class BulletinUpdate(AccessMixin, UpdateView):
    raise_exception = True
    form_class = BulletinForm
    model = Bulletin
    template_name = 'bulletin_edit.html'

    def dispatch(self, request, *args, **kwargs):
        bulletin = self.get_object()
        if not bulletin.can_edit(request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class BulletinDelete(AccessMixin, DeleteView):
    raise_exception = True
    model = Bulletin
    template_name = 'bulletin_delete.html'
    success_url = reverse_lazy('bulletin_list')

    def dispatch(self, request, *args, **kwargs):
        bulletin = self.get_object()
        if not bulletin.can_edit(request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ReplayCreate(AccessMixin, CreateView):
    raise_exception = True
    form_class = ReplayForm
    model = Replay
    template_name = 'replay_create.html'

    def __init__(self):
        super().__init__()
        self.bulletin = None
        self.object = None

    def form_valid(self, form):
        user = self.request.user
        self.object = form.save(commit=False)
        self.object.user = user
        self.object.bulletin = self.bulletin
        self.object.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse('replay_my_detail', args=(self.object.pk,)))

    def get_bulletin(self, **kwargs):
        bulletin_id = kwargs.get('bulletin')
        self.bulletin = get_object_or_404(Bulletin, pk=bulletin_id)

    def dispatch(self, request, *args, **kwargs):
        self.get_bulletin(**kwargs)
        if not self.bulletin.can_replay(request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bulletin'] = self.bulletin
        return context


class ReplayMyDetail(DetailView):
    model = Replay
    template_name = 'replay_my_detail.html'
    context_object_name = 'replay'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.request = None

    def get(self, request, *args, **kwargs):
        self.request = request
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Replay.objects.filter(user=self.request.user)
        return queryset.select_related('bulletin')


class ReplayMyList(ListView):
    ordering = '-created'
    template_name = 'replay_my_list.html'
    context_object_name = 'replays'
    paginate_by = 10

    def __init__(self):
        super().__init__()
        self.request = None

    def get(self, request, *args, **kwargs):
        self.request = request
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Replay.objects.filter(user=self.request.user)
        return queryset.select_related('bulletin')


class ReplayDetail(DetailView):
    model = Replay
    template_name = 'replay_detail.html'
    context_object_name = 'replay'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.request = None

    def get(self, request, *args, **kwargs):
        self.request = request
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Replay.objects.filter(bulletin__author=self.request.user)
        return queryset.select_related('bulletin')


class ReplayList(ListView):
    model = Replay
    ordering = 'accepted -created'
    template_name = 'replay_list.html'
    context_object_name = 'replays'
    paginate_by = 10

    def __init__(self):
        super().__init__()
        self.filter_set = None
        self.request = None

    def get(self, request, *args, **kwargs):
        self.request = request
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Replay.objects.filter(bulletin__author=self.request.user)
        self.filter_set = ReplayFilter(self.request.GET, queryset, request=self.request)
        return self.filter_set.qs.select_related('bulletin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_set'] = self.filter_set
        return context


class ReplayAccept(View):

    def get(self, request, *args, **kwargs):
        replay = get_object_or_404(Replay, pk=kwargs["pk"])
        if replay.do_accept(request.user):
            return HttpResponseRedirect(reverse('replay_detail', args=(kwargs["pk"],)))
        else:
            raise Http404()


class ReplayDecline(View):

    def get(self, request, *args, **kwargs):
        replay = get_object_or_404(Replay, pk=kwargs["pk"])
        if replay.do_decline(request.user):
            return HttpResponseRedirect(reverse('replay_list'))
        else:
            raise Http404()
