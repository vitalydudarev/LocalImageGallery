import threading
import Queue
import ioutils
import config
import localimage

class WorkerProxy:
    started = False

    def __init__(self):
        self.worker = Worker()

    def get_result(self, get_image_link, get_thumb_link):
        if not self.started:
            t = threading.Thread(target=self.worker.work)
            t.start()
            self.started = True
        
        images = self.worker.get_result()
        total = self.worker.get_total_count()
        processed = self.worker.get_processed_count()

        imgs = {}

        for image in images:
            thumb = get_thumb_link(ioutils.get_thumb_name(image, config.THUMB_PATH))
            img = get_image_link(image)
            imgs[img] = thumb

        return {'images':imgs, 'total':total, 'processed':processed}

class Worker:
    THREAD_COUNT = 2

    q = Queue.Queue()
    result = []
    total_count = 0
    processed_count = 0

    def get_processed_count(self):
        return self.processed_count

    def get_total_count(self):
        return self.total_count

    def get_result(self):
        res = self.result
        partial_res = []
        for item in res:
            partial_res.append(item)

        self.processed_count += len(self.result)
        del self.result[:]
        return partial_res

    def get_current_count(self):
        return len(self.result)

    def do_work(self):
        while True:
            file_name = self.q.get()
            thumb_file_name = ioutils.get_thumb_name(file_name, config.THUMB_PATH)
            localimage.thumb(file_name, thumb_file_name, config.THUMB_SIZE)
            self.result.append(file_name)
            self.q.task_done()

    def work(self):
        ioutils.create_directory(config.THUMB_PATH)
        files = ioutils.get_files(config.IMAGES_PATH, config.EXTENSIONS)

        images_count = len(files)
        if (images_count > config.LIMIT):
            images_count = config.LIMIT)

        if (images_count > 0):
            self.total_count = images_count
            res = {}

            for i in range(0, images_count):
                self.q.put(files[i])

            for i in range(0, self.THREAD_COUNT):
                t = threading.Thread(target=self.do_work)
                t.daemon = True
                t.start()

            self.q.join()