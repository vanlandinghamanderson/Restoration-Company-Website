from django.db import models

# Video for the Carousel
class RestorationCarouselBackground(models.Model):
    title = models.CharField(max_length=100)
    caption = models.CharField(max_length=200)
    description = models.TextField(default=True)
    video_file = models.FileField(upload_to='carousel_videos/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

# Site Setting for the Company
class RestorationSiteSetting(models.Model):
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

    def __str__(self):
        return self.company_name