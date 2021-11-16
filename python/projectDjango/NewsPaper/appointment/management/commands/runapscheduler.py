import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
import datetime
from news.models import Post, Category
from appointment.models import Subscriber
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives



logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    print('send messages from management')
    list_email = []
    # Получаем все доступные категории
    for category in Category.objects.all():
        today = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        last_week = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=7), datetime.time.max)
        #получаем посты за последнюю неделю с данной категорией
        posts_category = Post.objects.filter(postCategory=category, timeCreation__range=(last_week, today))
        list1 = Subscriber.objects.filter(sub_category=category)
        for mail in list1:
            list_email.append(mail.client_email)
        recipient_list = list(set(list_email))

        html_content = render_to_string(
            'appointment/weekly_send_posts.html',
            {
                'posts_category': posts_category
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Новое за неделю',
            body='This is an important message.',  # это то же, что и message
            from_email='email.infomail@yandex.ru',
            to=recipient_list,  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем



# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day="*/7"),
            # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")