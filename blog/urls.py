# urls.py
from django.urls import path
# from .views import blog

from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("blog-listing/", views.blog_list, name="blog_list"),
    path("category/<slug:slug>/", views.blog_category, name="blog_category"),
    path("<slug:slug>/", views.blog_detail, name="blog_detail"),
]
