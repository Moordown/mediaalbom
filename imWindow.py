import cv2
import sys
import os
import numpy as np
from itertools import chain, starmap
from functools import partial


IMAGE_PATH = ".\\images\\{}"
IMAGE_NAMES = [IMAGE_PATH.format(i) for i in [
    'bat1.jpg', 'bike.jpg', 'moustache.jpg', 'pink.jpg', 'silver1.jpg'
]]
EXTENTIONS = ['.png', '.jpg']


def iter_filenames(path):
    """Возвращает итератор по всем файлам в дирректории и поддиректориях"""
    return chain.from_iterable(
        starmap(lambda dp, _, fn: map(partial(os.path.join, dp), fn), os.walk(path))
    )


def with_extensions(extensions, filenames):
    """Фильтрует файлы по расширению"""
    return filter(lambda f: get_extension(f) in extensions, filenames)


def get_extension(filename):
    """Получает расширение имени файла"""
    return os.path.splitext(filename)[1]


def get_files_from(extentions, path):
    """Возвращает итератор по именам файлов с данными
     расширениями из данной дирректории"""
    return with_extensions(extentions, iter_filenames(path))


def get_images_array(path):
    """Возвращается итератор по массивам, содержащим картинки по заданному пути"""
    for im_name in get_files_from(['.png', '.jpg'], path):
        yield cv2.imread(im_name, 1)


