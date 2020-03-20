# -*- coding: utf-8 -*-

from PIL import Image
import numpy as np

def component_sample(comp):
    return comp[::2, ::2]

def pad_image(origin_img):
    assert len(origin_img) == 3
    comp, img_height, img_width = origin_img.shape
    padding_height = ((img_height+7)//8)*8 - img_height
    padding_width = ((img_width+7)//8)*8 - img_width
    origin_img = np.lib.pad(origin_img, ((0,0), (0, padding_height), (0, padding_width)), \
            'constant', constant_values=(0,0))
    return origin_img

def write_420p(comp_Y, comp_Cb, comp_Cr, yuv_path):
    """
    write data to file with data shift by yuv420 planar
    """
    with open(yuv_path, 'wb') as fp:
        for y in comp_Y.reshape([-1]):
            fp.write(y)
        for cb in comp_Cb.reshape([-1]):
            fp.write(cb)
        for cr in comp_Cr.reshape([-1]):
            fp.write(cr)

def rgb_to_420p(rgb_data):

    comp, img_height, img_width = rgb_data.shape
    rgb = np.array([c.reshape([-1]) for c in rgb_data])

    trans_co = np.array([
        [0.299, 0.587, 0.114],
        [-0.169, -0.331, 0.500],
        [0.500, -0.419, -0.081]])
    tran_off = np.array([[0],[128],[128]])

    YCbCr = np.matmul(trans_co, rgb) + tran_off
    comp_Y, comp_Cb, comp_Cr = [comp.reshape(img_height, img_width) \
            for comp in YCbCr]
    img_data = np.array([comp_Y, comp_Cb, comp_Cr])
    img_data = pad_image(img_data)
    comp_Y = img_data[0]
    comp_Cb, comp_Cr = component_sample(img_data[1]), component_sample(img_data[2])

    comp_Y, comp_Cb, comp_Cr = [comp.astype(np.uint8) \
            for comp in [comp_Y, comp_Cb, comp_Cr]]
    return comp_Y, comp_Cb, comp_Cr

def image_to_yuv(img_path, yuv_path):
    """
    return size of image and yuv
    """
    img = Image.open(img_path)
    img_width, img_height = img.size
    r,g,b = img.split()
    rgb_data = np.array([np.array(c.getdata()).reshape(img_height, img_width) \
            for c in [r,g,b]])
    comp_Y, comp_Cb, comp_Cr = rgb_to_420p(rgb_data)
    ycbcr_height, ycbcr_width= comp_Y.shape
    write_420p(comp_Y, comp_Cb, comp_Cr, yuv_path)
    return [img_height, img_width], [ycbcr_height, ycbcr_width]
