from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import RoomCategory


from django.urls import reverse
from resort.models import RoomCategory
from blog.models import Blog

from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse


from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse


def clean_sitemap(request, sitemaps):
    response = sitemap(request, sitemaps)

    # ✅ VERY IMPORTANT
    response.render()

    xml = response.content.decode("utf-8")

    # remove xhtml namespace
    xml = xml.replace(
        ' xmlns:xhtml="http://www.w3.org/1999/xhtml"', ""
    )

    return HttpResponse(xml, content_type="application/xml")

# ================= STATIC PAGES =================
class StaticSitemap(Sitemap):
    changefreq = "daily"

    def items(self):
        return [
            "home",
            "contact",
            "leave_review",
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        if item == "home":
            return 1.0
        elif item == "contact":
            return 0.8
        elif item == "leave_review":
            return 0.7
        return 0.5


# ================= ROOM CATEGORY =================
class RoomCategorySitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return RoomCategory.objects.all()

    def location(self, obj):
        return reverse("room_detail", args=[obj.slug])




# class StaticSitemap(Sitemap):
#     priority = 1.0
#     changefreq = "daily"

#     def items(self):
#         return [
#             'home',
#             'contact',
#             'leave_review',
#             'cancel_booking',
#         ]

#     def location(self, item):
#         return reverse(item)


# class RoomSitemap(Sitemap):
#     priority = 0.9
#     changefreq = "weekly"

#     def items(self):
#         return RoomCategory.objects.all()

#     def location(self, obj):
#         return reverse('room_detail', args=[obj.slug])
