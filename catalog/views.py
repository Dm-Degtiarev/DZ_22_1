from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from catalog.models import Product, ProductVersion, Contacts, Blog, Category
from catalog.forms import *
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.forms.models import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.conf import settings

from catalog.services import get_cache_categories


#CBV
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/index.html'


class ContactsView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/contacts.html'
    extra_context = {
        'title': 'Контакты'
    }


class ProductListView(ListView):
    model = Product
    extra_context = {
        'title': 'Товары'
    }

class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.object.product_name

        if settings.CACHE_ENABLE:
            key = 'product_cache'
            product_cache = cache.get(key)
            if product_cache is None:
                product_cache = self.object.product_name
                cache.set(key, product_cache)
        else:
            product_cache = self.object.product_name

        context_data['product_cache'] = product_cache


        return context_data


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products_list')

    def form_valid(self, form):
        product = form.save()

        product.user = self.request.user
        product.product_author = self.request.user
        product.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form_with_formset.html'
    success_url = reverse_lazy('catalog:products_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        user = self.request.user
        if not user.has_perm('catalog.set_status_product'):
            # Проверка авторства продукта
            if self.object.product_author != user:
                return self.handle_no_permission()

        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if not self.request.user.has_perm('catalog.change_info_product'):
            form.fields.pop('product_info')
        if not self.request.user.has_perm('catalog.set_status_product'):
            form.fields.pop('product_status')
        if not self.request.user.has_perm('catalog.change_category_product'):
            form.fields.pop('product_category')

        return form

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        version_formset = inlineformset_factory(
            Product,
            ProductVersion,
            form=ProductVersionForm,
            extra=1,
            fields='__all__'
        )
        if self.request.method == 'POST':
            context_data['formset'] = version_formset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = version_formset(instance=self.object)
        return context_data


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products_list')


class CategoryListView(ListView):
    model = Category
    queryset = get_cache_categories()


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(blog_publicate_flg=True)

        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self):
        blog_slug = self.kwargs['blog_slug']
        obj = get_object_or_404(self.model, blog_slug=blog_slug)

        return obj


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = context_data['object']

        return  context_data


    def get(self, request, *args, **kwargs):
        """Увеличивает счетчик просмотров статьи"""
        self.object = self.get_object()
        self.object.blog_views_count +=1
        self.object.save()

        context = self.get_context_data(object=self.object)

        return self.render_to_response(context)


class BlogCreateView(CreateView):
    model = Blog
    fields = ('blog_name', 'blog_content', 'blog_image')
    success_url = reverse_lazy('catalog:blog')


class BlogUpdateView(UpdateView, BlogDetailView):
    model = Blog
    fields = ('blog_name', 'blog_content', 'blog_image')

    def get_success_url(self):
        blog = self.get_object()

        return reverse_lazy('catalog:blog_detail', kwargs={'blog_slug': blog.blog_slug})


class BlogDeleteView(DeleteView, BlogDetailView):
    model = Blog
    success_url = reverse_lazy('catalog:blog')



#FBV
# def index(request):
#     return render(request, 'catalog/index.html')


# def products(request):
#     products = Product.objects.all()
#     context = {
#         'products': products
#     }
#
#     return render(request, 'catalog/product_list.html', context)


# def product(request, pk):
#     product_item = Product.objects.get(pk=pk)
#     context = {
#         'object': product_item
#     }
#
#     return render(request, 'catalog/product_detail.html', context)

