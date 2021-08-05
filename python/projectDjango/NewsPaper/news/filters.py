from django_filters import FilterSet  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post


# создаём фильтр
class PostFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля по которым будет фильтроваться (т.е. подбираться) информация о товарах
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'], # мы хотим чтобы нам выводило имя хотя бы отдалённо похожее на то что запросил пользователь
            'timeCreation': ['gt'], # количество товаров должно быть больше или равно тому, что указал пользователь
            'text': ['icontains'], # цена должна быть меньше или равна тому, что указал пользователь
        }