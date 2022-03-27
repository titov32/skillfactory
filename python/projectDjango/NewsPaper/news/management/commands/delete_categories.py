from django.core.management.base import BaseCommand, CommandError
from news.models import Category, Post


class Command(BaseCommand):

    help = 'Удаление новостей категорий'

    def handle(self, *args, **options):
        categories = Category.objects.all()
        self.stdout.readable()
        self.stdout.write(f'Доступные категории, напишите которую собираетесь удалить')
        for category in categories:
            self.stdout.write(category.name_category)
        count_posts = Post.objects.all().count()
        self.stdout.write(f'Quantity posts = {count_posts}')
        answer = input().encode().decode('utf-8', 'ignore')
        for category in categories:
            if category.name_category == answer:
                self.stdout.write(self.style.WARNING(f'Категория "{category.name_category}" будет удалена '))
                id_category = category.pk
                try:
                    Post.objects.filter(postCategory = id_category).delete()
                except Exception as E:
                    self.stdout.write(self.style.ERROR(f'Проблема удаления {E}'))

        count_posts = Post.objects.all().count()
        self.stdout.write(f'Quantity posts = {count_posts}')