from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),

    # App chính
    path('', include('main.urls')),

    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # MEDIA
    re_path(
        r'^media/(?P<path>.*)$',
        serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
]