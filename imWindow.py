import cv2
import sys
import os
import numpy as np
from itertools import chain, starmap
from functools import partial


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


def get_resized_images(path: str, x: int, y: int):
    """Возвращает картинку, которая будет входить в заданный размер"""
    for im_array in get_images_array(path):
        dx, dy = im_array.shape[1] - x, im_array.shape[0] - y
        if dx <= 0 and dy <= 0:
            yield im_array
        else:
            if dx < dy:
                new_size = (x, x / im_array.shape[1])
            else:
                new_size = (y / im_array.shape[0], y)
            yield cv2.resize(src=im_array, dsize=new_size)
