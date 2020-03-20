# -*- coding: utf-8 -*-

from PIL import Image
import numpy as np

def component_sample(comp):
    return comp[::2, ::2]

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

def rgb_to_420p(image_path, yuv_path):
    img = Image.open(image_path)
    img_width, img_height = img.size
    # r,g,b = img.split()
    # rgb = np.array([r.getdata(), g.getdata(), b.getdata()])
    rgb = np.array(img.getdata()).T
    trans_co = np.array([
        [0.299, 0.587, 0.114],
        [-0.169, -0.331, 0.500],
        [0.500, -0.419, -0.081]])
    tran_off = np.array([[0],[128],[128]])

    YCbCr = np.matmul(trans_co, rgb) + tran_off
    comp_Y, comp_Cb, comp_Cr = [comp.reshape(img_height, img_width) \
            for comp in YCbCr]
    comp_Cb = component_sample(comp_Cb)
    comp_Cr = component_sample(comp_Cr)

    comp_Y, comp_Cb, comp_Cr = [comp.astype(np.uint8) \
            for comp in [comp_Y, comp_Cb, comp_Cr]]
    write_420p(comp_Y, comp_Cb, comp_Cr, yuv_path)
