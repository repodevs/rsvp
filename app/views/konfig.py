from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from app.models import Konfig


def konfigsx(request):
    konfigs = Konfig.objects.all()
    return render(request, 'konfigs.html', {'records': konfigs})

def konfigs(request):
    if request.method == "POST":
        # Define all expected configuration keys
        config_keys = [
            'welcome_message',
            'motivations', 
            'bride_groom',
            'wedding_date',
            'location',
            'live_streaming',
            'gifts',
            'rsvp',
            'ucapan_doa',
            'penutup'
        ]

        # Process each configuration key
        for key in config_keys:
            # If checkbox is checked, it will be in request.POST with value "1"
            # If unchecked, it won't be in request.POST, so we set it to "0"
            value = "1" if key in request.POST else "0"
            Konfig.objects.update_or_create(key=key, defaults={"value": value})

        return redirect('konfigs')

    konfigs = {k.key: k.value for k in Konfig.objects.all()}
    return render(request, "konfigs.html", {"records": konfigs})

def api_configs(request):
    """
    API endpoint to get all configurations as JSON
    """
    if request.method == "GET":
        configs = {}
        for config in Konfig.objects.all():
            # Convert "1"/"0" strings to boolean for better API response
            configs[config.key] = config.value == "1"
        
        return JsonResponse({
            "success": True,
            "configs": configs
        })
    
    return JsonResponse({
        "success": False,
        "error": "Method not allowed"
    }, status=405)
