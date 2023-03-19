from django.shortcuts import render
#from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import *


# Create your views here.

# class PostList(ListView):
#     model = Post
#     ordering = '-dateCreation'
#     template_name = 'newsapp/news.html'
#     context_object_name = 'new'
#
#
#
#
class AuthorList(ListView):
    model = Author
    context_object_name = 'Authors'
    template_name = 'newsapp/author_list.html'
#
# class Post(DetailView):
#     model = Post
#     ordering = '-dateCreation'
#     template_name = 'newsapp/detail.html'
#     context_object_name = 'new'



def index(reqest):
    news = Post.objects.all().order_by('-dateCreation')
    return render(reqest, 'news.html', context={'news': news})


def detail(reqest, id):
    new = Post.objects.get(id__iexact=id)
    return render(reqest, 'detail.html', context={'new': new})