from django.db import models
from ckeditor.fields import RichTextField

from django.utils.text import slugify


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=2, unique=True)  # ISO country code
    is_default = models.BooleanField(default=False)  # Mark default country

    def __str__(self):
        return self.name
    
class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    cpr = models.CharField(max_length=20, blank=True, null=True)

    TYPE_OF_REQUEST_CHOICES = [
        ('rent_car', 'Rent a car'),
        ('travel', 'Travel'),
        ('business_center', 'Business Center'),
    ]
    type_of_request = models.CharField(max_length=50, choices=TYPE_OF_REQUEST_CHOICES)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.get_type_of_request_display()}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class GalleryItem(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='gallery/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='gallery_items')
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.ForeignKey(Country,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.title or f"Gallery Item {self.id}"



class Author(models.Model):
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='authors/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)  # allow blank so we can generate it
    description = RichTextField(blank=True, null=True)
    content = RichTextField()
    image = models.ImageField(upload_to='blog_images/')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
    featured = models.BooleanField(default=False)
    reading_time = models.PositiveIntegerField(help_text="Time in minutes", default=3)
    created_at = models.DateField(auto_now_add=True)
    country = models.ForeignKey(Country,on_delete=models.SET_NULL,null=True,blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

   