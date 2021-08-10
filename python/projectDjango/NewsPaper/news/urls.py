from django.urls import path
from .views import PostsList, PostDetail, PostsSearch, PostCreateView  # импортируем наше представление

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', PostsList.as_view()),
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>', PostDetail.as_view() ),
    path('search/', PostsSearch.as_view()),
    path('create/', PostCreateView.as_view(), name='post_create'),

]