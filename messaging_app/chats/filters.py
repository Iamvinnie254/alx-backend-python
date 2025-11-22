import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    """
    Filter messages by:
    - user involved (sender or receiver)
    - time range (created_at__gte, created_at__lte)
    """

    user = django_filters.NumberFilter(method='filter_by_user')
    start_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    def filter_by_user(self, queryset, name, value):
        # Return messages where this user is either sender OR receiver
        return queryset.filter(
            sender_id=value
        ) | queryset.filter(
            receiver_id=value
        )

    class Meta:
        model = Message
        fields = ['user', 'start_date', 'end_date']
