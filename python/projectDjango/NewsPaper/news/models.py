from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache

# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}'

    # собираем все связанные посты с автором, применяем к нему метод aggregate и высчитваем сумму по полю 'rating'
    def update_rating(self):
        rating_post = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat = rating_post.get('postRating')
        if not pRat:
            pRat = 0

        comment_rating = self.user.comment_set.all().aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat = comment_rating.get('commentRating')
        if not cRat:
            cRat = 0

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name_category}'


class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    MATERIAL_CHOICES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]
    material = models.CharField(
        max_length=7,
        choices=MATERIAL_CHOICES,
        default='article')
    created_by = models.ForeignKey(Author, on_delete=models.CASCADE)
    timeCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    # связь многие ко многим, один пост может иметь много категорий и
    # одна категория может иметь много постов
    postCategory = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return f'{self.title}:{self.text[:20]}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        text = self.text[:123] + '...'
        return text

    def get_absolute_url(self):  # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с новостью
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.post.title} : {self.category.category[:20]}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f' {self.user.username},  {self.text[:20]}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
