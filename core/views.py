from django.shortcuts import render, get_object_or_404
from .models import CarouselBackground, Post, Service, Certification, Review, Team, Project

# Home Page
def index(request):
    context = {
        'restoration_carousel_background' : CarouselBackground.objects.filter(is_active=True).order_by('order'),
        'restoration_certifications': Certification.objects.all(),
        'restoration_reviews' : Review.objects.all(),
    }
    return render(request, 'core/index.html', context)

# Gallery Page
def gallery(request):
    context = {
        'restoration_projects' : Project.objects.all(),
        'active_service': False,
    }
    return render(request, 'core/gallery.html', context)

# About Us Page
def about(request):
    context = {
        'restoration_team_members': Team.objects.all(),
    }
    return render(request, 'core/about.html', context)

# Contact Page
def contact(request):
    return render(request, 'core/contact.html', {})

# Our Services Page
def service_list(request):
    context = {
        'restoration_services': Service.objects.all(),
    }
    return render(request, 'core/services.html', context)

# Blog Page
def blog_list(request):
    service_filter = request.GET.get('service')
    restoration_posts = Post.objects.all()
    restoration_services = Service.objects.filter(is_active=True)
    active_service = None
    if service_filter:
        restoration_posts = restoration_posts.filter(related_service__slug=service_filter)
        active_service = service_filter
    return render(request, 'core/blog_list.html', {
        'restoration_posts': restoration_posts,
        'restoration_services': restoration_services,
        'active_service': active_service,
    })