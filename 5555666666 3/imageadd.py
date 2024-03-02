import os
GAME_DIR = ''
def get_res_path(name):
    """ Returns full path to resourse file.
    name - <str> - filename
    """
    return os.path.join(GAME_DIR, 'images', name)