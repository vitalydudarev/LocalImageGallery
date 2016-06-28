# -*- coding: utf-8 -*-
import threading
import Queue
import ioutils
import config
import localimage


class WorkerProxy:
    def __init__(self):
        self.__worker = Worker()
        self.__worker.init()
        self.__started = False

    def get_result(self, get_image_link, get_thumb_link):
        if not self.__started:
            t = threading.Thread(target=self.__worker.work)
            t.start()
            self.__started = True

        images = self.__worker.get_result()
        total = self.__worker.get_total_count()
        processed = self.__worker.get_processed_count()

        imgs = []

        for image in images:
            thumb = get_thumb_link(ioutils.get_thumb_name(image, config.THUMB_PATH))
            img = get_image_link(image)
            imgs.append({'name': img, 'thumb': thumb, 'title': image})

        return {'images': imgs, 'total': total, 'processed': processed}


class Worker:
    THREAD_COUNT = 2

    def __init__(self):
        self.__queue = Queue.Queue()
        self.__current_result = []
        self.__result = []
        self.__total_count = 0
        self.__processed_count = 0
        self.__files_to_process = []
        self.__finished = False
        self.__lock = threading.Lock()

    def get_processed_count(self):
        return self.__processed_count

    def get_total_count(self):
        return self.__total_count

    def get_result(self):
        if self.__finished:
            return self.__result

        current_result = []
        for item in self.__current_result:
            current_result.append(item)

        self.__result += current_result
        self.__processed_count += len(self.__current_result)

        if self.__processed_count == self.__total_count:
            self.__finished = True

        with self.__lock:
            del self.__current_result[:]

        return current_result

    def do_work(self):
        while True:
            file_name = self.__queue.get()
            thumb_file_name = ioutils.get_thumb_name(file_name, config.THUMB_PATH)
            localimage.thumb(file_name, thumb_file_name, config.THUMB_SIZE)
            
            with self.__lock:
                self.__current_result.append(file_name)

            self.__queue.task_done()

    def init(self):
        ioutils.create_directory(config.THUMB_PATH)
        files = ioutils.get_files(config.IMAGES_PATH, config.EXTENSIONS)

        images_count = len(files)
        if images_count > config.LIMIT:
            images_count = config.LIMIT

        self.__files_to_process = files
        self.__total_count = images_count

    def work(self):
        if self.__total_count > 0:

            for i in range(0, self.__total_count):
                self.__queue.put(self.__files_to_process[i])

            for i in range(0, self.THREAD_COUNT):
                t = threading.Thread(target=self.do_work)
                t.daemon = True
                t.start()

            self.__queue.join()
