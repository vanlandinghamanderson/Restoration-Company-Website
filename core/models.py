# django-imagekit creates smaller copies of uploaded images,
# so pages don't have to download the full-size originals.
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


# Video for the Carousel
class CarouselBackground(models.Model):
    title = models.CharField(max_length=100)
    caption = models.CharField(max_length=200)
    description = models.TextField(default='')
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

    def grouped_hours(self):
        """ Combine consecutive days with the same hours into a single entry. """
        groups = []
        for hour in self.business_hours.all():
            key = (hour.is_closed, hour.open_time, hour.close_time)
            if groups and groups[-1]['key'] == key and groups[-1]['end_num'] == hour.day - 1:
                groups[-1]['end_num'] = hour.day
                groups[-1]['end_day'] = hour.get_day_display()
            else:
                groups.append({
                    'key': key,
                    'start_day': hour.get_day_display(),
                    'end_day': hour.get_day_display(),
                    'end_num': hour.day,
                    'is_closed': hour.is_closed,
                    'open_time': hour.open_time,
                    'close_time': hour.close_time,
                })

        for group in groups:
            if group['start_day'] == group['end_day']:
                group['label'] = group['start_day']
            else:
                group['label'] = f"{group['start_day']} - {group['end_day']}"
        return groups
    

class BusinessHours(models.Model):
    class Weekday(models.IntegerChoices):
        MONDAY = 0, 'Monday'
        TUESDAY = 1, 'Tuesday'
        WEDNESDAY = 2, 'Wednesday'
        THURSDAY = 3, 'Thursday'
        FRIDAY = 4, 'Friday'
        SATURDAY = 5, 'Saturday'
        SUNDAY = 6, 'Sunday'

    site_settings = models.ForeignKey('SiteSetting', on_delete=models.CASCADE, related_name='business_hours')
    day = models.IntegerField(choices=Weekday.choices)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ['day']
        verbose_name_plural = 'Business Hours'
        constraints = [
            models.UniqueConstraint(fields=['site_settings', 'day'], name='unique_business_hours_per_day')
        ]

    def clean(self):
        if self.is_closed:
            return
        if not self.open_time or not self.close_time:
            raise ValidationError("Open and close times must be set if the business is not closed.")
        if self.open_time >= self.close_time:
            raise ValidationError("Open time must be before close time.")

    def __str__(self):
        if self.is_closed:
            return f'{self.get_day_display()}: Closed'
        return f'{self.get_day_display()}: {self.open_time:%I:%M %p} - {self.close_time:%I:%M %p}'

# Needs to be altered eventually
class Service(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    short_description = models.TextField(default='')
    order = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=False, blank=True, null=True) #Safe for now
    is_active = models.BooleanField(default=True)

    # A smaller, faster-loading version of `image` used on the service cards.
    # - Not stored in the database, so no migration is needed.
    # - Generated the first time it's requested and saved in media/CACHE/.
    # - Cropped to 800x450 (16:9) to match the card's aspect ratio in CSS.
    # - Format must be "JPEG" (not "JPG"), or Pillow raises a KeyError.
    image_card = ImageSpecField(
        source="image",
        processors=[ResizeToFill(800, 450)],
        format="JPEG",
        options={"quality": 75},
    )

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

    def get_after_alt(self):
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

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

# Customer Table for customers who write a message on the contact page
class Customer(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    requested_service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f'{self.full_name} - wrote a message on {self.created_at.strftime("%Y-%m-%d")}'