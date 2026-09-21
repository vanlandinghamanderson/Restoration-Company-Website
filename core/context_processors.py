from .models import SiteSetting, Service, ServiceArea

def site_globals(request):
    return {
        'restoration_site_setting': SiteSetting.objects.first(),
        'restoration_services': Service.objects.all(),
        'restoration_service_areas': ServiceArea.objects.all(),
    }