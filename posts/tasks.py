from celery import shared_task
import zipfile

@shared_task
def extract_gamefile(new_game_path, new_game_file):
    """
    extracts the game's zip file so the game upload form can return quicker
    """

    with zipfile.ZipFile(new_game_file, 'r') as thefile:
        thefile.extractall(new_game_path)
    return True
