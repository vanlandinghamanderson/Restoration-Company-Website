from django.shortcuts import render
from .models import RestorationCarouselBackground, RestorationSiteSetting, RestorationService, RestorationCertification

# Home page view
def index(request):
    context = {
        'restoration_carousel_background' : RestorationCarouselBackground.objects.filter(is_active=True).order_by('order'),
        'restoration_site_setting' : RestorationSiteSetting.objects.first(),
        'restoration_services': RestorationService.objects.all(),
        'restoration_certifications': RestorationCertification.objects.all()
    }
    return render(request, 'core/index.html', context)