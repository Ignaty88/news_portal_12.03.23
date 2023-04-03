import django_filters
from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter, CharFilter, DateTimeFilter
from .models import *
from django.forms import DateInput
# from datetimewidget.widgets import DateTimeWidget


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class NewsFilter(FilterSet):
    author = ModelChoiceFilter(
        field_name='Author',
        queryset=Author.objects.all(),
        empty_label='любой',
    )
    post_title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок',
    )
    post_text = CharFilter(
        field_name='text',
        lookup_expr='icontains',
    )

    post_category = ModelMultipleChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Категория поста'
    )

    post_date = django_filters.DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label= 'Дата',
        widget=DateInput(
            format='%Y-%m-%dT',
            attrs={'type': 'datetime-local'},
        ),
    )
        # widget=DateInput(attrs={'tupe': 'date'},)





    # class Meta:
    #     # В Meta классе мы должны указать Django модель,
    #     # в которой будем фильтровать записи.
    #     model = Post
    #     # В fields мы описываем по каким полям модели
    #     # будет производиться фильтрация.
    #     fields = {
    #     # поиск по названию
    #         'dateCreation': [
    #         'gt',  # дата должна быть больше или равна указанной
    #        ],
    #     }
    #     filter_overrides = {
    #         models.DateField: {
    #             'filter_class': django_filters.DateFilter,
    #             'extra': lambda f: {
    #                 'widget': DateInput
    #             },
    #         }
    #     }