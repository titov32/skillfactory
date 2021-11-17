from django.urls import path
from .views import PostsList, PostDetail, PostsSearch, PostCreateView, PostsUpdate, PostsDelete  # импортируем наше представление
from django.views.decorators.cache import cache_page


urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', cache_page(10)(PostsList.as_view())),
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>', PostDetail.as_view(), name='post_detail' ),
    path('search/', PostsSearch.as_view()),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit', PostsUpdate.as_view()),
    path('<int:pk>/delete', PostsDelete.as_view()),

]