import unittest
import imWindow as imWin
import cv2

class ImageDownload(unittest.TestCase):
    def setUp(self):
        self.image_path = ".\\images\\{}"
        self.image_names = [self.image_path.format(i) for i in [
            'bat1.jpg', 'bike.jpg', 'moustache.jpg', 'pink.jpg', 'silver1.jpg'
        ]]
        self.extentions = ['.png', '.jpg']

    def testCorrectImageNames(self):
        self.assertListEqual(
            list(imWin.get_files_from(self.extentions, self.image_path[:-2])),
            self.image_names
        )


if __name__ == '__main__':
    unittest.main()
