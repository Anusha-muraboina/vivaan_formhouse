"""
URL configuration for resort_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView
from resort.sitemaps import clean_sitemap
from django.contrib.sitemaps.views import sitemap
from resort.sitemaps import StaticSitemap, RoomCategorySitemap
from blog.sitemaps import (
    BlogListSitemap,
    BlogDetailSitemap,
)

sitemaps = {
    'static': StaticSitemap,
    'rooms': RoomCategorySitemap,
    "blog_list": BlogListSitemap,
    # "blogs": BlogDetailSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('vivvan_admin/', include('vivaan_admin.urls')),
    path('', include('resort.urls')),
    path('blog/', include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path(
        'sitemap.xml',
        clean_sitemap,
        {'sitemaps': sitemaps},
        name='sitemap'
    ),
    
    
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain"
        ),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



