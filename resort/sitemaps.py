from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import RoomCategory


class StaticSitemap(Sitemap):
    priority = 1.0
    changefreq = "daily"

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)



class RoomSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return RoomCategory.objects.all()

    def location(self, obj):
        return reverse('room_detail', args=[obj.slug])
