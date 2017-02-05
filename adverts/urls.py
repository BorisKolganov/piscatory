from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from adverts.views import AddAdvertView, AdvertView, GetCategories, GetSubcategories, ShowAdvertsView

#
urlpatterns = [
    url(r'^add/$', login_required(AddAdvertView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', AdvertView.as_view(), name='advert'),
    url(r'^get_categories/$', GetCategories.as_view(), name='categories'),
    url(r'^get_subcategories/(?P<pk>\d+)/$', GetSubcategories.as_view(), name='subcategories'),
    url(r'^all/(?P<pk>\d+)/$', ShowAdvertsView.as_view(), name='all')
]
