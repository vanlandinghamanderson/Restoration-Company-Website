from .models import SiteSetting, Service, ServiceArea
# Step 3: Import the settings
from django.conf import settings

def site_globals(request):
    return {
        'restoration_services': Service.objects.filter(is_active=True),
        'restoration_service_areas': ServiceArea.objects.all(),
        'restoration_site_setting': SiteSetting.objects.prefetch_related('business_hours').first(),
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }