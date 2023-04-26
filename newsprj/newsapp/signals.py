from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from .models import *



#
#
# @receiver(post_save, sender=Post)
# def send_notification(sender, instance, created, **kwargs):
#     if created:
#         for subscriber in Subscriber.objects.filter(category=instance.category):
#             subject = f'Появилась новость  {instance.category.name} category'
#             article_url = reverse('post_detail', args=[instance.pk])
#             message_html = render_to_string('newsapp/new_article_notification.html',
#                                             {'post_title': instance.title, 'post_url': article_url})
#             message = strip_tags(message_html)
#             send_mail(subject, message, 'from@example.com', [subscriber.user.email], html_message=message_html)

def post_save(preview, pk, title, subscribers ):
    html_context = render_to_string(
        'post_created.html',
        {
            "text": preview,
            'link': f'{settings.SITE_URL}newsapp/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()






@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs ):
    if kwargs ['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers:list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        post_save(instance.preview(), instance.pk, instance.title, subscribers)
