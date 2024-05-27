from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Game
from django.conf import settings
from .tasks import extract_gamefile

import zipfile
import shutil

@receiver(post_save, sender=Game)
def extract_game_file(sender, instance, **kwargs):
    """
    extract the contents of the game zip file. this method only works if a new game is being created. 
    in the case of a file update, the Model's "save" method is overriden to take care of it. 
    if i wanted to also do that using siganals, i should have also used a "pre_save" signal to check which fields have changed
    TODO: use celery instead of this
    """
    if kwargs['created']:
        extract_gamefile.delay(str(settings.MEDIA_ROOT / instance.file_path_maker()),
                         str(instance.file.path))
        # with zipfile.ZipFile(instance.file.path, 'r') as thefile:
        #     thefile.extractall(settings.MEDIA_ROOT / game_file_path_maker(instance))
        
@receiver(post_delete, sender=Game)
def delete_game_files(sender, instance, **kwargs):
    """
    deletes both 'image' folder and 'file' folder of a Game after deletion. 
    i'm sending an empty string as the 2nd argument of "game_file_path_maker" so i can delete the whole game's folder
    """
    shutil.rmtree(settings.MEDIA_ROOT / instance.file_path_maker(''))