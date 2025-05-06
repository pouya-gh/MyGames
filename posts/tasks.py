from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task
import zipfile

import urllib.request
import json

import posts

@shared_task
def extract_gamefile(new_game_path, new_game_file):
    """
    extracts the game's zip file so the game upload form can return quicker
    """

    with zipfile.ZipFile(new_game_file, 'r') as thefile:
        thefile.extractall(new_game_path)
    return True


@shared_task
def find_ip_location(ip):
    record: posts.models.SiteVisitTracker = posts.models.SiteVisitTracker.objects.filter(ip=ip).first()
    if record and not record.location:
        with urllib.request.urlopen(f"http://ip-api.com/json/{ip}") as url:
            data = url.read().decode()
            j = json.loads(data)
            location = f"{j['country']}:{j['regionName']}:{j['city']}"
            try:
                record.location = location
                record.save()
            except ObjectDoesNotExist:
                pass
    
    return True
