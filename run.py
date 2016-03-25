# -*- coding: utf-8 -*-
import adapter
import ioutils
import config

#print ioutils.get_files(config.IMAGES_PATH, config.EXTENSIONS)
print adapter.create_thumbnails()