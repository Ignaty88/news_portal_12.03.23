from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .filters import NewsFilter
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'newsapp/news.html'
    context_object_name = 'news'
    paginate_by = 10


    # def get_queryset(self):
    #     # Получаем обычный запрос
    #     queryset = super().get_queryset()
    #     # Используем наш класс фильтрации.
    #     # self.request.GET содержит объект QueryDict, который мы рассматривали
    #     # в этом юните ранее.
    #     # Сохраняем нашу фильтрацию в объекте класса,
    #     # чтобы потом добавить в контекст и использовать в шаблоне.
    #     self.filterset = NewsFilter (self.request.GET, queryset)
    #     # Возвращаем из функции отфильтрованный список товаров
    #     return self.filterset.qs
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Добавляем в контекст объект фильтрации.
    #     context['filterset'] = self.filterset
    #     return context
#
#
#
#
class AuthorList(ListView):
    model = Author
    context_object_name = 'Authors'
    template_name = 'newsapp/author_list.html'
#
class DetailPost(DetailView):
    model = Post
    template_name = 'newsapp/detail.html'
    context_object_name = 'new'

    # def get_object(self):
    #     return get_object_or_404(Post, id__iexact=self.kwargs['id'])



# def index(reqest):
#     news = Post.objects.all().order_by('-dateCreation')
#     return render(reqest, 'news.html', context={'news': news})
#
#
# def detail(reqest, id):
#     new = Post.objects.get(id__iexact=id)
#     return render(reqest, 'detail.html', context={'new': new})

class SearchList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'newsapp/search.html'
    context_object_name = 'news1'
    paginate_by = 10


    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('newsapp.add_post',)
    raise_exception = True
    model = Post
    fields = ['Author', 'title', 'text']
    template_name = 'newsapp/post_form.html'
    success_url = reverse_lazy('news')

    def form_valid(self, form):
        form.instance.categoryType = 'NW' # присваиваем значение «новость» при создании новости
        return super().form_valid(form)

class NewsUpdateView(PermissionRequiredMixin,UpdateView):
    permission_required = ('newsapp.change_post',)
    raise_exception = True
    model = Post
    fields = ['title', 'text']
    template_name = 'newsapp/post_form.html'
    success_url = reverse_lazy('news')

class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('newsapp.delete_post',)
    model = Post
    template_name = 'newsapp/post_confirm_delete.html'
    success_url = reverse_lazy('news')

class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('newsapp.add_post',)
    model = Post
    fields = ['Author', 'title', 'text', 'postCategory']
    template_name = 'newsapp/post_form.html'
    success_url = reverse_lazy('news')

    def form_valid(self, form):
        form.instance.categoryType = 'AR' # присваиваем значение «статья» при создании статьи
        return super().form_valid(form)

class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsapp.change_post',)
    model = Post
    fields = ['title', 'text', 'postCategory']
    template_name = 'newsapp/post_form.html'
    success_url = reverse_lazy('news')

class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('newsapp.delete_post',)
    model = Post
    template_name = 'newsapp/post_confirm_delete.html'
    success_url = reverse_lazy('news')
