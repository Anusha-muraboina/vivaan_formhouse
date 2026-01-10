from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


from django.shortcuts import render, get_object_or_404
from django.db.models import F
from .models import Blog, BlogCategory


from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, F
from .models import Blog, BlogCategory, BlogTag, BlogComment


def blog_list(request):
    blogs = Blog.objects.filter(status="published").select_related("category")

    # Search
    q = request.GET.get("q")
    if q:
        blogs = blogs.filter(
            Q(title__icontains=q) |
            Q(short_description__icontains=q) |
            Q(content__icontains=q)
        )

    # Category filter
    category_slug = request.GET.get("category")
    if category_slug:
        blogs = blogs.filter(category__slug=category_slug)

    # Tag filter
    tag_slug = request.GET.get("tag")
    if tag_slug:
        blogs = blogs.filter(tags__slug=tag_slug)

    context = {
        "blogs": blogs,
        "categories": BlogCategory.objects.all(),
        "tags": BlogTag.objects.all(),
        "recent_comments": BlogComment.objects.filter(is_approved=True).order_by("-created_at")[:5],
    }
    return render(request, "blog/blog_list.html", context)

def blog_category(request, slug):
    category = get_object_or_404(BlogCategory, slug=slug)
    blogs = category.blogs.filter(status="published")

    context = {
        "category": category,
        "blogs": blogs,
    }
    return render(request, "blog/blog_category.html", context)

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status="published")

    # Increase views
    Blog.objects.filter(id=blog.id).update(views_count=F("views_count") + 1)
    blog.refresh_from_db()

    # Handle comment submit
    if request.method == "POST":
        BlogComment.objects.create(
            blog=blog,
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            comment=request.POST.get("comment"),
        )
        return redirect("blog:blog_detail", slug=blog.slug)

    context = {
        "blog": blog,
        "comments": blog.comments.filter(is_approved=True),
        "categories": BlogCategory.objects.all(),
        "tags": BlogTag.objects.all(),
    }
    return render(request, "blog/blog_detail.html", context)
