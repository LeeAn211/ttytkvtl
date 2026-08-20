from django import template
import datetime

register = template.Library()

@register.filter
def thu_viet(value):
    if not isinstance(value, datetime.datetime):
        return value
    days = ['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ nhật']
    day_name = days[value.weekday()]
    return f"{day_name}, {value.strftime('%H:%M %d/%m/%Y')}"
