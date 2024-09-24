from .models import SiteSettingsModel

def processors(request):
    site_settings = SiteSettingsModel.objects.filter().first()
    context = {
            'site_settings': site_settings,
        }
    return context