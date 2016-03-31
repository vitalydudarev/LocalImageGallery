import config
import ioutils
import os.path
import worker

def init():
    ioutils.create_directory(config.THUMB_PATH)

def create_thumbnails():
    worker_obj = worker.Worker()
    worker_obj.work()
    processed = worker_obj.get_result()
    result = {}
    for i in range(len(processed)):
        file_name = processed[i]
        thumb_file_name = ioutils.get_thumb_name(file_name, config.THUMB_PATH)
        result[file_name] = thumb_file_name

    return result