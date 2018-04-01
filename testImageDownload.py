import unittest
import imWindow as imWin


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

    def testCorrectResize(self):
        embedding_size = (300, 300)

        count = 0
        for image in imWin.get_resized_images(self.image_path[:-2], *embedding_size):
            self.assertLessEqual(image.shape[:2], embedding_size,
                             "error with image {}. Expect embedding in {}, got {}".format(
                                 self.image_names[count], embedding_size, image.shape[:2]
                             ))
            count += 1


if __name__ == '__main__':
    unittest.main()
