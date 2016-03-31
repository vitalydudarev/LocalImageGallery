import threading
import Queue
import ioutils
import config
import localimage

class Worker:
    THREAD_COUNT = 2

    q = Queue.Queue()
    result = []

    def get_result(self):
        return self.result

    def do_work(self):
        while True:
            file_name = self.q.get()
            thumb_file_name = ioutils.get_thumb_name(file_name, config.THUMB_PATH)
            localimage.thumb(file_name, thumb_file_name, config.THUMB_SIZE)
            self.result.append(file_name)
            self.q.task_done()

    def work(self):
        files = ioutils.get_files(config.IMAGES_PATH, config.EXTENSIONS)
        res = {}

        for i in range(0, config.LIMIT):
            self.q.put(files[i])

        for i in range(0, self.THREAD_COUNT):
            t = threading.Thread(target=self.do_work)
            t.daemon = True
            t.start()

        self.q.join()