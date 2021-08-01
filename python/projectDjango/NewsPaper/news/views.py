from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Post


class PostsList(ListView):
    # указываем модель, объекты которой мы будем выводить
    model = Post
    # указываем имя шаблона, в котором будет лежать html, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    template_name = 'news/news.html'
    # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через html-шаблон
    context_object_name = 'posts'

class PostDetail(DetailView):

    # указываем модель, объекты которой мы будем выводить
    model = Post
    # указываем имя шаблона, в котором будет лежать html, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    template_name = 'news/new.html'
    # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через html-шаблон
    context_object_name = 'post'