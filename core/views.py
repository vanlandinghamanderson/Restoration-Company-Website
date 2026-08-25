from django.shortcuts import render, get_object_or_404
from .models import RestorationCarouselBackground, RestorationService, RestorationCertification, RestorationReview, RestorationTeam, RestorationProject

# Home Page
def index(request):
    context = {
        'restoration_carousel_background' : RestorationCarouselBackground.objects.filter(is_active=True).order_by('order'),
        'restoration_certifications': RestorationCertification.objects.all(),
        'restoration_reviews' : RestorationReview.objects.all(),
    }
    return render(request, 'core/index.html', context)

# Gallery Page
def gallery(request):
    context = {
        'restoration_projects' : RestorationProject.objects.all(),
        'active_service': False,
    }
    return render(request, 'core/gallery.html', context)

# About Us Page
def about(request):
    context = {
        'restoration_team_members': RestorationTeam.objects.all(),
    }
    return render(request, 'core/about.html', context)

# Contact Page
def contact(request):
    return render(request, 'core/contact.html', {})

# Our Services Page
def service_list(request):
    return render(request, 'core/services.html', {})

