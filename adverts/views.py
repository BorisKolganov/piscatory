from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic import ListView

from adverts.models import Advert, Category, SubCategory
from adverts.forms import AdvertForm


class AddAdvertView(CreateView):
    template_name = 'adverts/advert_create.html'
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
    pass


class GetCategories(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {c.name: c.id for c in categories}
        return JsonResponse(context)


class GetSubcategories(View):
    def get(self, request, pk, *args, **kwargs):
        subcategories = SubCategory.objects.filter(category__id=pk)
        context = {c.id: c.name for c in subcategories}
        return JsonResponse(context)


class ShowAdvertsView(ListView):
    template_name = 'index.html'
    context_object_name = 'adverts'
    paginate_by = 6

    def get_queryset(self):
        subcategory_id = self.kwargs.get('pk')
        if subcategory_id:
            self.subcategory = get_object_or_404(SubCategory, pk=self.kwargs.get('pk'))
            return Advert.objects.get_showable().filter(type__id=subcategory_id).order_by('-id')
        else:
            return Advert.objects.get_showable().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(ShowAdvertsView, self).get_context_data(**kwargs)
        context['categories'] = {c.id: c.name for c in Category.objects.all()}
        context['best_adverts'] = Advert.objects.get_best_adverts()
        if hasattr(self, 'subcategory') and self.subcategory:
            context['selected_category'] = self.subcategory.category.id
            context['selected_subcategory'] = self.subcategory.id
        return context
