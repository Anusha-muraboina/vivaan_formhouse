from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Blog, BlogCategory


# ================= BLOG LIST PAGE =================
class BlogListSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ["blog:blog_list"]

    def location(self, item):
        return reverse(item)


# ================= BLOG DETAIL =================
class BlogDetailSitemap(Sitemap):
    priority = 0.9
    changefreq = "daily"

    def items(self):
        return Blog.objects.filter(status="published")

    def location(self, obj):
        return reverse("blog:blog_detail", args=[obj.slug])
