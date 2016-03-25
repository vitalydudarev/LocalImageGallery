import config
import ioutils
import localimage
import os.path

def init():
    ioutils.create_directory(config.THUMB_PATH)

def create_thumbnails():
    files = ioutils.get_files(config.IMAGES_PATH, config.EXTENSIONS)
    result = { }

    for i in range(0, config.LIMIT):
    	file_name = files[i]
        thumb_file_name = ioutils.get_thumb_name(file_name, config.THUMB_PATH)
        if not os.path.exists(thumb_file_name):
            localimage.thumb(file_name, thumb_file_name, config.THUMB_SIZE)
        result[file_name] = thumb_file_name

    return result