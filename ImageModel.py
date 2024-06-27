import cv2
import numpy as np
from pyqtgraph import PlotWidget
from PyQt5.QtGui import QPixmap, QImage

import enum
import logging

logger = logging.getLogger()


class Modes(enum.Enum):
    magnitude = "MagMode"
    phase = "phaseMode"
    real = "realMode"
    Imaginary = "ImagMode"


class ImageModel:

    def __init__(self, img_data=0, url=None):
        if url is not None:
            self.img_data = cv2.imread(url, cv2.IMREAD_GRAYSCALE)
        else:
            self.img_data = img_data

        self.img_fft = np.fft.fft2(self.img_data)
        self.fft_shifted = np.fft.fftshift(self.img_fft)
        self.magnitude = np.abs(self.fft_shifted)
        self.phase = np.angle(self.fft_shifted)
        self.real = self.fft_shifted.real
        self.imaginary = self.fft_shifted.imag
        self.attrs = [
            self.magnitude,
            self.phase,
            self.img_fft.real,
            self.img_fft.imag
        ]
        self.img_brightness=self.img_data
        self.img_contrast=self.img_data
        self.region_type = "inner"  # Default is inner region
        self.region_percentage = 50  # Default is 50%

    def resize_image(self, target_width, target_height):
        # Resize the image
        resized_image_data = cv2.resize(self.img_data, (target_width, target_height))
        self.img_data=resized_image_data
        return ImageModel(resized_image_data)

    def brightness(self, brightness_factor, last_contrast_factor):
        img_data_brightness = np.clip((self.img_data * brightness_factor - 128) * last_contrast_factor + 128, 0, 255)
        self.img_brightness=img_data_brightness
        return ImageModel(img_data_brightness)

    def contrast(self, contrast_factor, last_brightness_factor):
        img_data_brightness = np.clip(self.img_data * last_brightness_factor, 0, 255)
        img_data_contrast = np.clip((img_data_brightness - 128) * contrast_factor + 128, 0, 255)
        self.img_contrast=img_data_contrast
        return ImageModel(img_data_contrast)

    def set_region_parameters(self, region_type, region_percentage):
        self.region_type = region_type
        self.region_percentage = region_percentage

    def get_selected_region(self, shape):
        rows, cols = shape
        center_row, center_col = rows // 2, cols // 2
        if self.region_type == "inner":
            percentage = abs(1 - self.region_percentage / 100)
            start_row = int(center_row - center_row * percentage)
            end_row = int(center_row + center_row * percentage)
            start_col = int(center_col - center_col * percentage)
            end_col = int(center_col + center_col * percentage)
        else:
            percentage = self.region_percentage / 100
            start_row = int(center_row - center_row * (percentage))
            end_row = int(center_row + center_row * (percentage))
            start_col = int(center_col - center_col * (percentage))
            end_col = int(center_col + center_col * (percentage))
        return start_row, end_row, start_col, end_col


    def mixer(self, ratio: float, mode: 'Modes', selected_region: int, region_size: float) -> np.ndarray:

        if selected_region == 0:
            selected_image = ImageModel(img_data=self.img_brightness)
        elif selected_region == 1:
            selected_image = self.lp_spatial(region_size / 100)
        elif selected_region == 2:
            selected_image = self.hp_spatial(1 - region_size / 100)

        if mode == Modes.magnitude:
            mag = ratio * selected_image.magnitude
            exp = np.exp(1j * selected_image.phase)
            mix = mag * exp
        elif mode == Modes.phase:
            if ratio == 0:
                mag = ratio*selected_image.magnitude
                exp = np.exp(1j * selected_image.phase)
                mix = mag * exp  # If ratio is zero, only magnitude matters
            else:
                phase = ratio * selected_image.phase
                exp = np.exp(1j * phase)
                mix = selected_image.magnitude * exp
        elif mode == Modes.real:
            real = ratio * selected_image.real
            mix = real
        elif mode == Modes.Imaginary:
            imag = 1j * (ratio * selected_image.imaginary)
            mix = imag

        return np.abs(np.fft.ifft2(mix))

    def lp_spatial(self, value):
        start_row, end_row, start_col, end_col = self.get_selected_region(self.img_data.shape)
        kernel = np.zeros_like(self.img_data)
        kernel[start_row:end_row, start_col:end_col] = 1
        fft_shifted = np.fft.fftshift(self.img_fft) * kernel
        return ImageModel(np.real(np.fft.ifft2(np.fft.ifftshift(fft_shifted))))

    def hp_spatial(self, value):
        start_row, end_row, start_col, end_col = self.get_selected_region(self.img_data.shape)
        kernel = np.zeros_like(self.img_data).astype(bool)
        kernel[start_row:end_row, start_col:end_col] = 1
        fft_shifted = np.fft.fftshift(self.img_fft) * ~kernel
        return ImageModel(np.real(np.fft.ifft2(np.fft.ifftshift(fft_shifted))))
