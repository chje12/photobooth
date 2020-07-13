from datetime import datetime, timedelta
from PIL import Image, ImageWin
from pillow_lut import load_cube_file
from configparser import ConfigParser
import cv2
import os


class Config():
    def __init__(self):
        pass

    @classmethod
    def read_config(cls, section, key):
        parser = ConfigParser()
        parser.read('config.ini')
        value = parser.get(section, key).strip()
        return value


class ImageUtils():
    def __init__(self):
        pass

    @classmethod
    def write_image_by_id(cls, image, template_id, index):
        original_filename = FileUtils.get_original_filename(template_id, index)
        cv2.imwrite(original_filename, image)

    @classmethod
    def write_image_by_path(cls, image, path):
        cv2.imwrite(path, image)

    @classmethod
    def read_image_by_path(cls, path):
        image = cv2.imread(path)
        return image

    @classmethod
    def convert_to_rgb_array(cls, image):
        rgb_array = Image.fromarray(image, mode='RGB')
        return rgb_array

    @classmethod
    def save_filter(cls, lut, lut_path):
        hefe = load_cube_file('file/cube/{lut}.cube'.format(lut=lut))
        im = Image.open(lut_path)
        im.filter(hefe).save(lut_path, quality=100)


class FileUtils():
    def __init__(self):
        pass

    @classmethod
    def get_original_filename(cls, template_id, index):
        image_folder = Config.read_config('settings', 'image')

        original_filename = '{image_folder}/{template_id}/original/{poto_datetime}_org_{index}.jpg'
        original_filename = original_filename.format(image_folder=image_folder
                                                     , template_id=template_id
                                                     , poto_datetime=datetime.today().strftime("%Y%m%d%H%M%S")
                                                     , index=index)
        return original_filename

    @classmethod
    def get_lut_filename(cls, template_id, lut, index):
        image_folder = Config.read_config('settings', 'image')
        lut_filename = '{image_folder}/{template_id}/original/{lut}/{poto_datetime}_org_{index}.jpg'
        lut_filename = lut_filename.format(image_folder=image_folder
                                           , template_id=template_id
                                           , lut=lut
                                           , poto_datetime=datetime.today().strftime("%Y%m%d%H%M%S")
                                           , index=index)
        return lut_filename

    @classmethod
    def force_directories(cls, path):
        os.makedirs(path, exist_ok=True)
