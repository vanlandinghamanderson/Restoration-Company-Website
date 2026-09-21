from django.contrib import admin
from .models import CarouselBackground, Post, SiteSetting, Service, Certification, ServiceArea, Review, Team, Project

# Carousel Background Admin
@admin.register(CarouselBackground)
class CarouselBackgroundAdmin(admin.ModelAdmin):
    list_display = ('title', 'caption', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'caption')
    ordering = ('order',)

# Site Setting Admin
@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    fields = ['company_name', 'email', 'phone_number', 'address', 'city', 'state', 'zip_code', 'instagram_url', 'facebook_url', 'twitter_url', 'linkedin_url']
    list_display = ('company_name', 'email', 'phone_number', 'city', 'state')

# Restoration Service Admin
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    prepopulated_fields = {'slug': ('name',)}

# Certification Admin
@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'alt_text', 'caption', 'description']
    list_editable = ['alt_text', 'caption', 'description']

# Restoration Service Areas Admin
@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ['city', 'state', 'order', 'is_active']
    list_editable = ['order', 'is_active']

# Restoration Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['rating', 'name', 'service_area', 'service']
    list_filter = ['service_area', 'service']

# Restoration Team Admin
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['team_member', 'occupation', 'order']
    list_display_links = ('occupation',)

# Restoration Project Admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'service']
    list_filter = ['service']

# Posts Admin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'published_at']
    list_filter = ['is_published', 'related_service']
    prepopulated_fields = {'slug':('title',)}