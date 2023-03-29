from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter, CharFilter, ChoiceFilter
from .models import Category, Bulletin


class ReplayFilter(FilterSet):
    ACCEPTED_CHOICES = (
        ('1', 'Принятые'),
        ('0', 'Не отвеченные'),
    )

    accepted = ChoiceFilter(
        field_name='accepted',
        choices=ACCEPTED_CHOICES,
        label='Статус',
        empty_label='любой',
    )

    # bulletin__title = CharFilter(
    #     field_name='bulletin__title',
    #     lookup_expr='icontains',
    #     label='Заголовок содержит'
    # )

    bulletin = ModelChoiceFilter(
        field_name='bulletin',
        label='Заголовок объявления',
        empty_label = 'любой',
    )

    bulletin__category = ModelChoiceFilter(
        field_name='bulletin__category',
        queryset=Category.objects.all(),
        label='Категория:',
        empty_label='любая',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bulletin_qs = Bulletin.objects.filter(author=kwargs['request'].user)
        self.filters['bulletin'].extra['queryset'] = bulletin_qs

