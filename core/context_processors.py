from .models import RestorationSiteSetting, RestorationService, RestorationServiceArea

def site_globals(request):
    return {
        'restoration_site_setting': RestorationSiteSetting.objects.first(),
        'restoration_services': RestorationService.objects.all(),
        'restoration_service_areas': RestorationServiceArea.objects.all(),
    }