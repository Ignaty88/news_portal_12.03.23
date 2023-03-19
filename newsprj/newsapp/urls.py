from django.urls import path, include
from .views import *

urlpatterns = [
    path('news/', index),
    path('author/', AuthorList.as_view()),
    path('news/<int:id>', detail, name='detail')

]