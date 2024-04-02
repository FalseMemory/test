import os


def get_download_dir():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "file", "wegame_client")
    return path


def get_file_dir():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "file")
    return path


def get_screen_dir():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "file", "screen")
    return path

def get_data_dir():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    return path