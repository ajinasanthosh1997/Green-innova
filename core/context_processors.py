from .models import SiteConfiguration

def contact_info(request):
    config = SiteConfiguration.objects.first()
    if not config:
        config = SiteConfiguration.objects.create()  # creates singleton with defaults
    return {
        'contact_phone': config.phone,
        'contact_email': config.email,
        'contact_address': config.address,
        'social_links': {
            'linkedin': config.linkedin,
            'instagram': config.instagram,
            'facebook': config.facebook,
            'youtube': config.youtube,
        },
        'map_embed_url': config.map_embed_url,
    }