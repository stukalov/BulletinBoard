"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from ckeditor_uploader import views as ck_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path, include
from django.views.decorators.cache import never_cache

from board.urls import board_urlpatterns
from board.views import index_page


ck_urlpatterns = [
    re_path(r"^upload/", login_required(ck_views.upload), name="ckeditor_upload"),
    re_path(
        r"^browse/",
        never_cache(login_required(ck_views.browse)),
        name="ckeditor_browse",
    ),
]

urlpatterns = (
    [
        path('', index_page),
        path('accounts/', include('django.contrib.auth.urls')),
        path('board/', include(board_urlpatterns)),

        re_path(r"^admin/", admin.site.urls),
        re_path(r"^ckeditor/", include(ck_urlpatterns)),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
