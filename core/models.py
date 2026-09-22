from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Video for the Carousel
class CarouselBackground(models.Model):
    title = models.CharField(max_length=100)
    caption = models.CharField(max_length=200)
    description = models.TextField(default=True)
    video_file = models.FileField(upload_to='carousel_videos/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Carousel Background'

    def __str__(self):
        return self.title

# Site Setting for the Company
class SiteSetting(models.Model):
    company_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    instagram_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Site Setting'

    def __str__(self):
        return self.company_name

# Needs to be altered eventually
class Service(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=100, default='service', help_text='Icon needed')
    short_description = models.TextField(default=True)
    order = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=False, blank=True, null=True) #Safe for now
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.name

# Certification model for this company earned
class Certification(models.Model):
    image = models.ImageField(upload_to='certifications/')
    alt_text = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True)
    caption = models.TextField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Certifications'

    def __str__(self):
        return self.title

# Service Area model
class ServiceArea(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, default='NC')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'city']
        verbose_name_plural = 'Service Areas'

    def __str__(self):
        return f'{self.city}, {self.state}'

# Review Model
class Review(models.Model):
    rating = models.PositiveSmallIntegerField(default=5)
    quote = models.TextField()
    name = models.CharField(max_length=120)
    service_area = models.ForeignKey(ServiceArea, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"{self.name}, ({self.rating}*)"

# Team Model
class Team(models.Model):
    image = models.ImageField(upload_to='restoration_team')
    team_member = models.CharField(max_length=255, blank=True)
    occupation = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'team_member', 'occupation']
        verbose_name = 'Team'

    def __str__(self):
        return f"{self.team_member}, ({self.occupation})"

# Project Model
class Project(models.Model):
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    before_image = models.ImageField(upload_to='restoration_projects/before/')
    before_alt_text = models.CharField(max_length=250, blank=True)
    after_image = models.ImageField(upload_to='restoration_projects/after/')
    after_alt_txt = models.CharField(max_length=250, blank=True)
    caption = models.TextField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title or f"{self.service.name} gallery item"

    def get_before_alt(self):
        return self.before_alt_text or f"{self.service.name} before restoration damage"

    def __str__ (self):
        return self.after_alt_txt or f"{self.service.name} after restoration damage"

class Post(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField(blank=True, default="")    
    content = models.TextField()
    author = models.CharField(max_length=200, default='StaDry Restorations')
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    related_service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name_plural = 'Posts'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absoulte_url(self):
        return reverse('core:blog_detail', kwargs={'slug': self.slug})