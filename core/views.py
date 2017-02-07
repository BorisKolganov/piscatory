from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from core.forms import RegistrationForm, LoginForm
from django.contrib.auth import logout, login


class IndexView(RedirectView):
    url = reverse_lazy('adverts:index')


class AdvertView(TemplateView):
    template_name = 'adverts/show.html'


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('core:index')


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        user = form.cleaned_data.get('user')
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')
        return reverse_lazy('core:index')


class LogoutView(View):
    logout_redirect = reverse_lazy('core:index')

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(self.logout_redirect)
