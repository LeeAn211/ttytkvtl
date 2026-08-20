# main/middleware.py
from datetime import timedelta
from django.utils import timezone
from .models import PageView

def get_client_ip(request):
    """Lấy địa chỉ IP của client."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class PageViewMiddleware:
    """
    Đếm lượt truy cập:
      - Mỗi URL, mỗi client chỉ đếm 1 lần trong 15 phút.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Chỉ đếm GET và không đếm admin, static, media
        if request.method == 'GET' and not request.path.startswith(('/admin', '/static', '/media')):
            viewed_key = f'viewed_{request.path}'
            now = timezone.now()
            last_view_time = request.session.get(viewed_key)
            allow_new = True

            if last_view_time:
                try:
                    from datetime import datetime
                    last_time = datetime.fromisoformat(last_view_time)
                except ValueError:
                    last_time = None

                if last_time and now - last_time < timedelta(minutes=15):
                    allow_new = False  # chưa đủ 15 phút, không đếm

            if allow_new:
                PageView.objects.create(
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
                    path=request.path
                )
                request.session[viewed_key] = now.isoformat()

        return response
