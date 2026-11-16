from .models import SiteSetting, Service, ServiceArea
# Step 3: Import the settings
from django.conf import settings

def site_globals(request):
    site_setting = SiteSetting.objects.prefetch_related('business_hours').first()
    services = Service.objects.filter(is_active=True)
    service_areas = ServiceArea.objects.all()
    return {
        'services': services,
        'service_areas': service_areas,
        'site_setting': site_setting,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }