from .models import SiteSetting, Service, ServiceArea

def site_globals(request):
    return {
        'restoration_services': Service.objects.filter(is_active=True),
        'restoration_service_areas': ServiceArea.objects.all(),
        'restoration_site_setting': SiteSetting.objects.prefetch_related('business_hours').first()
    }