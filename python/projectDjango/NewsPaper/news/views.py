from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post, Author, User, Comment
from .filters import PostFilter # импортируем недавно написанный фильтр
from .forms import PostForm # импортируем нашу форму
from django.contrib.auth.mixins import PermissionRequiredMixin
from appointment.utils import PostCountException
from django.shortcuts import redirect
import datetime
from django.core.cache import cache

class PostDetail(DetailView):
    # указываем модель, объекты которой мы будем выводить
    model = Post
    # указываем имя шаблона, в котором будет лежать html, в котором будут все инструкции о том, как именно
    # пользователю должны вывестись наши объекты
    template_name = 'news/new.html'
    # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов
    # через html-шаблон
    context_object_name = 'post'


    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует также. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object()
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)
        return context


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
    paginate_by = 4
    form_class = PostForm


    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        context['form'] = PostForm()
        context['page_news'] = 'active'
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)


class PostsSearch(ListView):
    # указываем модель, объекты которой мы будем выводить
    model = Post
    # указываем имя шаблона, в котором будет лежать html, в котором будут все инструкции о том, как именно
    # пользователю должны вывестись наши объекты
    template_name = 'news/search.html'
    # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов
    # через html-шаблон
    context_object_name = 'posts'
    ordering = ['-timeCreation', 'created_by']
    paginate_by = 3

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_search'] = 'active'
        return {
            **context,
            "filter": self.get_filter(),
        }


class PostCreateView(PermissionRequiredMixin, CreateView):

    permission_required = ('news.add_post')
    model = Post
    template_name = 'news/create_news.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        """
        определяем контекст для последующего ограничения ввода в шаблонах
        """
        context = super().get_context_data(**kwargs)
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        user = self.request.user
        user = User.objects.get(username=user)
        author = Author.objects.get(user=user)
        count_posts = Post.objects.filter(created_by=author, timeCreation__range=(today_min, today_max)).count()
        context['count_post'] = count_posts
        context['page_editor'] = 'active'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        user = self.request.user
        user = User.objects.get(username=user)
        author = Author.objects.get(user=user)
        obj.created_by = author
        return super(PostCreateView, self).form_valid(form)


class PostsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    template_name = 'news/create_news.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_editor'] = 'active'
        return context


class PostsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    template_name = 'news/delete_news.html'
    queryset = Post.objects.all()
    success_url = '/news/'




