from django.shortcuts import render
from .models import RestorationCarouselBackground, RestorationServiceArea, RestorationSiteSetting, RestorationService, RestorationCertification, RestorationReview, RestorationTeam, RestorationProject

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

# Gallery Page
def gallery(request):
    context = {
        'restoration_site_setting' : RestorationSiteSetting.objects.first(),
        'restoration_services' : RestorationService.objects.all(),
        'restoration_service_areas' : RestorationServiceArea.objects.all(),

        'restoration_projects' : RestorationProject.objects.all(),
    }
    return render(request, 'core/gallery.html', context)


# About Us Page
def about(request):
    context = {
        'restoration_site_setting': RestorationSiteSetting.objects.first(),
        'restoration_services': RestorationService.objects.all(),
        'restoration_service_areas': RestorationServiceArea.objects.all(),
        'restoration_team_members': RestorationTeam.objects.all(),
    }
    return render(request, 'core/about.html', context)

# Contact Page
def contact(request):
    context = {
        'restoration_site_setting': RestorationSiteSetting.objects.first(),
        'restoration_services' : RestorationService.objects.all(),
        'restoration_service_areas' : RestorationServiceArea.objects.all(),
    }
    return render(request, 'core/contact.html', context)

# Our Services Page
def service_list(request):
    context = {
        'restoration_site_setting' : RestorationSiteSetting.objects.first(),
        'restoration_services' : RestorationService.objects.all(),
        'restoration_service_areas' : RestorationServiceArea.objects.all(),
    }
    return render(request, 'core/services.html', context)

# Our Service Detail
def service_detail(request, slug):
    context = {
        'restoration_site_setting' : RestorationSiteSetting.objects.first(),
        'restoration_services' : RestorationService.objects.all(),
        'restoration_service_areas' : RestorationServiceArea.objects.all(),

        # Gets the slug from the Service model
        'restoration_service': RestorationService.objects.get(slug=slug)
    }
    return render(request, 'core/service_detail.html', context)