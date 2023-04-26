from django.apps import AppConfig




class NewsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsapp'

    def ready(self):
        import newsapp.signals
#         from apscheduler.schedulers.background import BackgroundScheduler
#         from django_apscheduler.jobstores import DjangoJobStore
#         from django_apscheduler.models import DjangoJobExecution
#         from django.core.mail import get_connection, EmailMultiAlternatives
#         from django.template.loader import render_to_string
#         from django.utils import timezone
#         from .models import *
#
#         scheduler = BackgroundScheduler()
#         scheduler.add_jobstore(DjangoJobStore(), 'default')
#
#         def send_articles_to_subscribers():
#             subscribers = Subscriber.objects.all()
#             for subscriber in subscribers:
#                 articles = Post.objects.filter(category=subscriber.category,
#                                                   created_at__gt=subscriber.last_email_sent)
#                 if articles.exists():
#                     subject = f'New articles in {subscriber.category.name} category'
#                     message_html = render_to_string('newsapp/new_articles_notification.html', {'articles': articles})
#                     message = render_to_string('newsapp/new_articles_notification.txt', {'articles': articles})
#                     connection = get_connection(backend='django.core.mail.backends.console.EmailBackend')
#                     msg = EmailMultiAlternatives(subject, message, 'from@example.com', [subscriber.user.email],
#                                                  connection=connection)
#                     msg.attach_alternative(message_html, "text/html")
#                     msg.send()
#                     subscriber.last_email_sent = timezone.now()
#                     subscriber.save()
#
#         scheduler.add_job(send_articles_to_subscribers, 'interval', weeks=1, day_of_week='fri', hour=18,
#                           timezone='Europe/Moscow', name='send_articles_to_subscribers')
#
#         try:
#             scheduler.start()
#         except Exception as e:
#             print(e)
#         finally:
#             print('Scheduler started')
        # выполнение модуля -> регистрация сигналов