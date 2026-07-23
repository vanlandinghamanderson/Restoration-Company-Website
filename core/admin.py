from django.contrib import admin
from .models import RestorationCarouselBackground, RestorationSiteSetting

# Carousel Background Admin
class RestorationCarouselBackgroundAdmin(admin.ModelAdmin):
    list_display = ('title', 'caption', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'caption')
    ordering = ('order',)

# Restoration Site Setting Admin
class RestorationSiteSettingAdmin(admin.ModelAdmin):
    fields = ['company_name', 'email', 'phone_number', 'address', 'city', 'state', 'zip_code', 'instagram_url', 'facebook_url', 'twitter_url', 'linkedin_url']
    list_display = ('company_name', 'email', 'phone_number', 'city', 'state')

admin.site.register(RestorationCarouselBackground, RestorationCarouselBackgroundAdmin)
admin.site.register(RestorationSiteSetting, RestorationSiteSettingAdmin)