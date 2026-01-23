from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Blog, BlogCategory


class BlogStaticSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ["blog:blog_list"]

    def location(self, item):
        return reverse(item)


class BlogCategorySitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return BlogCategory.objects.all()

    def location(self, obj):
        return reverse("blog:blog_category", args=[obj.slug])


class BlogDetailSitemap(Sitemap):
    priority = 0.9
    changefreq = "daily"

    def items(self):
        return Blog.objects.filter(status="published")

    def location(self, obj):
        return reverse("blog:blog_detail", args=[obj.slug])
