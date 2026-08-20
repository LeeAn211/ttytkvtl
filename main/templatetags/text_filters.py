from django import template
import html

register = template.Library()

@register.filter(name='html_unescape')
def html_unescape(value):
    """
    Chuyển các HTML entities (ví dụ &agrave;) thành ký tự thật (à).
    Trả về chuỗi thường — không mark_safe, an toàn khi dùng sau striptags.
    """
    if value is None:
        return ''
    return html.unescape(str(value))
