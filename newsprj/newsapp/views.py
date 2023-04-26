from django.shortcuts import render, get_object_or_404,redirect
#from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import *
from .filters import NewsFilter
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.utils.decorators import method_decorator
from django.contrib import messages

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



class CategoryListView(ListView):
    model = Post
    template_name = 'newsapp/category_list.html'
    context_object_name = 'category_news_list'


    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.category).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        # context['is_subscriber'] = self.request.user in self.category.subscribers.all()
        context['category'] = self.category
        return context



@login_required
def subscribe(reqest, pk):

    user = reqest.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = ' Вы успешно подписались на рассылку новостей в категории'
    return render(reqest, 'newsapp/subscribe.html', {'category': category, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = get_object_or_404(Category, id=pk)

    if user in category.subscribers.all():
        category.subscribers.remove(user)
        message = 'Вы успешно отписались от рассылки новостей в категории '

        return render(request, 'newsapp/unsubscribe.html', {'category': category, 'message': message})




# def subscriptions(request):
#     if request.method == 'POST':
#         category_id = request.POST.get('category_id')
#         category = Category.objects.get(id=category_id)
#         action = request.POST.get('action')
#
#         if action == 'subscribe':
#             Subscription.objects.create(user=request.user, category=category)
#         elif action == 'unsubscribe':
#             Subscription.objects.filter(
#                 user=request.user,
#                 category=category,
#             ).delete()
#
#     categories_with_subscriptions = Category.objects.annotate(
#         user_subscribed=Exists(
#             Subscription.objects.filter(
#                 user=request.user,
#                 category=OuterRef('pk'),
#             )
#         )
#     ).order_by('postcategory')
#     return render(
#         request,
#         'subscriptions.html',
#         {'categories': categories_with_subscriptions},
#     )









# class SubscriptionView(View):
#     template_name = 'newsapp/subscriptions.html'
#
#     @method_decorator(login_required(login_url=reverse_lazy('login')))
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def get(self, request):
#         categories = Category.objects.all()
#         subscriptions = Subscriber.objects.filter(user=request.user)
#         return render(request, self.template_name, {'categories': categories, 'subscriptions': subscriptions})
#
#     def post(self, request):
#         selected_categories = request.POST.getlist('category')
#         current_subscriptions = Subscriber.objects.filter(user=request.user)
#         for sub in current_subscriptions:
#             if sub.category.name not in selected_categories:
#                 sub.delete()
#         for category_name in selected_categories:
#             category = Category.objects.get(name=category_name)
#             try:
#                 Subscriber.objects.get(user=request.user, category=category)
#             except Subscriber.DoesNotExist:
#                 Subscriber(user=request.user, category=category).save()
#         return redirect('subscriptions')