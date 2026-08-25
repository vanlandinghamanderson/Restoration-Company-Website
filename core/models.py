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

# Needs to be altered eventually
class RestorationService(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField(default=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

# Certification model for this company earned
class RestorationCertification(models.Model):
    image = models.ImageField(upload_to='certifications/')
    alt_text = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True)
    caption = models.TextField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

# Service Area model
class RestorationServiceArea(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, default='NC')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'city']
        verbose_name = 'Restoration Service Area'
        verbose_name_plural = 'Restoration Service Areas'

    def __str__(self):
        return f'{self.city}, {self.state}'

# Review Model
class RestorationReview(models.Model):
    rating = models.PositiveSmallIntegerField(default=5)
    quote = models.TextField()
    name = models.CharField(max_length=120)
    service_area = models.ForeignKey(RestorationServiceArea, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(RestorationService, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Restoration Review'
        verbose_name_plural = 'Restoration Reviews'

    def __str__(self):
        return f"{self.name}, ({self.rating}*)"

# Team Model
class RestorationTeam(models.Model):
    image = models.ImageField(upload_to='restoration_team')
    team_member = models.CharField(max_length=255, blank=True)
    occupation = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'team_member', 'occupation']
        verbose_name = 'Restoration Team'

    def __str__(self):
        return f"{self.team_member}, ({self.occupation})"

# Project Model
class RestorationProject(models.Model):
    service = models.ForeignKey(RestorationService, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    before_image = models.ImageField(upload_to='restoration_projects/before/')
    before_alt_text = models.CharField(max_length=250, blank=True)
    after_image = models.ImageField(upload_to='restoration_projects/after/')
    after_alt_txt = models.CharField(max_length=250, blank=True)
    caption = models.TextField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Restoration Projects'
        verbose_name_plural = "Restoration Projects"

    def __str__(self):
        return self.title or f"{self.service.name} gallery item"

    def get_before_alt(self):
        return self.before_alt_text or f"{self.service.name} before restoration damage"

    def __str__ (self):
        return self.after_alt_txt or f"{self.service.name} after restoration damage"

    