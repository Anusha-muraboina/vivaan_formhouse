from django.db import models

# Create your models here.


from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class BlogCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=160, unique=True , null=True ,blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while BlogCategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
    def __str__(self):
        return self.name


class Blog(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=260, unique=True, blank=True)

    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="blogs"
    )

    short_description = models.TextField(
        help_text="Short summary for listing & SEO"
    )

    content = models.TextField(
        help_text="Full blog content (HTML allowed)"
    )

    featured_image = models.ImageField(
        upload_to="blog_images/",
        null=True,
        blank=True
    )

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    meta_title = models.CharField(
        max_length=255,
        blank=True
    )
    meta_description = models.CharField(
        max_length=300,
        blank=True
    )
    meta_keywords = models.CharField(
        max_length=300,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_date"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == "published" and not self.published_date:
            from django.utils import timezone
            self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title




class BlogTag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True ,null=True ,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogComment(models.Model):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    name = models.CharField(max_length=120)
    email = models.EmailField()
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.blog.title}"
