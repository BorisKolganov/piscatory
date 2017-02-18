from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from adverts.views import AddAdvertView, AdvertView, GetCategories, GetSubcategories, ShowAdvertsView, ChangeAdvertView, \
    DeleteAdvertView

#
urlpatterns = [
    url(r'^add/$', login_required(AddAdvertView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', AdvertView.as_view(), name='advert'),
    url(r'^(?P<pk>\d+)/edit/$', login_required(ChangeAdvertView.as_view()), name='edit'),
    url(r'^(?P<pk>\d+)/delete/$', login_required(DeleteAdvertView.as_view()), name='delete'),
    url(r'^get_categories/$', GetCategories.as_view(), name='categories'),
    url(r'^get_subcategories/(?P<pk>\d+)/$', GetSubcategories.as_view(), name='subcategories'),
    url(r'^all/$', ShowAdvertsView.as_view(), name='index'),
    url(r'^all/(?P<category_id>\d+)/$', ShowAdvertsView.as_view(), name='category'),
    url(r'^all/(?P<category_id>\d+)/(?P<subcategory_id>\d+)/$', ShowAdvertsView.as_view(), name='subcategory'),
]
