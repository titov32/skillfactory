from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=128)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    # собираем все связанные посты с автором, применяем к нему метод aggregate и высчитваем сумму по полю 'rating'
    def update_rating(self):
        rating_post = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat = rating_post.get('postRating')

        comment_rating = self.user.comment_set.all().aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat = comment_rating.get('commentRating')

class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)


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
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    timeCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    # связь многие ко многим, один пост может иметь много категорий и
    # одна категория может иметь много постов
    postCategory = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        text = self.text[:123] + '...'
        return text


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
