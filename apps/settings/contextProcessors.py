from .models import SiteSettingsModel

def processors(request):
    siteSettings = SiteSettingsModel.objects.filter().first()
    context = {
            'siteSettings': siteSettings,
        }
    return context