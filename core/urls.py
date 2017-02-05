from django.conf.urls import url

from core.views import IndexView, AdvertView, RegistrationView, LoginView, LogoutView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'advert/$', AdvertView.as_view(), name='advert'),
    url(r'registration/$', RegistrationView.as_view(), name='registration'),
    url(r'login/$', LoginView.as_view(), name='login'),
    url(r'logout/$', LogoutView.as_view(), name='logout')
]
