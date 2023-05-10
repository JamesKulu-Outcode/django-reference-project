from collections import OrderedDict
import math
from apps.chat.models import UserRoom

def get_meta(self, data):
    page_size = int(self.request.query_params.get('page_size') \
        if self.request.query_params.get('page_size') else self.page_size)
    current_page = int(self.get_page_number(
                                self.request, 
                                self.page.paginator
                                ))
    total = self.page.paginator.count

    if self.request.resolver_match.view_name == 'chat-room-list':
        return OrderedDict(
            [
                (
                    'meta',
                    {
                        'next': self.get_next_link(),
                        'previous': self.get_previous_link(),
                        'current_page': current_page,
                        'from': ((current_page - 1) * page_size) + 1,
                        'last_page': math.ceil(total / page_size),
                        'per_page': page_size or self.page_size,
                        'to': (current_page * page_size)
                        if (current_page * page_size) < total
                        else total,
                        'total': total,
                    },
                ),
                ('data', data),
                (
                    'unread_count',
                    UserRoom.objects.filter(
                        user=self.request.user, is_seen=False, room__organization=self.request.user.organization or None
                    ).count(),
                ),
            ]
        )
    return OrderedDict(
        [
            (
                'meta',
                {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                    'current_page': current_page,
                    'from': ((current_page - 1) * page_size) + 1,
                    'last_page': math.ceil(total / page_size),
                    'per_page': page_size or self.page_size,
                    'to': (current_page * page_size)
                    if (current_page * page_size) < total
                    else total,
                    'total': total,
                },
            ),
            ('data', data),
        ]
    )
