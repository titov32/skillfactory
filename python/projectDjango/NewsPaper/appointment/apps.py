from django.apps import AppConfig


class AppointmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointment'

    # нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками
    def ready(self):
        import appointment.signals

""" Ниже код может быть раскометирован для того чтобы отрпалвялть сообщения через task.py
        from .tasks import send_mail
        from .scheduler import appointment_scheduler
        print('started job from scheduler')

        appointment_scheduler.add_job(
            id = 'mail send',
            func = send_mail,
            trigger= 'interval',
            seconds = 30,
        )
        appointment_scheduler.start()
"""