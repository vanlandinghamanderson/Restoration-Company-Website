from django.shortcuts import render
from .models import RestorationCarouselBackground, RestorationSiteSetting

# Home page view
def index(request):
    context = {
        'restoration_carousel_background' : RestorationCarouselBackground.objects.filter(is_active=True).order_by('order'),
        'restoration_site_setting' : RestorationSiteSetting.objects.first(),
    }
    return render(request, 'core/index.html', context)