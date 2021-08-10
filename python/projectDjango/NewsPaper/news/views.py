from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post
from .filters import PostFilter # импортируем недавно написанный фильтр
from .forms import PostForm # импортируем нашу форму


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
    form_class = PostForm

    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)

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


class PostCreateView(CreateView):
    model = Post
    template_name = 'news/create_news.html'
    form_class = PostForm
    success_url = '/news/'


