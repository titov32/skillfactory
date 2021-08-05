from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Post
from .filters import PostFilter # импортируем недавно написанный фильтр


class PostsList(ListView):
    # указываем модель, объекты которой мы будем выводить
    model = Post
    # указываем имя шаблона, в котором будет лежать html, в котором будут все инструкции о том, как именно
    # пользователю должны вывестись наши объекты
    template_name = 'news/news.html'
    # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов
    # через html-шаблон
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-timeCreation')
    paginate_by = 2

    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context

class PostDetail(DetailView):
    # указываем модель, объекты которой мы будем выводить
    model = Post
    # указываем имя шаблона, в котором будет лежать html, в котором будут все инструкции о том, как именно
    # пользователю должны вывестись наши объекты
    template_name = 'news/new.html'
    # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов
    # через html-шаблон
    context_object_name = 'post'


class PostsSearch(ListView):
    # указываем модель, объекты которой мы будем выводить
    model = Post
    # указываем имя шаблона, в котором будет лежать html, в котором будут все инструкции о том, как именно
    # пользователю должны вывестись наши объекты
    template_name = 'news/search.html'
    # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов
    # через html-шаблон
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-timeCreation')
    paginate_by = 2

    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context
