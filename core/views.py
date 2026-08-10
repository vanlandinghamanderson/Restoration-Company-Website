from django.shortcuts import render
from .models import RestorationCarouselBackground, RestorationServiceArea, RestorationSiteSetting, RestorationService, RestorationCertification, RestorationReview, RestorationTeam

# Home Page
def index(request):
    context = {
        'restoration_carousel_background' : RestorationCarouselBackground.objects.filter(is_active=True).order_by('order'),
        'restoration_site_setting' : RestorationSiteSetting.objects.first(),
        'restoration_services': RestorationService.objects.all(),
        'restoration_certifications': RestorationCertification.objects.all(),
        'restoration_reviews' : RestorationReview.objects.all(),
        'restoration_service_areas' : RestorationServiceArea.objects.all(),
    }
    return render(request, 'core/index.html', context)

# About Us Page
def about(request):
    context = {
        'restoration_site_setting': RestorationSiteSetting.objects.first(),
        'restoration_services': RestorationService.objects.all(),
        'restoration_services_areas': RestorationServiceArea.objects.all(),
        'restoration_team_members': RestorationTeam.objects.all(),
    }
    return render(request, 'core/about.html', context)