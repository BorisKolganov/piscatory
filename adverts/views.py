# coding=utf-8
from django.http import Http404
from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView

from adverts.models import Advert, Category, SubCategory
from adverts.forms import AdvertForm


class AddAdvertView(CreateView):
    template_name = 'adverts/create.html'
    form_class = AdvertForm

    def get_context_data(self, **kwargs):
        context = super(AddAdvertView, self).get_context_data(**kwargs)
        context['categories'] = {c.id: c.name for c in Category.objects.all()}
        return context

    def get_success_url(self):
        return reverse_lazy('adverts:advert', args=[self.object.id])

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        type = form.cleaned_data.get('type')
        if type:
            context['selected_category'] = type.category.id
        return self.render_to_response(context)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        return super(AddAdvertView, self).form_valid(form)


class AdvertView(DetailView):
    template_name = 'adverts/show.html'
    model = Advert
    context_object_name = 'advert'


class ChangeAdvertView(UpdateView):
    model = Advert
    template_name = 'adverts/edit.html'
    context_object_name = 'advert'
    form_class = AdvertForm

    def get_success_url(self):
        return reverse_lazy('adverts:advert', args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super(ChangeAdvertView, self).get_context_data(**kwargs)
        context['categories'] = {c.id: c.name for c in Category.objects.all()}
        return context

    def get_object(self, queryset=None):
        advert = get_object_or_404(self.model, id=self.kwargs.get('pk'))
        if self.request.user != advert.owner:
            raise Http404()
        return advert

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_moderated = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class DeleteAdvertView(DeleteView):
    model = Advert
    http_method_names = ['post']

    def get_object(self, queryset=None):
        advert = get_object_or_404(self.model, id=self.kwargs.get('pk'))
        if self.request.user != advert.owner:
            raise Http404()
        return advert

    def get_success_url(self):
        return reverse_lazy('core:index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return JsonResponse({'status': '302', 'redirect_url': success_url})


class GetCategories(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {c.name: c.id for c in categories}
        return JsonResponse(context)


class GetSubcategories(View):
    def get(self, request, pk, *args, **kwargs):
        subcategories = SubCategory.objects.filter(category__id=pk)
        context = {0: u'Все подкатегории'}
        context.update({c.id: c.name for c in subcategories})
        return JsonResponse(context)


class ShowAdvertsView(ListView):
    template_name = 'index.html'
    context_object_name = 'adverts'
    paginate_by = 20

    def get_queryset(self):
        subcategory_id = self.kwargs.get('subcategory_id')
        category_id = self.kwargs.get("category_id")
        if subcategory_id:
            subcategory = get_object_or_404(SubCategory, pk=subcategory_id)
            return Advert.objects.get_showable().filter(type=subcategory).order_by('-id')
        elif category_id:
            category = get_object_or_404(Category, pk=category_id)
            return Advert.objects.get_showable().filter(type__category=category).order_by('-id')
        else:
            return Advert.objects.get_showable().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(ShowAdvertsView, self).get_context_data(**kwargs)
        context['categories'] = {c.id: c.name for c in Category.objects.all()}
        context['best_adverts'] = Advert.objects.get_best_adverts()
        if self.kwargs.get("category_id"):
            context['selected_category'] = self.kwargs.get("category_id")
        if self.kwargs.get("subcategory_id"):
            context['selected_subcategory'] = self.kwargs.get("subcategory_id")
        return context
